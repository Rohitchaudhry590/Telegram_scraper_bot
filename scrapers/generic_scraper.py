# ============================================================
#  scrapers/generic_scraper.py  —  Kisi bhi website ke liye
# ============================================================
import requests
from bs4 import BeautifulSoup
import logging
import re
from config.settings import TARGET_WEBSITE

logger = logging.getLogger(__name__)
BASE = TARGET_WEBSITE.rstrip("/")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}


def get_listing_urls(page: int = 1) -> list[str]:
    url = f"{BASE}/page/{page}/" if page > 1 else BASE + "/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for selector in [
            "article a[href]",
            "h2 a[href]",
            "h3 a[href]",
            ".post-title a[href]",
            ".entry-title a[href]"
        ]:
            for a in soup.select(selector):
                href = a.get("href", "")
                if href and BASE in href and href not in links:
                    links.append(href)
        logger.info(f"Generic page {page}: {len(links)} links")
        return list(dict.fromkeys(links))
    except Exception as e:
        logger.error(f"Generic listing error: {e}")
        return []


def scrape_detail(url: str) -> dict | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Title
        title = ""
        for sel in ["h1.entry-title", "h1.post-title", "h1"]:
            t = soup.select_one(sel)
            if t:
                title = t.get_text(strip=True)
                break

        # Description
        description = ""
        for p in soup.select(".entry-content p, .post-content p, article p"):
            text = p.get_text(strip=True)
            if len(text) > 40:
                description = text
                break

        # Image — og:image first
        image_url = ""
        og_img = soup.select_one("meta[property='og:image']")
        if og_img:
            image_url = og_img.get("content", "")
        if not image_url:
            for sel in [".post-thumbnail img", "article img", ".featured img"]:
                img = soup.select_one(sel)
                if img:
                    image_url = img.get("src") or img.get("data-src") or ""
                    if image_url:
                        break

        # Version — title se
        version = ""
        version_match = re.search(r'(\d+[\.\d]+)', title)
        if version_match:
            version = version_match.group(1)

        # Size
        size = ""
        full = soup.get_text(" ")
        m = re.search(r"Size\s*[:\-]\s*([\d\.]+\s*(?:MB|GB|KB))", full, re.I)
        if m:
            size = m.group(1).strip()[:50]

        return {
            "title": title or "Unknown",
            "description": description[:600],
            "image_url": image_url,
            "download_url": url,
            "url": url,
            "size": size,
            "version": version,
            "category": "",
        }
    except Exception as e:
        logger.error(f"Generic detail error ({url}): {e}")
        return None
