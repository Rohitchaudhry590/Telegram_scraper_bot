# ============================================================
#  config/settings.py  —  Apni settings yahan bharo
# ============================================================

# 🔑 Telegram Bot Token  (BotFather se lena)
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# 📢 Telegram Channel ID  (e.g. "@mychannel"  ya  "-1001234567890")
TELEGRAM_CHANNEL_ID = "@your_channel_here"

# 🌐 Target website  (jo scrape karni hai)
# Examples: "https://filecr.com", "https://getintopc.com", "https://crackedforum.io"
TARGET_WEBSITE = "https://filecr.com"

# ⏰ Kitne minutes baad check kare naye posts ke liye  (default: 30 min)
CHECK_INTERVAL_MINUTES = 30

# 📦 Pehli baar kitne purane posts backfill kare  (0 = sirf naye)
BACKFILL_PAGES = 5

# 🗃️ Database file (SQLite) — previously posted URLs track karne ke liye
DB_FILE = "posted.db"

# 📝 Log file
LOG_FILE = "bot.log"

# 🖼️ Image ke saath post kare ya nahi
SEND_IMAGE = True

# ✂️ Description ki max length (characters)
DESC_MAX_LEN = 800

# ⏳ Telegram rate-limit ke liye delay (seconds) between posts
POST_DELAY_SECONDS = 3