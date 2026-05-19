# ============================================================
#  scrapers/filecr_scraper.py  —  FileCR.com scraper (Full)
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

# Saari categories
CATEGORIES = [
    "/ms-windows/",
    "/mac/",
    "/android/",
    "/android-games/",
    "/pc-games/",
]

# Skip karo sirf top-level category pages
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
    """Saari categories se URLs nikalao."""
    all_links = []

    for category in CATEGORIES:
        if page == 1:
            url = f"{BASE}{category}"
        else:
            url = f"{BASE}{category}?page={page}"

        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")

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
                    if (
                        full_url not in SKIP_URLS and
                        len(parts) >= 2 and
                        full_url not in all_links
                    ):
                        all_links.append(full_url)

            logger.info(f"FileCR {category} page {page}: {len(all_links)} links so far")

        except Exception as e:
            logger.error(f"FileCR listing error ({category}): {e}")
            continue

    return list(dict.fromkeys(all_links))


def scrape_detail(url: str) -> dict | None:
    """Ek software page ka full detail scrape karo."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Title
        title_tag = soup.select_one("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Description
        description = ""
        for p in soup.select("p"):
            text = p.get_text(strip=True)
            if len(text) > 40 and "windows" not in text.lower()[:20]:
                description = text
                break

        # Image — og:image sabse reliable
        image_url = ""
        og_img = soup.select_one("meta[property='og:image']")
        if og_img:
            image_url = og_img.get("content", "")
        if not image_url:
            img_tag = soup.select_one("img[src*='imgcdn'], img[src*='media']")
            if img_tag:
                image_url = img_tag.get("src") or img_tag.get("data-src") or ""

        # Version — title se extract karo
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
                "android": "Android Apps",
                "pc-games": "PC Games",
            }
            category = cat_map.get(parts[0], parts[0].title())

        # Size
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
            "download_url": url,
            "url": url,
            "size": size,
            "version": version,
            "category": category,
        }
    except Exception as e:
        logger.error(f"FileCR detail error ({url}): {e}")
        return None
