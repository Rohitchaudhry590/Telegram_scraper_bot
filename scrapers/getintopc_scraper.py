# ============================================================
#  scrapers/getintopc_scraper.py  —  GetIntoPC.com scraper
# ============================================================
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}

BASE = "https://getintopc.com"


def get_listing_urls(page: int = 1) -> list[str]:
    url = f"{BASE}/page/{page}/" if page > 1 else BASE + "/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.select("h2 a, h3 a, .entry-title a"):
            href = a.get("href", "")
            if href and "getintopc.com" in href:
                links.append(href)
        logger.info(f"GetIntoPC page {page}: {len(links)} links found")
        return list(dict.fromkeys(links))
    except Exception as e:
        logger.error(f"GetIntoPC listing error: {e}")
        return []


def scrape_detail(url: str) -> dict | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        title_tag = soup.select_one("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        desc_tag = soup.select_one(".entry-content p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        img_tag = soup.select_one(".entry-content img, .post img")
        image_url = ""
        if img_tag:
            image_url = img_tag.get("src") or img_tag.get("data-src") or ""

        dl_tag = soup.select_one("a[href*='download'], a.download")
        download_url = dl_tag["href"] if dl_tag else url

        size = version = category = ""
        full_text = soup.get_text(" ")
        import re
        m = re.search(r"Size\s*[:\-]\s*([\w\.\s]+MB|[\w\.\s]+GB)", full_text, re.I)
        if m: size = m.group(1).strip()
        m = re.search(r"Version\s*[:\-]\s*([\w\.\s]+)", full_text, re.I)
        if m: version = m.group(1).strip()[:50]

        return {
            "title": title,
            "description": description[:600],
            "image_url": image_url,
            "download_url": download_url,
            "url": url,
            "size": size[:50],
            "version": version,
            "category": category,
        }
    except Exception as e:
        logger.error(f"GetIntoPC detail error ({url}): {e}")
        return None