# ============================================================
#  scrapers/filecr_scraper.py  —  FileCR.com scraper
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
    url = f"{BASE}/page/{page}/" if page > 1 else f"{BASE}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.select("h2.post-title a, h3.title a, article a.entry-title-link"):
            href = a.get("href", "")
            if href and href.startswith("http"):
                links.append(href)
        # fallback broad selector
        if not links:
            for a in soup.select("article a[href]"):
                href = a["href"]
                if BASE in href and href not in links:
                    links.append(href)
        logger.info(f"FileCR page {page}: {len(links)} links found")
        return list(dict.fromkeys(links))  # deduplicate
    except Exception as e:
        logger.error(f"FileCR listing error: {e}")
        return []


def scrape_detail(url: str) -> dict | None:
    """Ek software page ka full detail scrape karo."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Title
        title_tag = soup.select_one("h1.post-title, h1.entry-title, h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Description (first paragraph)
        desc_tag = soup.select_one(".entry-content p, .post-content p, article p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # Thumbnail / featured image
        img_tag = soup.select_one(".post-thumbnail img, .featured-image img, article img")
        image_url = ""
        if img_tag:
            image_url = img_tag.get("src") or img_tag.get("data-src") or ""

        # Download link (external)
        dl_tag = soup.select_one("a.download-btn, a[href*='download'], a.btn-download")
        download_url = dl_tag["href"] if dl_tag else url

        # Meta info (size, version, category)
        size = version = category = ""
        for li in soup.select(".post-meta li, .entry-meta li, table tr"):
            text = li.get_text(" ", strip=True).lower()
            if "size" in text:
                size = li.get_text(strip=True).replace("Size:", "").replace("size:", "").strip()
            if "version" in text:
                version = li.get_text(strip=True).replace("Version:", "").replace("version:", "").strip()
            if "categor" in text:
                category = li.get_text(strip=True).replace("Category:", "").replace("category:", "").strip()

        return {
            "title": title,
            "description": description,
            "image_url": image_url,
            "download_url": download_url,
            "url": url,
            "size": size[:50],
            "version": version[:50],
            "category": category[:50],
        }
    except Exception as e:
        logger.error(f"FileCR detail error ({url}): {e}")
        return None