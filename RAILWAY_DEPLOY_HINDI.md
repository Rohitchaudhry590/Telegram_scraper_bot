# 🚀 Railway.app pe Bot Deploy Karne Ka Complete Guide (HINDI)

## Railway Kya Hai?
Railway.app ek **FREE cloud hosting service** hai jo Python bots ko 24/7 chalane ke liye perfect hai!
- ✅ Bilkul FREE
- ✅ 24 ghante chalega
- ✅ GitHub se direct deploy
- ✅ Automatic restart

---

## 📋 STEP 1 — GitHub Account Banana (Agar Nahi Hai)

1. Browser mein jaao: **https://github.com/signup**
2. "Sign up" button click karo
3. Email, password daro aur account banao
4. Email verify karo (GitHub tum ko email bhejega)

✅ **GitHub account ready!**

---

## 📋 STEP 2 — Railway.app Account Banana

1. Browser mein jaao: **https://railway.app**
2. Upar right corner mein "Sign In" click karo
3. "Continue with GitHub" click karo
4. GitHub login karo (pop-up mein)
5. Railway ko permission do

✅ **Railway account ready!**

---

## 🔗 STEP 3 — Bot Repository GitHub pe Upload Karo

### Option A: EASIEST (GitHub Desktop se)

**GitHub Desktop Install Karo:**
1. https://desktop.github.com jaao
2. Download aur install karo

**Repository Create Karo:**
1. GitHub Desktop kholo → "File" → "New Repository"
2. Name: `Telegram_scraper_bot`
3. Description: `Telegram Software Auto-Poster Bot`
4. "Create Repository" click karo
5. Folder select karo jahan apni files ho

**Files Upload Karo:**
1. GitHub Desktop mein left side mein changes dikhenge
2. Neeche "Summary" mein message likho: `Initial commit - Bot files`
3. "Commit to main" click karo
4. Upar mein "Publish repository" click karo
5. GitHub.com par auto-open ho jayega ✅

### Option B: Git Command Se (Advanced Users)

```bash
cd /path/to/bot/folder
git init
git add .
git commit -m "Initial commit - Bot files"
git remote add origin https://github.com/YOUR_USERNAME/Telegram_scraper_bot.git
git branch -M main
git push -u origin main
```

✅ **Bot GitHub pe upload ho gaya!**

---

## 🚂 STEP 4 — Railway.app se Deploy Karo

### 4.1 Railway Dashboard Kholo

1. https://railway.app jaao (apka account logged in hona chahiye)
2. Dashboard mein "New Project" button dekho (neeche right side mein)
3. Click karo "Deploy from GitHub"

### 4.2 GitHub Repository Connect Karo

1. Pop-up mein GitHub se login karo (agar nahi ho)
2. Apna repository dhundo: **`Telegram_scraper_bot`**
3. Click karo select karne ke liye
4. "Deploy" button click karo

**Bot deployment shuru hoga!** ⏳ (3-5 minute lagenge)

✅ **Deployment complete hone ka wait karo!**

---

## ⚙️ STEP 5 — Environment Variables Set Karo

### Ye IMPORTANT hai! Bot ko token aur channel ID batana padega.

1. Railway dashboard mein apna project kholo
2. Left sidebar mein "Variables" tab dhundo
3. "Environment" section mein ho
4. **Ye sab variables add karo:**

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

### Har variable ke liye:
1. "Add Variable" button click karo
2. **Key** likho (e.g., `TELEGRAM_BOT_TOKEN`)
3. **Value** likho (e.g., token)
4. "Save" click karo
5. Sab variables add hone ke baad **"Save"** final ek baar click karo

✅ **Variables set ho gaye!**

---

## 🎬 STEP 6 — Bot Start Karo

1. Railway dashboard mein left side mein "Deployments" dekho
2. Pehle deployment dekho (build aur running status)
3. Agar **"Running"** likha hai ✅ to bot chalu hai!
4. Agar error hai to "Logs" tab mein dekho

### Bot Check Karne Ke Liye:

