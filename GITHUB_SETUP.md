# 📦 GitHub Setup Guide

Prepare your trading bot codebase for GitHub deployment.

---

## ✅ Pre-Upload Checklist

Before uploading to GitHub, ensure:

- [ ] All sensitive data removed from code
- [ ] `.env` file is in `.gitignore`
- [ ] `env.example` template is included
- [ ] `config.py` uses environment variables
- [ ] No API keys or tokens in code
- [ ] Log files are in `.gitignore`

---

## 🔐 Step 1: Secure Your Credentials

### Current Status Check:

Your `config.py` currently has hardcoded credentials. This is OK for local use, but for GitHub:

1. **Option A: Use .env file (Recommended)**
   - Create `.env` file from `env.example`
   - Fill in your actual credentials
   - `config.py` will automatically read from `.env`
   - `.env` is already in `.gitignore` ✅

2. **Option B: Keep config.py local only**
   - `config.py` is already in `.gitignore` ✅
   - Don't commit it to GitHub
   - Others will use `env.example` template

---

## 📝 Step 2: Create .env File (If Not Exists)

```powershell
# Copy the example file
Copy-Item env.example .env

# Edit .env with your actual credentials
# Use any text editor
```

Fill in your actual values in `.env`:
```env
TELEGRAM_BOT_TOKEN=your_actual_token_here
TELEGRAM_CHAT_ID=your_actual_chat_id_here
RESEND_API_KEY=your_actual_key_here
EMAIL_FROM=your-email@domain.com
EMAIL_TO=your-email@gmail.com
```

---

## 🚫 Step 3: Verify .gitignore

Check that `.gitignore` includes:

```
.env
.env.local
config.py  # Optional - if you want to keep it private
*.log
trading_bot.log
```

---

## 📤 Step 4: Initialize Git Repository

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Check what will be committed (verify no secrets!)
git status

# Commit
git commit -m "Initial commit: Trading Alert Bot"

# Create GitHub repository (on github.com)
# Then connect:
git remote add origin https://github.com/yourusername/trading-bot.git
git branch -M main
git push -u origin main
```

---

## 🔍 Step 5: Verify Nothing Sensitive is Committed

Before pushing, check:

```powershell
# See what files will be committed
git status

# Search for any hardcoded tokens (if config.py is tracked)
git diff | Select-String -Pattern "8202402702|re_4ysnWD1w"
```

**If you see your actual tokens**, they're in the commit. Options:

1. **Remove config.py from tracking:**
   ```powershell
   git rm --cached config.py
   git commit -m "Remove config.py from tracking"
   ```

2. **Or use .env file instead** (recommended)

---

## 📋 Step 6: Files That SHOULD Be Committed

✅ **Safe to commit:**
- `bot.py`
- `rules.py`
- `alerts.py`
- `portfolio.py` (your holdings - you may want to anonymize)
- `app.py` (web UI)
- `requirements.txt`
- `README.md`
- `env.example` (template, no real secrets)
- `config.example.py` (template)
- All documentation files
- `templates/` and `static/` folders

❌ **Never commit:**
- `.env` (your actual credentials)
- `config.py` (if it has real credentials)
- `*.log` files
- `__pycache__/`
- `venv/` or `env/`

---

## 🔄 Step 7: For Others Using Your Repo

When someone clones your repo, they should:

1. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/trading-bot.git
   cd trading-bot
   ```

2. **Create .env file:**
   ```bash
   cp env.example .env
   # Edit .env with their credentials
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the bot:**
   ```bash
   python bot.py
   ```

---

## 🛡️ Step 8: If You Accidentally Committed Secrets

**If you already pushed secrets to GitHub:**

1. **Rotate all API keys immediately:**
   - Create new Telegram bot token
   - Generate new Resend API key
   - Update your `.env` file

2. **Remove from Git history:**
   ```powershell
   # Remove file from history
   git filter-branch --force --index-filter `
     "git rm --cached --ignore-unmatch config.py" `
     --prune-empty --tag-name-filter cat -- --all

   # Force push (WARNING: rewrites history)
   git push origin --force --all
   ```

3. **Or create new repository:**
   - Start fresh
   - Don't commit secrets this time

---

## 📝 Step 9: Update README for GitHub

Your README should include:

1. **Installation instructions**
2. **Environment setup** (using `env.example`)
3. **Deployment guide** (link to DEPLOYMENT.md)
4. **Contributing guidelines** (optional)

---

## ✅ Final Verification

Before making repository public:

```powershell
# Check what's tracked
git ls-files

# Verify no secrets
git grep -i "token\|api_key\|password" -- :!*.md :!*.example :!env.example

# If you see actual secrets, remove them before pushing!
```

---

## 🎯 Quick Start for New Users

Add this to your README:

```markdown
## Quick Start

1. Clone this repository
2. Copy `env.example` to `.env`
3. Fill in your credentials in `.env`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python bot.py`

See [DEPLOYMENT.md](DEPLOYMENT.md) for 24/7 deployment options.
```

---

## 🔗 Repository Structure

Your GitHub repo should look like:

```
trading-bot/
├── .gitignore          ✅ (protects secrets)
├── env.example         ✅ (template for others)
├── config.example.py   ✅ (template)
├── requirements.txt    ✅
├── README.md          ✅
├── DEPLOYMENT.md      ✅
├── bot.py             ✅
├── rules.py           ✅
├── alerts.py          ✅
├── portfolio.py       ✅ (consider anonymizing)
├── app.py             ✅
├── templates/         ✅
├── static/            ✅
└── .env               ❌ (NOT committed - in .gitignore)
```

---

## 🚀 You're Ready!

Once everything is set up:

1. ✅ All secrets are in `.env` (not committed)
2. ✅ `env.example` provides template
3. ✅ `.gitignore` protects sensitive files
4. ✅ Code is ready for GitHub

**Push to GitHub and deploy to cloud for 24/7 operation!**

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options.

