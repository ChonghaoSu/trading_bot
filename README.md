# 🤖 Trading Alert Bot

A **lightweight, alert-only** trading bot that monitors your Robinhood portfolio and instantly notifies you via **Telegram** and **Email** when pre-defined sell rules are breached or buy opportunities arise.

## 🚀 Quick Deploy

**Want to run 24/7?** See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for 5-minute setup.

**Preparing for GitHub?** See [GITHUB_SETUP.md](GITHUB_SETUP.md) for secure setup.

**Deployment options:** See [DEPLOYMENT.md](DEPLOYMENT.md) for all platforms.

## ✨ Features

- 🔔 **Instant Alerts** - Get notified immediately via Telegram and email
- 📊 **Portfolio Monitoring** - Tracks all your holdings every 5 minutes during market hours
- 🛡️ **Risk Management** - Hard stop losses, early warnings, and profit targets
- 📈 **Buy Signals** - Identifies momentum + pullback opportunities
- 📱 **Daily Summary** - Receive a portfolio snapshot at 5pm ET
- 🆓 **100% Free** - Uses free APIs only (yfinance, Telegram, Resend)
- 🧹 **Clean Code** - Well-commented and easy to customize

## 🚨 Alert Rules

| Rule | Condition | Action |
|------|-----------|--------|
| **Hard Stop** | Price ≤ avg_cost × 0.91 | 🔴 SELL 100% NOW |
| **Early Warning** | Price ≤ avg_cost × 0.95 | ⚠️ Prepare to sell |
| **Profit Target** | Price ≥ avg_cost × 1.30 | 🎯 Consider selling 60-75% |
| **200-Day SMA Breach** | Weekly close below 200-MA (Fridays) | 📉 Sell Monday |
| **Buy Signal** | Price > 50-MA + 8% pullback + RSI < 65 | 💡 Consider buying |

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Internet connection
- Telegram account
- Email account (for Resend API)

---

### 🪟 Windows Setup

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation

2. **Download the bot**
   ```powershell
   cd Desktop
   git clone <your-repo-url>
   cd trading-bot
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure credentials** (see Configuration section below)

5. **Run the bot**
   ```powershell
   python bot.py
   ```

---

### 🍎 Mac Setup

1. **Install Python** (if not already installed)
   ```bash
   # Check if Python is installed
   python3 --version
   
   # If not, install via Homebrew
   brew install python3
   ```

2. **Download the bot**
   ```bash
   cd ~/Desktop
   git clone <your-repo-url>
   cd trading-bot
   ```

3. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Configure credentials** (see Configuration section below)

5. **Run the bot**
   ```bash
   python3 bot.py
   ```

---

### 🌐 Replit Setup

1. **Create a new Repl**
   - Go to [replit.com](https://replit.com)
   - Click "Create Repl"
   - Select "Import from GitHub" and paste your repo URL
   - Or create a blank Python repl and upload files

2. **Install dependencies**
   - Replit auto-detects `requirements.txt`
   - Or manually run: `pip install -r requirements.txt`

3. **Configure credentials**
   - Click on "Secrets" (lock icon in sidebar)
   - Add your Telegram and email credentials as environment variables
   - Update `config.py` to read from environment variables:
   
   ```python
   import os
   TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TOKEN")
   TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")
   # ... etc
   ```

4. **Run the bot**
   - Click the "Run" button
   - Or use Shell: `python bot.py`

5. **Keep it running 24/7** (optional)
   - Use [UptimeRobot](https://uptimerobot.com) to ping your Repl
   - Or upgrade to Replit's "Always On" feature

---

## ⚙️ Configuration

### Step 1: Get Telegram Credentials

1. **Create a Telegram Bot**
   - Open Telegram and message [@BotFather](https://t.me/BotFather)
   - Send `/newbot` command
   - Follow prompts to name your bot
   - Copy the API token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Your Chat ID**
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram
   - Copy your chat ID (looks like `123456789`)

3. **Update config.py**
   ```python
   TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
   TELEGRAM_CHAT_ID = "123456789"
   ```

### Step 2: Get Resend Email API Key

1. **Sign up for Resend**
   - Go to [resend.com](https://resend.com)
   - Create a free account (100 emails/day limit)

2. **Create API Key**
   - Go to "API Keys" in dashboard
   - Click "Create API Key"
   - Copy the key (starts with `re_`)

3. **Configure Email**
   - Add and verify your sending domain
   - Or use their test domain for testing

4. **Update config.py**
   ```python
   RESEND_API_KEY = "re_YourAPIKeyHere"
   EMAIL_FROM = "alerts@yourdomain.com"
   EMAIL_TO = "your-email@gmail.com"
   ```

### Step 3: Update Your Portfolio

Edit `portfolio.py` to match your holdings:

```python
holdings = [
    {"symbol": "AAPL", "shares": 10, "avg_cost": 150.00},
    {"symbol": "TSLA", "shares": 5, "avg_cost": 200.00},
    # Add all your positions here
]
```

### Step 4: Customize Alert Rules (Optional)

Edit thresholds in `config.py`:

```python
HARD_STOP_MULTIPLIER = 0.91      # 9% loss
WARNING_MULTIPLIER = 0.95         # 5% loss
PROFIT_TARGET_MULTIPLIER = 1.30   # 30% gain
```

---

## 🚀 Usage

### 🌐 Web UI (Recommended!)

**Beautiful web interface to manage everything without editing code!**

```powershell
# Start the web UI
python app.py