1. Telegram mein **@pccrackedapp** channel kholo
2. Neeche scroll karo
3. Bot ka message dikhai dena chahiye:
   ```
   🤖 Bot started! Backfilling 10 pages from https://filecr.com...
   ```

✅ **Bot successfully running hai!**

---

## 📊 STEP 7 — Logs Check Karo (Debugging)

Agar bot slow chal raha hai ya error aaye:

1. Railway dashboard → "Logs" tab
2. Neeche from dropdown mein **"latest"** select karo
3. Real-time logs dekho
4. Agar red text (ERROR) hai to screenshot lo aur mujhe bhejo

**Common Errors:**

| Error | Solution |
|-------|----------|
| `Bot token invalid` | Token copy-paste sahi se karo, spaces check karo |
| `Chat not found` | @pccrackedapp channel check karo, bot admin ho |
| `Connection timeout` | Railway ko 5 min aur wait do |
| `Module not found` | requirements.txt check karo |

---

## 🔄 STEP 8 — Bot Restart Karo (Agar Slow Ho)

1. Railway dashboard → "Services" tab
2. Apna service click karo
3. Top right mein **"Restart"** button click karo
4. Bot 30 seconds mein restart ho jayega

---

## 💾 STEP 9 — Database Backup Lena (Optional)

Apke bot ne jitne posts bheje hain, sab `posted.db` file mein save hain.
Agar backup lena hai:

1. Railway dashboard → "Data" tab
2. `posted.db` file dekho
3. Click karo download karne ke liye
4. Apne computer mein save karo

---

## 🎉 SUCCESS! Bot LIVE Hai!

### Ab Bot Automatically Ye Karega:

✅ **Har 30 minutes mein:**
- FileCR aur GetIntoPC se naye software check karega
- Naye posts @pccrackedapp channel pe post karega
- Database mein URL save karega (duplicate posts nahi honge)

✅ **Har bar start hone pe:**
- Pehle 10 pages backfill karega (sirf pehli baar)
- Phir watch mode mein chala jayega

✅ **24/7 Online:**
- Railway automatically bot ko restart karega
- Agar crash ho to khud restart hoga

---

## 📱 Bot Status Check Karna

### Telegram Channel mein Messages Dekho:

```
🤖 Bot started! Backfilling 10 pages...
📦 Adobe Photoshop 2024 v25.5
🔖 Version: 25.5.0
💾 Size: 2.4 GB
📝 Adobe is the world's best...
🔗 Download Now

📬 3 naye posts bheje gaye!
😴 Koi naya post nahi mila.
```

Agar ye messages dikhai de rahe hain to ✅ **Bot perfect chal raha hai!**

---

## ⚠️ Important Tips

1. **Token Share Mat Karna** - Token secret rakhna!
2. **Channel Admin** - Ensure bot @pccrackedapp ka admin ho
3. **Variables Double Check** - Copy-paste mein space/typo na ho
4. **Regular Logs Check** - Errors aaye to jaldi fix karo
5. **Database Backup** - Weekly backup lo

---

## 🆘 Agar Kuch Gadbad Ho

### 1️⃣ Bot Nahi Chal Raha
```
→ Railway Logs check karo
→ Environment variables double-check karo
→ Token sahi ho
→ Channel ID correct ho
→ Railway Restart karo
```

### 2️⃣ Posts Nahi Ho Rahe
```
→ Check karo bot admin @pccrackedapp mein hai
→ Logs mein error dekho
→ Token valid hai?
→ Channel accessible hai?
```

### 3️⃣ Duplicate Posts
```
→ posted.db file delete mat karo
→ Database corrupt ho gaya to naya restart karo
```

---

## 🎓 Next Steps

1. ✅ Bot successfully deployed
2. ✅ Logs check karo daily
3. ✅ Features improve karne ke liye code modify karo
4. ✅ More websites add karne ke liye scrapers update karo

---

## 📞 Support

Koi issue ho to:
1. GitHub Issues mein likho
2. Telegram mein message karo
3. Logs screenshot share karo

**Happy Botting! 🤖**
