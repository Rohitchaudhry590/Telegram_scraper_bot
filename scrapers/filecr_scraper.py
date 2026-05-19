# ============================================================
#  scrapers/filecr_scraper.py  —  FileCR.com scraper (Fixed v3)
# ============================================================
import requests
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

BASE = "https://filecr.com"

SKIP_URLS = {
    f"{BASE}/android/",
    f"{BASE}/pc-games/",
    f"{BASE}/ms-windows/",
    f"{BASE}/mac/",
    f"{BASE}/android-games/",
    f"{BASE}/windows/",
    f"{BASE}/macos/",
}


def get_listing_urls(page: int = 1) -> list[str]:
    """Latest software listing page se URLs nikalao."""
    url = f"{BASE}/ms-windows/" if page == 1 else f"{BASE}/ms-windows/?page={page}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if (
                href.startswith("/windows/") or
                href.startswith("/macos/") or
                href.startswith("/android/") or
                href.startswith("/pc-games/")
            ):
                full_url = BASE + href
                parts = href.strip("/").split("/")
                # Sirf software pages lo, category pages nahi
                if full_url not in SKIP_URLS and len(parts) >= 2 and full_url not in links:
                    links.append(full_url)
        logger.info(f"FileCR page {page}: {len(links)} links found")
        return list(dict.fromkeys(links))
    except Exception as e:
        logger.error(f"FileCR listing error: {e}")
        return []


def scrape_detail(url: str) -> dict | None:
    """Ek software page ka full detail scrape karo."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Title — h1 se lo
        title_tag = soup.select_one("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Description — first meaningful paragraph
        description = ""
        for p in soup.select("p"):
            text = p.get_text(strip=True)
            # Navigation/menu text skip karo
            if len(text) > 40 and "windows" not in text.lower()[:20]:
                description = text
                break

        # Image — og:image sabse reliable hai FileCR pe
        image_url = ""
        og_img = soup.select_one("meta[property='og:image']")
        if og_img:
            image_url = og_img.get("content", "")
        if not image_url:
            img_tag = soup.select_one("img[src*='imgcdn'], img[src*='media']")
            if img_tag:
                image_url = img_tag.get("src") or img_tag.get("data-src") or ""

        # Download link
        dl_tag = soup.select_one("a[href*='download'], a.download-btn")
        download_url = dl_tag["href"] if dl_tag else url

        # Version — title se extract karo (most reliable)
        version = ""
        version_match = re.search(r'(\d+[\.\d]+)', title)
        if version_match:
            version = version_match.group(1)

        # Category — URL se extract karo
        category = ""
        parts = url.replace(BASE, "").strip("/").split("/")
        if len(parts) >= 1:
            cat_map = {
                "windows": "Windows",
                "macos": "MacOS",
                "android": "Android",
                "pc-games": "PC Games",
            }
            category = cat_map.get(parts[0], parts[0].title())

        # Size — page se dhundho
        size = ""
        for tag in soup.select("span, li, td, div"):
            text = tag.get_text(strip=True)
            size_match = re.search(r'(\d+\.?\d*\s*(mb|gb|kb))', text, re.IGNORECASE)
            if size_match:
                size = size_match.group(1).upper()
                break

        return {
            "title": title,
            "description": description,
            "image_url": image_url,
            "download_url": download_url,
            "url": url,
            "size": size,
            "version": version,
            "category": category,
        }
    except Exception as e:
        logger.error(f"FileCR detail error ({url}): {e}")
        return None
