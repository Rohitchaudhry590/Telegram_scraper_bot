# 📱 Telegram Software Auto-Poster Bot — Setup Guide (Hindi)

## 🎯 Ye Bot Kya Karta Hai?
Ye bot automatically kisi bhi PC software website (FileCR, GetIntoPC, etc.) se
naye software scrape karke aapke Telegram channel pe post karta hai.
Purane/existing posts bhi ek baar mein sab post kar sakta hai.

---

## 📋 STEP 1 — Telegram Bot Banana

1. Telegram mein **@BotFather** ko open karo
2. `/newbot` type karo
3. Bot ka naam do (e.g. "My Software Hub")
4. Username do (e.g. `MySoftwareHub_bot`)
5. BotFather aapko ek **Token** dega — ise copy karo
   ```
   Example: 7812345678:AAHdqTcvCH1vGWJxfSeofSs0K5PALDsaw
   ```

---

## 📢 STEP 2 — Telegram Channel Setup

1. Telegram mein ek **Channel** banao
2. Apne bot ko channel ka **Admin** banao
   - Channel Settings → Administrators → Add Admin → apna bot dhundo
3. Channel ka **ID** nikalo:
   - Public channel ke liye: `@yourchannel`
   - Private ke liye: web.telegram.org pe jaao, channel open karo, URL mein number copy karo (add `-100` prefix)

---

## ⚙️ STEP 3 — Settings Configure Karo

`config/settings.py` file kholo aur ye fill karo:

```python
TELEGRAM_BOT_TOKEN  = "7812345678:AAHdqTcvCH1vGWJxfSeofSs0K5PALDsaw"
TELEGRAM_CHANNEL_ID = "@MySoftwareChannel"
TARGET_WEBSITE      = "https://filecr.com"   # ya getintopc.com
BACKFILL_PAGES      = 10   # Kitne purane pages post karne hain
CHECK_INTERVAL_MINUTES = 30
```

---

## 💻 STEP 4 — Python Setup (Local Machine)

### Windows:
```bash
# Python 3.11+ install karo: python.org
# Phir command prompt mein:
cd telegram-scraper-bot
pip install -r requirements.txt
python main.py
```

### Linux/Mac:
```bash
cd telegram-scraper-bot
pip3 install -r requirements.txt
python3 main.py
```

---

## 🐳 STEP 5 — Docker se Deploy (Recommended)

```bash
# Docker install karo: docker.com

# Build karo
docker build -t tg-software-bot .

# Run karo (always restart)
docker run -d \
  --name tg-bot \
  --restart always \
  -v $(pwd)/data:/app \
  tg-software-bot

# Logs dekhne ke liye:
docker logs -f tg-bot
```

---

## ☁️ STEP 6 — Free Cloud Deploy Options

### Option A — Railway.app (Easiest, FREE)
1. github.com pe account banao
2. Project folder GitHub pe upload karo
3. railway.app jaao → "New Project" → "Deploy from GitHub"
4. Environment variables mein `TELEGRAM_BOT_TOKEN` etc. daalo
5. Deploy! ✅

### Option B — Render.com (FREE)
1. render.com pe account
2. New → Background Worker → GitHub repo connect
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python main.py`

### Option C — VPS (DigitalOcean/Hostinger ₹200/month)
```bash
# Server pe upload karo, phir:
screen -S bot
python3 main.py
# Ctrl+A+D to detach
```

---

## 🚀 STEP 7 — Bot Run Karo

```bash
# OPTION 1: Sirf backfill (purane sab posts)
python main.py backfill

# OPTION 2: Sirf watch mode (naye posts)
python main.py watch

# OPTION 3: Dono (default — recommended)
python main.py
```

---

## 📊 Bot Output Example

Jab bot post karega, Telegram channel pe aisa dikhega:

```
📦 Adobe Photoshop 2024 v25.5
🔖 Version: 25.5.0
🗂 Category: Design
💾 Size: 2.4 GB

📝 Adobe Photoshop is the world's best
imaging and design app...

🔗 Download Now
```

---

## ❓ Common Problems & Solutions

| Problem | Solution |
|---------|----------|
| "Bot token invalid" | BotFather se token dobara copy karo |
| "Chat not found" | Bot ko channel admin banao |
| "No URLs found" | Website ka structure check karo / scraper update karo |
| Posts repeat ho rahe hain | `posted.db` file delete mat karo |

---

## 📁 File Structure

```
telegram-scraper-bot/
├── main.py                  ← Bot start karne ke liye
├── requirements.txt         ← Python packages
├── Dockerfile               ← Docker deploy
├── config/
│   └── settings.py          ← ⭐ AAPKI SETTINGS YAHAN
├── scrapers/
│   ├── filecr_scraper.py    ← FileCR.com scraper
│   ├── getintopc_scraper.py ← GetIntoPC.com scraper
│   └── generic_scraper.py   ← Kisi bhi site ke liye
└── utils/
    ├── database.py          ← Posted URLs track karna
    └── telegram_poster.py   ← Telegram mein post karna
```

---

## 🆘 Support
Agar koi error aaye toh `bot.log` file check karo — wahan sab detail hogi.