# Or use the helper script
.\start_ui.ps1
```

Then open **http://localhost:5000** in your browser.

**Features:**
- 📊 Manage holdings (add/remove stocks)
- 👀 Edit watchlist (add/remove symbols to scan)
- ⚙️ Change strategy parameters
- 📧 Update email settings

See [UI_README.md](UI_README.md) for full documentation.

---

### Run the Bot Continuously

```bash
python bot.py
```

The bot will:
- Check portfolio every 5 minutes during market hours (9:30 AM - 4:00 PM ET)
- Send alerts when rules are breached
- Send daily summary at 5:00 PM ET
- Automatically skip weekends and holidays

### Test Commands

```bash
# Test a single portfolio check (ignores market hours)
python bot.py --test

# Test Telegram and email notifications
python bot.py --test-alerts

# Verify Telegram setup
python bot.py --verify

# Generate portfolio summary
python bot.py --summary

# Scan watchlist for buy opportunities
python bot.py --scan

# Show help
python bot.py --help
```

---

## 📝 Examples of Alerts

### Hard Stop Alert (Telegram)
```
🚨 TRADING ALERT 🚨
2025-11-24 14:30:15

🔴 HARD STOP TRIGGERED - SELL NOW! 🔴

Symbol: TSLA
Current Price: $367.44
Your Avg Cost: $403.79
Loss: 9.0%

⚠️ ACTION REQUIRED: Sell 100% of position immediately!
```

### Profit Target Alert
```
🎯 PROFIT TARGET HIT - Consider Taking Gains! 🎯

Symbol: NVDA
Current Price: $238.25
Your Avg Cost: $183.27
Gain: +30.0%

💰 Consider selling 60-75% to lock in profits
```

### Daily Summary (5pm ET)
```
📊 DAILY PORTFOLIO SUMMARY
Date: 2025-11-24 17:00:00
==================================================

GOOG   | Price: $165.50 | Value: $112.35 | P&L:  -43.8% | To Stop: 38.3%
SMH    | Price: $210.25 | Value: $188.80 | P&L:  -37.0% | To Stop: 33.5%
META   | Price: $575.00 | Value:  $97.75 | P&L:   -2.0% | To Stop:  7.0%
...

==================================================
TOTAL VALUE:  $1,234.56
TOTAL COST:   $1,500.00
TOTAL P&L:    -$265.44 (-17.70%)
==================================================
```

---

## 🔧 Troubleshooting

### Bot doesn't send alerts

1. **Check credentials**
   ```bash
   python bot.py --test-alerts
   ```

2. **Verify Telegram bot**
   - Make sure you messaged your bot at least once
   - Check that chat ID is correct

3. **Check logs**
   - Look at `trading_bot.log` file for errors

### yfinance data errors

- Yahoo Finance sometimes rate-limits requests
- Wait a few minutes and try again
- Check if ticker symbol is correct

### Bot stops running

- Check for Python errors in console
- Make sure computer doesn't go to sleep
- Consider running on a cloud server or Replit

### Market hours not detected correctly

- Bot uses Eastern Time (ET)
- Check `config.py` market hours settings
- Set `TESTING_MODE = True` to bypass market hours check

---

## 📂 File Structure

```
trading-bot/
│
├── bot.py                  # Main bot application
├── config.py              # Configuration & credentials
├── portfolio.py           # Your holdings & watchlist
├── alerts.py              # Telegram & email notifications
├── rules.py               # Trading rules & technical analysis
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── trading_bot.log        # Activity log (auto-created)
```

---

## 🔒 Security Notes

- **Never commit `config.py` to GitHub** with real credentials
- Add `config.py` to `.gitignore`
- Use environment variables for Replit/cloud deployments
- Rotate API keys regularly

---

## 🎯 Customization Ideas

### Add More Rules

Edit `rules.py` to add custom alert conditions:

```python
def check_volume_spike(self, symbol: str) -> bool:
    """Alert when volume is 2x average"""
    # Your logic here
    pass
```

### Change Notification Format

Edit alert templates in `alerts.py`:

```python
def send_custom_alert(self, data):
    message = f"Custom format: {data}"
    self.send_telegram(message)
```

### Add More Symbols to Watchlist

Edit `portfolio.py`:

```python
watchlist = [
    "AAPL", "MSFT", "GOOGL",
    # Add more symbols here
]
```

---

## 🐛 Known Limitations

- Free yfinance data can be delayed by 15 minutes
- Yahoo Finance sometimes throttles requests
- Email limit: 100/day with free Resend account
- No automatic trade execution (alert-only system)

---

## 📚 Resources

- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Resend Email API](https://resend.com/docs)
- [Python Schedule Library](https://schedule.readthedocs.io/)

---

## 📄 License

This project is for educational purposes only. Not financial advice.

**Use at your own risk.** The author is not responsible for any trading losses.

---

## 🤝 Contributing

Feel free to:
- Report bugs via GitHub Issues
- Submit pull requests for improvements
- Share your customizations

---

## ❓ FAQ

**Q: Will this bot execute trades automatically?**  
A: No, it's alert-only. You make all trading decisions.

**Q: Does it work with brokers other than Robinhood?**  
A: Yes! It uses yfinance for price data, so it works with any portfolio.

**Q: Can I run multiple portfolios?**  
A: Yes, create separate `portfolio.py` files and run multiple bot instances.

**Q: How much does it cost?**  
A: $0. All services used have free tiers.

**Q: Can I backtest strategies?**  
A: Not built-in, but you can use the `rules.py` logic with historical data.

**Q: What if I want to change alert thresholds?**  
A: Edit values in `config.py` and restart the bot.

---

## 📞 Support

If you encounter issues:

1. Check this README first
2. Look at `trading_bot.log` for errors
3. Run `python bot.py --test` to diagnose
4. Create a GitHub Issue with error details

---

**Happy Trading! 🚀📈**

*Remember: Past performance doesn't guarantee future results. Always do your own research.*

