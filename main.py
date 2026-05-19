#!/usr/bin/env python3
# ============================================================
#  main.py  —  Bot ka main entry point
# ============================================================
import time
import logging
import sys

from config.settings import CHECK_INTERVAL_MINUTES, BACKFILL_PAGES, TARGET_WEBSITE
from utils.database import init_db, is_already_posted, mark_as_posted, get_total_posted
from utils.telegram_poster import send_post, send_status_message

# ── Logging setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_scraper():
    """Website ke hisaab se scraper load karo."""
    site = TARGET_WEBSITE.lower()
    if "filecr" in site:
        from scrapers.filecr_scraper import get_listing_urls, scrape_detail
    elif "getintopc" in site:
        from scrapers.getintopc_scraper import get_listing_urls, scrape_detail
    else:
        from scrapers.generic_scraper import get_listing_urls, scrape_detail
    return get_listing_urls, scrape_detail


def process_pages(get_listing_urls, scrape_detail, pages: int = 1):
    """Given number of pages scrape karo aur naye items post karo."""
    posted_count = 0
    for page in range(1, pages + 1):
        urls = get_listing_urls(page)
        if not urls:
            logger.info(f"Page {page}: No URLs found, stopping.")
            break

        for url in urls:
            if is_already_posted(url):
                logger.debug(f"SKIP (already posted): {url}")
                continue

            item = scrape_detail(url)
            if not item:
                continue

            success = send_post(item)
            if success:
                mark_as_posted(url, item.get("title", ""))
                posted_count += 1
                logger.info(f"Posted [{posted_count}]: {item['title']}")
            else:
                logger.warning(f"Failed to post: {url}")

    return posted_count


def backfill():
    """Pehli baar purane posts bhi bhejo."""
    get_listing_urls, scrape_detail = load_scraper()
    logger.info(f"🔄 Backfill shuru: {BACKFILL_PAGES} pages")
    send_status_message(f"🤖 Bot started! Backfilling {BACKFILL_PAGES} pages from {TARGET_WEBSITE}...")
    count = process_pages(get_listing_urls, scrape_detail, pages=BACKFILL_PAGES)
    logger.info(f"✅ Backfill complete. {count} posts bheje gaye.")
    send_status_message(f"✅ Backfill done! {count} posts sent. Total in DB: {get_total_posted()}")


def watch_loop():
    """Har X minutes mein check karo naye posts ke liye."""
    get_listing_urls, scrape_detail = load_scraper()
    interval = CHECK_INTERVAL_MINUTES * 60
    logger.info(f"👀 Watch loop shuru. Har {CHECK_INTERVAL_MINUTES} min check karega.")

    while True:
        logger.info("🔍 Checking for new posts...")
        count = process_pages(get_listing_urls, scrape_detail, pages=1)
        if count:
            logger.info(f"📬 {count} naye posts bheje gaye!")
        else:
            logger.info("😴 Koi naya post nahi mila.")
        time.sleep(interval)


# ── Entry Point ────────────────────────────────────────────
if __name__ == "__main__":
    init_db()

    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode == "backfill":
        backfill()
    elif mode == "watch":
        watch_loop()
    else:
        # Default: pehle backfill, phir watch
        backfill()
        watch_loop()
