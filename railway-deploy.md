# 🚀 Railway.app pe Deploy Karo (FREE)

## Step 1: GitHub Account Setup
1. GitHub account banao: https://github.com/signup
2. Apna Telegram scraper bot repository fork karo
3. Ya naya repository create karo

## Step 2: Railway Account Setup
1. Railway.app jaao: https://railway.app
2. GitHub se login karo
3. "New Project" click karo

## Step 3: GitHub Repository Connect Karo
1. "Deploy from GitHub" select karo
2. Apna repository select karo (Rohitchaudhry590/Telegram_scraper_bot)
3. Deploy button click karo

## Step 4: Environment Variables Set Karo

Railway dashboard mein:
1. "Variables" tab kholo
2. Ye variables add karo:

```
TELEGRAM_BOT_TOKEN = 8981892893:AAEMHQ_0wW9F-bjUuvzabEX34SXbYMGbrpQ
TELEGRAM_CHANNEL_ID = @pccrackedapp
TARGET_WEBSITE = https://filecr.com
BACKFILL_PAGES = 10
CHECK_INTERVAL_MINUTES = 30
SEND_IMAGE = True
DESC_MAX_LEN = 800
POST_DELAY_SECONDS = 3
```

## Step 5: Deploy Karo
1. "Deploy" button press karo
2. Build process 3-5 minutes mein complete hoga
3. Logs mein "Bot started" message dekho ✅

## Step 6: Logs Check Karo
1. Railway dashboard mein "Logs" tab kholo
2. Bot ka progress dekho
3. Agar error aaye toh message bhejo

## 💾 Database Persistence

Railway mein database file automatically persist ho jayegi.
Agar manually backup chahiye:

1. Railway dashboard → "Volumes" tab
2. Naya volume create karo: `/app/posted.db`
3. Bot automatically ismein data save karega

## 🔄 Bot Restart Karo (Agar Slow Ho)

```bash
# Railway CLI se
railway up
railway down
railway up
```

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| "Bot token invalid" | Token sahi copy karo settings.py mein |
| "Chat not found" | Bot ko @pccrackedapp channel ka admin banao |
| "Deployment failed" | GitHub repo sahi connected hai check karo |
| Bot slow chalraha hai | CHECK_INTERVAL_MINUTES increase karo |

## ✅ Bot Successfully Running Agar:
- Railway logs mein "Bot started" likha hai
- Telegram channel pe posts aa rahe hain
- Har 30 minutes baad new posts aa rahe hain

---

**Cost:** ₹0 (Completely FREE)
**Uptime:** 24/7 (jab tak Railway free tier support karega)
**Speed:** Medium (Free tier)
