# ============================================================
#  scrapers/getintopc_scraper.py  —  GetIntoPC.com scraper
# ============================================================
import requests
from bs4 import BeautifulSoup
import logging
import re

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
        for a in soup.select("h2 a, h3 a, .entry-title a, article a"):
            href = a.get("href", "")
            if href and "getintopc.com" in href and href not in links:
                # Sirf software pages lo
                parts = href.replace(BASE, "").strip("/").split("/")
                if len(parts) >= 1 and parts[0]:
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

        # Title
        title_tag = soup.select_one("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Description — meaningful paragraph
        description = ""
        for p in soup.select(".entry-content p, article p"):
            text = p.get_text(strip=True)
            if len(text) > 40:
                description = text
                break

        # Image — og:image sabse reliable
        image_url = ""
        og_img = soup.select_one("meta[property='og:image']")
        if og_img:
            image_url = og_img.get("content", "")
        if not image_url:
            img_tag = soup.select_one(".entry-content img, .post img")
            if img_tag:
                image_url = img_tag.get("src") or img_tag.get("data-src") or ""

        # Version — title se extract
        version = ""
        version_match = re.search(r'(\d+[\.\d]+)', title)
        if version_match:
            version = version_match.group(1)

        # Size
        size = ""
        full_text = soup.get_text(" ")
        m = re.search(r"Size\s*[:\-]\s*([\d\.]+\s*(?:MB|GB|KB))", full_text, re.I)
        if m:
            size = m.group(1).strip()[:50]

        # Category — URL se
        category = ""
        parts = url.replace(BASE, "").strip("/").split("/")
        if len(parts) >= 1:
            category = parts[0].replace("-", " ").title()

        return {
            "title": title,
            "description": description[:600],
            "image_url": image_url,
            "download_url": url,
            "url": url,
            "size": size,
            "version": version,
            "category": category,
        }
    except Exception as e:
        logger.error(f"GetIntoPC detail error ({url}): {e}")
        return None
