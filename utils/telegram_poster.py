# ============================================================
#  utils/telegram_poster.py  —  Telegram pe message bhejo
# ============================================================
import requests
import time
import logging
from config.settings import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID,
    SEND_IMAGE, DESC_MAX_LEN, POST_DELAY_SECONDS
)

logger = logging.getLogger(__name__)
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def format_message(item: dict) -> str:
    title       = item.get("title", "No Title")
    description = item.get("description", "")[:DESC_MAX_LEN]
    download    = item.get("download_url", item.get("url", ""))
    category    = item.get("category", "")
    size        = item.get("size", "")
    version     = item.get("version", "")

    lines = [f"📦 <b>{title}</b>"]
    if version:     lines.append(f"🔖 Version: {version}")
    if category:    lines.append(f"🗂 Category: {category}")
    if size:        lines.append(f"💾 Size: {size}")
    if description:
        lines.append(f"\n📝 {description}")
    if download:
        lines.append(f"\n🔗 <a href='{download}'>Download Now</a>")

    return "\n".join(lines)


def send_post(item: dict) -> bool:
    """Post ek software item Telegram channel pe."""
    text = format_message(item)
    image_url = item.get("image_url", "").strip()

    # Image valid hai ya nahi check karo
    has_valid_image = (
        SEND_IMAGE and
        image_url and
        image_url.startswith("http")
    )

    try:
        if has_valid_image:
            resp = requests.post(
                f"{BASE_URL}/sendPhoto",
                data={
                    "chat_id": TELEGRAM_CHANNEL_ID,
                    "photo": image_url,
                    "caption": text,
                    "parse_mode": "HTML",
                },
                timeout=20
            )
            data = resp.json()

            # Agar photo fail ho toh text se try karo
            if not data.get("ok"):
                logger.warning(f"⚠️ Photo send failed, text se try kar raha: {data}")
                resp = requests.post(
                    f"{BASE_URL}/sendMessage",
                    data={
                        "chat_id": TELEGRAM_CHANNEL_ID,
                        "text": text,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": False,
                    },
                    timeout=20
                )
                data = resp.json()
        else:
            resp = requests.post(
                f"{BASE_URL}/sendMessage",
                data={
                    "chat_id": TELEGRAM_CHANNEL_ID,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False,
                },
                timeout=20
            )
            data = resp.json()

        if data.get("ok"):
            logger.info(f"✅ Posted: {item.get('title')}")
            time.sleep(POST_DELAY_SECONDS)
            return True
        else:
            logger.error(f"❌ Telegram error: {data}")
            return False

    except Exception as e:
        logger.error(f"❌ Exception posting to Telegram: {e}")
        return False


def send_status_message(text: str):
    """Status message bhejo."""
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            data={"chat_id": TELEGRAM_CHANNEL_ID, "text": text},
            timeout=10
        )
    except Exception:
        pass
