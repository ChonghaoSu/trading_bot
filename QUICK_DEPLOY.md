# ⚡ Quick Deploy Guide

Get your bot running 24/7 in 5 minutes!

---

## 🎯 Fastest Option: Replit (Free)

### Step 1: Upload to GitHub
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/trading-bot.git
git push -u origin main
```

### Step 2: Import to Replit
1. Go to [replit.com](https://replit.com)
2. Click "Create Repl"
3. Select "Import from GitHub"
4. Paste your repo URL
5. Click "Import"

### Step 3: Set Secrets
1. Click "Secrets" (lock icon)
2. Add these variables:
   - `TELEGRAM_BOT_TOKEN` = your token
   - `TELEGRAM_CHAT_ID` = your chat ID
   - `RESEND_API_KEY` = your key
   - `EMAIL_FROM` = your email
   - `EMAIL_TO` = your email
   - (Add all from `env.example`)

### Step 4: Run
1. Click "Run" button
2. Bot starts automatically! ✅

### Step 5: Keep Alive (Free Tier)
1. Sign up at [uptimerobot.com](https://uptimerobot.com) (free)
2. Add monitor → HTTP(s) → Your Repl URL
3. Set interval: 5 minutes
4. Done! Bot stays alive 24/7

---

## 💰 Best Option: Railway ($5/month)

### Step 1: Deploy
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub"
4. Select your repo

### Step 2: Configure
1. Go to "Variables" tab
2. Add all variables from `env.example`
3. Go to "Settings" → "Deploy"
4. Set start command: `python bot.py`

### Step 3: Deploy
- Railway auto-deploys
- Bot runs 24/7! ✅

---

## 🏠 Home Option: Raspberry Pi

### Step 1: Buy Hardware
- Raspberry Pi 4 ($50)
- MicroSD card (32GB+)
- Power supply

### Step 2: Setup
```bash
# Install OS, then:
git clone your-repo-url
cd trading-bot
cp env.example .env
nano .env  # Fill in credentials
pip3 install -r requirements.txt
```

### Step 3: Auto-Start
```bash
sudo nano /etc/systemd/system/trading-bot.service
```

Paste:
```ini
[Unit]
Description=Trading Bot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/trading-bot
ExecStart=/usr/bin/python3 /home/pi/trading-bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable trading-bot
sudo systemctl start trading-bot
```

Done! Bot runs 24/7 at home! ✅

---

## ✅ Verification

After deploying, test:

```bash
python bot.py --test-alerts
```

You should receive test notifications!

---

## 📊 Comparison

| Platform | Time | Cost | Difficulty |
|----------|------|------|------------|
| Replit | 5 min | Free | ⭐ Easy |
| Railway | 10 min | $5/mo | ⭐ Easy |
| Raspberry Pi | 30 min | $50 once | ⭐⭐ Medium |

---

**Choose one and deploy! Your bot will run 24/7! 🚀**

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

