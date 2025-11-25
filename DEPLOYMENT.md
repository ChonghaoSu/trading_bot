# 🚀 Deployment Guide - Running Your Bot 24/7

This guide explains how to deploy your trading bot so it runs continuously, even when your computer is off.

---

## ⚠️ Important: Why You Need Cloud Deployment

**If you delete the codebase or turn off your computer, the bot stops working.**

To run 24/7, you need to deploy to a cloud service that:
- ✅ Runs continuously (even when your computer is off)
- ✅ Has internet connection
- ✅ Can run Python scripts
- ✅ Is free or low-cost

---

## 🌐 Deployment Options

### Option 1: Replit (Recommended for Beginners) ⭐

**Free tier available, easiest setup**

#### Pros:
- ✅ Completely free for basic use
- ✅ No credit card required
- ✅ Built-in code editor
- ✅ Automatic deployment from GitHub
- ✅ Easy environment variable setup

#### Cons:
- ⚠️ Free tier sleeps after inactivity (use UptimeRobot to keep alive)
- ⚠️ Limited resources

#### Setup Steps:

1. **Create Replit Account**
   - Go to [replit.com](https://replit.com)
   - Sign up (free)

2. **Import from GitHub**
   - Click "Create Repl"
   - Select "Import from GitHub"
   - Paste your repository URL
   - Click "Import"

3. **Set Environment Variables**
   - Click "Secrets" (lock icon in sidebar)
   - Add each variable from `env.example`:
     ```
     TELEGRAM_BOT_TOKEN = your_token_here
     TELEGRAM_CHAT_ID = your_chat_id
     RESEND_API_KEY = your_key_here
     EMAIL_FROM = your_email@domain.com
     EMAIL_TO = your_email@gmail.com
     ```
   - Add all variables from `env.example`

4. **Install Dependencies**
   - Replit auto-detects `requirements.txt`
   - Or run: `pip install -r requirements.txt`

5. **Run the Bot**
   - Click "Run" button
   - Bot starts automatically

6. **Keep It Alive (Free Tier)**
   - Sign up for [UptimeRobot](https://uptimerobot.com) (free)
   - Add a monitor pointing to your Repl URL
   - Set to ping every 5 minutes
   - This prevents the Repl from sleeping

7. **Upgrade (Optional)**
   - Replit "Always On" costs ~$7/month
   - Prevents sleeping without UptimeRobot

---

### Option 2: Railway (Recommended) ⭐⭐

**$5/month, very reliable**

#### Pros:
- ✅ Very reliable (99.9% uptime)
- ✅ Easy deployment from GitHub
- ✅ Automatic restarts
- ✅ Free $5 credit monthly
- ✅ Simple environment variable setup

#### Cons:
- ⚠️ Costs $5/month after free credit

#### Setup Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Python

3. **Set Environment Variables**
   - Go to "Variables" tab
   - Add all variables from `env.example`

4. **Configure Start Command**
   - In "Settings" → "Deploy"
   - Set start command: `python bot.py`

5. **Deploy**
   - Railway automatically deploys
   - Bot runs 24/7!

---

### Option 3: Render (Free Tier Available)

**Free tier with limitations**

#### Pros:
- ✅ Free tier available
- ✅ Easy GitHub integration
- ✅ Automatic deployments

#### Cons:
- ⚠️ Free tier sleeps after 15 minutes inactivity
- ⚠️ Slow cold starts

#### Setup Steps:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Set:
     - **Name**: trading-bot
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python bot.py`

3. **Set Environment Variables**
   - Go to "Environment" tab
   - Add all variables from `env.example`

4. **Deploy**
   - Click "Create Web Service"
   - Render deploys automatically

5. **Keep Free Tier Alive**
   - Use [UptimeRobot](https://uptimerobot.com) to ping every 5 minutes

---

### Option 4: DigitalOcean App Platform

**$5/month, professional**

#### Pros:
- ✅ Very reliable
- ✅ Professional infrastructure
- ✅ Easy scaling

#### Cons:
- ⚠️ Costs $5/month minimum

#### Setup Steps:

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Sign up

2. **Create App**
   - Go to "Apps" → "Create App"
   - Connect GitHub repository
   - Select your repo

3. **Configure**
   - Set environment: Python
   - Add environment variables from `env.example`
   - Set run command: `python bot.py`

4. **Deploy**
   - Click "Create Resources"
   - App deploys automatically

---

### Option 5: AWS EC2 / Google Cloud / Azure

**For advanced users**

#### Pros:
- ✅ Full control
- ✅ Very reliable
- ✅ Scalable

#### Cons:
- ⚠️ More complex setup
- ⚠️ Requires technical knowledge
- ⚠️ Costs vary

#### Basic Setup (AWS EC2):

1. **Launch EC2 Instance**
   - Choose Ubuntu Server
   - t2.micro (free tier eligible)

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git -y
   git clone your-repo-url
   cd trading-bot
   pip3 install -r requirements.txt
   ```

4. **Set Environment Variables**
   ```bash
   nano .env
   # Paste all variables from env.example
   ```

5. **Run with PM2 (keeps it running)**
   ```bash
   sudo npm install -g pm2
   pm2 start bot.py --interpreter python3
   pm2 save
   pm2 startup  # Follow instructions
   ```

---

### Option 6: Raspberry Pi (At Home)

**One-time cost, runs at home**

#### Pros:
- ✅ One-time purchase (~$50)
- ✅ Full control
- ✅ No monthly fees
- ✅ Runs 24/7 at home

#### Cons:
- ⚠️ Requires initial setup
- ⚠️ Needs stable internet
- ⚠️ Power consumption

#### Setup Steps:

1. **Buy Raspberry Pi 4** (~$50)
   - 4GB RAM minimum
   - MicroSD card (32GB+)
   - Power supply

2. **Install Raspberry Pi OS**
   - Download from [raspberrypi.org](https://raspberrypi.org)
   - Flash to SD card
   - Boot Raspberry Pi

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git -y
   git clone your-repo-url
   cd trading-bot
   pip3 install -r requirements.txt
   ```

4. **Set Environment Variables**
   ```bash
   nano .env
   # Paste all variables
   ```

5. **Run with systemd (auto-start)**
   ```bash
   sudo nano /etc/systemd/system/trading-bot.service
   ```
   
   Add:
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

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] All sensitive data is in `.env` file (not in code)
- [ ] `.env` is in `.gitignore` (not committed to GitHub)
- [ ] `env.example` is committed (template for others)
- [ ] `config.py` reads from environment variables
- [ ] Test locally first: `python bot.py --test-alerts`
- [ ] All dependencies are in `requirements.txt`

---

## 🔐 Security Best Practices

### For Cloud Deployment:

1. **Never commit `.env` file**
   - Already in `.gitignore`
   - Double-check before pushing

2. **Use Environment Variables**
   - All cloud platforms support this
   - More secure than hardcoded values

3. **Rotate API Keys Regularly**
   - Change Telegram bot token monthly
   - Rotate Resend API key quarterly

4. **Monitor Access**
   - Check logs regularly
   - Set up alerts for unusual activity

---

## 🧪 Testing After Deployment

After deploying, test:

```bash
# Test notifications
python bot.py --test-alerts

# Test portfolio check
python bot.py --test

# Verify it's running
# Check logs or dashboard
```

---

## 📊 Monitoring Your Bot

### Check if Bot is Running:

1. **Replit**: Check "Logs" tab
2. **Railway**: Check "Deployments" → "Logs"
3. **Render**: Check "Logs" tab
4. **AWS/Cloud**: SSH and check `pm2 logs` or `systemctl status`

### Check Bot Activity:

- Look at `trading_bot.log` file
- Check Telegram for test alerts
- Verify daily summaries are sent

---

## 🔄 Updating Your Bot

### After Making Changes:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Update bot"
   git push
   ```

2. **Cloud Platform Auto-Deploys**
   - Most platforms auto-deploy on push
   - Or manually trigger deployment

3. **Verify Update**
   - Check logs
   - Test notifications

---

## 💰 Cost Comparison

| Platform | Monthly Cost | Free Tier | Reliability |
|----------|-------------|-----------|-------------|
| Replit | $0-7 | ✅ Yes | ⭐⭐⭐ |
| Railway | $5 | ✅ $5 credit | ⭐⭐⭐⭐⭐ |
| Render | $0-7 | ✅ Yes (sleeps) | ⭐⭐⭐ |
| DigitalOcean | $5+ | ❌ No | ⭐⭐⭐⭐⭐ |
| AWS EC2 | $0-10 | ✅ Free tier | ⭐⭐⭐⭐⭐ |
| Raspberry Pi | $0 | ✅ One-time $50 | ⭐⭐⭐⭐ |

---

## 🎯 Recommended Setup

**For Beginners:**
→ **Replit** (free) + UptimeRobot (free) = $0/month

**For Reliability:**
→ **Railway** ($5/month) = Best balance

**For Advanced Users:**
→ **AWS EC2** (free tier) or **Raspberry Pi** = Full control

---

## ❓ Troubleshooting

### Bot Stops Running:

1. **Check logs** on your platform
2. **Verify environment variables** are set correctly
3. **Check internet connection** (cloud should be fine)
4. **Restart the service** (platform dashboard)

### Not Receiving Alerts:

1. **Test notifications**: `python bot.py --test-alerts`
2. **Check Telegram** - did you message the bot first?
3. **Verify credentials** in environment variables
4. **Check logs** for error messages

### Platform-Specific Issues:

- **Replit sleeping**: Use UptimeRobot to ping
- **Railway timeout**: Check start command
- **Render cold start**: Upgrade to paid tier
- **AWS costs**: Monitor usage, use free tier limits

---

## 📞 Need Help?

1. Check platform documentation
2. Review bot logs
3. Test locally first
4. Check GitHub Issues

---

**Your bot will run 24/7 once deployed to any of these platforms! 🚀**

