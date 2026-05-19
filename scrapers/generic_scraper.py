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
        # Common article/post selectors
        for selector in ["article a[href]", "h2 a[href]", "h3 a[href]", ".post-title a[href]"]:
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

        title = ""
        for sel in ["h1.entry-title", "h1.post-title", "h1"]:
            t = soup.select_one(sel)
            if t:
                title = t.get_text(strip=True)
                break

        desc = ""
        for sel in [".entry-content p", ".post-content p", "article p"]:
            d = soup.select_one(sel)
            if d:
                desc = d.get_text(strip=True)
                break

        img_url = ""
        for sel in [".post-thumbnail img", "article img", ".featured img"]:
            img = soup.select_one(sel)
            if img:
                img_url = img.get("src") or img.get("data-src") or ""
                break

        dl = soup.select_one("a[href*='download']")
        download_url = dl["href"] if dl else url

        full = soup.get_text(" ")
        size = version = ""
        m = re.search(r"Size\s*[:\-]\s*([\w\.\s]+(?:MB|GB))", full, re.I)
        if m: size = m.group(1).strip()[:50]
        m = re.search(r"Version\s*[:\-]\s*([\w\.\-]+)", full, re.I)
        if m: version = m.group(1).strip()[:50]

        return {
            "title": title or "Unknown",
            "description": desc[:600],
            "image_url": img_url,
            "download_url": download_url,
            "url": url,
            "size": size,
            "version": version,
            "category": "",
        }
    except Exception as e:
        logger.error(f"Generic detail error ({url}): {e}")
        return None