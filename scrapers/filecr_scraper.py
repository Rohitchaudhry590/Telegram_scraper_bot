# ============================================================
#  scrapers/filecr_scraper.py  —  FileCR.com scraper (Updated)
# ============================================================
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

BASE = "https://filecr.com"


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
                if full_url not in links:
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

        # Title
        title_tag = soup.select_one("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Description
        desc_tag = soup.select_one("div p, article p, main p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # Image (FileCR imgcdn se serve karta hai)
        img_tag = soup.select_one("img[src*='imgcdn']")
        image_url = ""
        if img_tag:
            image_url = img_tag.get("src") or img_tag.get("data-src") or ""

        # Download link
        dl_tag = soup.select_one("a[href*='download'], a.download-btn, a[href*='get']")
        download_url = dl_tag["href"] if dl_tag else url

        # Size, Version, Category
        size = version = category = ""
        for li in soup.select("li, tr, div"):
            text = li.get_text(" ", strip=True).lower()
            if "size" in text and not size:
                size = li.get_text(strip=True)[:50]
            if "version" in text and not version:
                version = li.get_text(strip=True)[:50]
            if "categor" in text and not category:
                category = li.get_text(strip=True)[:50]

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
