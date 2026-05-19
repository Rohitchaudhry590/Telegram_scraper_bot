# ============================================================
#  config/settings.py  — Apni settings yahan bharo
# ============================================================
import os

# 🔑 Telegram Bot Token  (BotFather se lena)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8981892893:AAEMHQ_0wW9F-bjUuvzabEX34SXbYMGbrpQ")

# 📢 Telegram Channel ID  (e.g. "@mychannel"  ya  "-1001234567890")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "@pccrackedapp")

# 🌐 Target website  (jo scrape karni hai)
# Examples: "https://filecr.com", "https://getintopc.com", "https://crackedforum.io"
TARGET_WEBSITE = os.getenv("TARGET_WEBSITE", "https://filecr.com")

# ⏰ Kitne minutes baad check kare naye posts ke liye  (default: 30 min)
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))

# 📦 Pehli baar kitne purane posts backfill kare  (0 = sirf naye)
BACKFILL_PAGES = int(os.getenv("BACKFILL_PAGES", "10"))

# 🗃️ Database file (SQLite) — previously posted URLs track karne ke liye
DB_FILE = os.getenv("DB_FILE", "posted.db")

# 📝 Log file
LOG_FILE = os.getenv("LOG_FILE", "bot.log")

# 🖼️ Image ke saath post kare ya nahi
SEND_IMAGE = os.getenv("SEND_IMAGE", "True").lower() == "true"

# ✂️ Description ki max length (characters)
DESC_MAX_LEN = int(os.getenv("DESC_MAX_LEN", "800"))

# ⏳ Telegram rate-limit ke liye delay (seconds) between posts
POST_DELAY_SECONDS = int(os.getenv("POST_DELAY_SECONDS", "3"))

# 🌐 Multiple websites ke liye (rotation mode)
WEBSITES = [
    "https://filecr.com",
    "https://getintopc.com"
]

# 🔄 Rotation mode - har website se alternate scrape karo
ROTATION_MODE = True
