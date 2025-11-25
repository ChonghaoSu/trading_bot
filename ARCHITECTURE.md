# 🏗️ Project Architecture

Understanding how the Trading Alert Bot works under the hood.

---

## 📁 File Structure

```
trading-bot/
│
├── bot.py                  # 🎯 Main orchestrator - scheduler & market hours logic
├── rules.py               # 📊 Trading rules engine - evaluates all alert conditions
├── alerts.py              # 📢 Notification system - sends Telegram & email alerts
├── portfolio.py           # 💼 Your holdings & watchlist data
├── config.py              # ⚙️ Configuration & credentials (DO NOT COMMIT!)
│
├── requirements.txt       # 📦 Python package dependencies
├── README.md              # 📖 Full documentation
├── QUICKSTART.md          # 🚀 5-minute setup guide
├── ARCHITECTURE.md        # 🏗️ This file - system design
│
├── setup.ps1              # 🪟 Windows setup script
├── setup.sh               # 🍎 Mac/Linux setup script
├── config.example.py      # 📋 Config template (safe to commit)
├── .gitignore             # 🔒 Protects sensitive files
│
└── trading_bot.log        # 📝 Activity log (auto-generated)
```

---

## 🔄 System Flow

```
┌─────────────────────────────────────────────────────────┐
│                      BOT.PY                              │
│                  (Main Orchestrator)                     │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  1. Check if market is open (9:30am-4pm ET)      │  │
│  │  2. Skip weekends & holidays                     │  │
│  │  3. Run checks every 5 minutes                   │  │
│  │  4. Send daily summary at 5pm ET                 │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    RULES.PY                              │
│                (Trading Rules Engine)                    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  For each stock in portfolio:                    │  │
│  │                                                   │  │
│  │  ✓ Fetch current price (yfinance)                │  │
│  │  ✓ Calculate technical indicators                │  │
│  │  ✓ Check Rule 1: Hard stop (≤ 9% loss)          │  │
│  │  ✓ Check Rule 2: Warning (≤ 5% loss)            │  │
│  │  ✓ Check Rule 3: Profit target (≥ 30% gain)     │  │
│  │  ✓ Check Rule 4: 200-day SMA breach (Fridays)   │  │
│  │                                                   │  │
│  │  For each symbol in watchlist:                   │  │
│  │                                                   │  │
│  │  ✓ Check Rule 5: Momentum + pullback signal     │  │
│  │                                                   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ (when rule breached)
┌─────────────────────────────────────────────────────────┐
│                   ALERTS.PY                              │
│                (Notification System)                     │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Format alert message                            │  │
│  │      │                                            │  │
│  │      ├─► Send to Telegram (primary)              │  │
│  │      │    └─► POST to Telegram Bot API           │  │
│  │      │                                            │  │
│  │      └─► Send via Email (fallback)               │  │
│  │           └─► POST to Resend API                 │  │
│  │                                                   │  │
│  │  📱 YOU GET NOTIFIED! 🔔                         │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Details

### 1️⃣ **bot.py** - Main Application

**Responsibilities:**
- Scheduler management (runs every 5 minutes)
- Market hours detection (9:30 AM - 4:00 PM ET)
- Weekend & holiday filtering
- Daily summary trigger (5:00 PM ET)
- Logging & error handling

**Key Functions:**
- `is_market_hours()` - Checks if trading is currently active
- `check_portfolio()` - Main job that runs every 5 minutes
- `send_daily_summary()` - Sends 5pm portfolio report
- `run()` - Infinite loop with schedule checking

**Libraries Used:**
- `schedule` - Job scheduling
- `pytz` - Timezone handling (Eastern Time)
- `datetime` - Date/time operations

---

### 2️⃣ **rules.py** - Trading Rules Engine

**Responsibilities:**
- Fetch stock data from Yahoo Finance
- Calculate technical indicators (SMA, RSI)
- Evaluate all 5 alert rules
- Track which alerts already fired (prevent spam)
- Generate daily summary reports

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `get_stock_data()` | Fetch historical prices from yfinance |
| `calculate_sma()` | Simple Moving Average calculation |
| `calculate_rsi()` | Relative Strength Index (14-period) |
| `check_hard_stop()` | Rule 1: Critical 9% loss alert |
| `check_warning()` | Rule 2: 5% loss early warning |
| `check_profit_target()` | Rule 3: 30% gain profit-taking |
| `check_sma_200_breach()` | Rule 4: 200-day MA breach (Fridays) |
| `check_momentum_pullback()` | Rule 5: Buy signal detection |
| `evaluate_portfolio()` | Check all rules for all holdings |
| `generate_daily_summary()` | Create formatted portfolio report |

**Alert Deduplication:**
- Tracks fired alerts in `triggered_alerts` dictionary
- Prevents duplicate notifications for same condition
- Resets recommendation alerts daily

---

### 3️⃣ **alerts.py** - Notification System

**Responsibilities:**
- Send Telegram messages via Bot API
- Send emails via Resend API
- Format alert messages
- Handle API errors gracefully
- Provide test functions

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `send_telegram()` | POST to Telegram Bot API |
| `send_email()` | POST to Resend Email API |
| `send_alert()` | Send via both channels |
| `send_hard_stop_alert()` | Formatted critical alert |
| `send_warning_alert()` | Formatted warning message |
| `send_profit_alert()` | Formatted profit-taking alert |
| `send_sma_breach_alert()` | Formatted SMA breach message |
| `send_recommendation()` | Formatted buy signal |
| `send_daily_summary()` | Formatted portfolio report |

**API Integrations:**

**Telegram Bot API:**
```python
POST https://api.telegram.org/bot{token}/sendMessage
{
  "chat_id": "123456789",
  "text": "Alert message",
  "parse_mode": "HTML"
}
```

**Resend Email API:**
```python
POST https://api.resend.com/emails
Headers: {"Authorization": "Bearer {api_key}"}
{
  "from": "alerts@yourdomain.com",
  "to": ["you@email.com"],
  "subject": "Trading Alert",
  "html": "<pre>Alert message</pre>"
}
```

---

### 4️⃣ **portfolio.py** - Data Layer

**Responsibilities:**
- Store your current holdings
- Define watchlist for scanning
- Calculate portfolio metrics
- Format currency & percentages

**Data Structure:**
```python
holdings = [
    {
        "symbol": "AAPL",     # Stock ticker
        "shares": 10,          # Number of shares (can be fractional)
        "avg_cost": 150.00     # Your average cost per share
    },
    # ... more holdings
]
```

**Helper Functions:**
- `get_portfolio_value()` - Calculate total P&L
- `format_currency()` - Format as USD ($1,234.56)
- `format_percent()` - Format as percentage (+12.34%)

---

### 5️⃣ **config.py** - Configuration

**Categories:**

1. **Credentials** (sensitive - never commit!)
   - Telegram Bot Token
   - Telegram Chat ID
   - Resend API Key
   - Email addresses

2. **Schedule Settings**
   - Market hours (9:30 AM - 4:00 PM ET)
   - Check interval (5 minutes)
   - Daily summary time (5:00 PM ET)

3. **Alert Thresholds**
   - Hard stop: 0.91 (9% loss)
   - Warning: 0.95 (5% loss)
   - Profit target: 1.30 (30% gain)
   - Pullback: 8%
   - RSI max: 65

4. **Logging Settings**
   - Log file path
   - Console/file flags

5. **Market Holidays**
   - US stock market closure dates

---

## 🔐 Security & Best Practices

### Credential Protection

1. **Never commit `config.py`** with real credentials
2. Use `.gitignore` to exclude sensitive files
3. Provide `config.example.py` as a template
4. For cloud deployments, use environment variables:

```python
import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

### Error Handling

- All API calls wrapped in try-except blocks
- Graceful degradation (skip if one stock fails)
- Detailed logging for troubleshooting
- Fallback email if Telegram fails

### Rate Limiting

- yfinance sometimes throttles requests
- 5-minute interval prevents excessive API calls
- Alert deduplication prevents spam

---

## 📊 Data Flow Diagram

```
START
  │
  ├─► Is it a weekday? ──► NO ──► Sleep until next check
  │         │
  │        YES
  │         │
  ├─► Is it a holiday? ──► YES ──► Sleep until next check
  │         │
  │         NO
  │         │
  ├─► Is it 9:30am-4pm ET? ──► NO ──► Sleep until next check
  │         │
  │        YES
  │         │
  ├─► [FETCH] Get current prices from yfinance
  │         │
  │         ├─► For each holding in portfolio:
  │         │     │
  │         │     ├─► Calculate P&L %
  │         │     │
  │         │     ├─► Is price ≤ avg_cost × 0.91?
  │         │     │    └─► YES ──► Send HARD STOP alert 🔴
  │         │     │
  │         │     ├─► Is price ≤ avg_cost × 0.95?
  │         │     │    └─► YES ──► Send WARNING alert ⚠️
  │         │     │
  │         │     ├─► Is price ≥ avg_cost × 1.30?
  │         │     │    └─► YES ──► Send PROFIT alert 🎯
  │         │     │
  │         │     └─► (If Friday after 4pm) Check 200-day SMA
  │         │          └─► Breached? ──► Send SMA BREACH alert 📉
  │         │
  │         └─► Optional: Scan watchlist for buy signals
  │                │
  │                └─► For each symbol:
  │                      │
  │                      ├─► Is price > 50-day SMA?
  │                      ├─► Is pullback ≥ 8% from 52-week high?
  │                      ├─► Is RSI < 65?
  │                      │
  │                      └─► ALL YES? ──► Send BUY SIGNAL alert 💡
  │
  ├─► Is it 5:00 PM ET? ──► YES ──► Generate & send daily summary 📊
  │
  └─► Sleep 5 minutes ──► REPEAT
```

---

## 🧪 Testing Strategy

### 1. Test Notifications
```bash
python bot.py --test-alerts
```
Verifies Telegram and email are working.

### 2. Test Portfolio Check
```bash
python bot.py --test
```
Runs a single check ignoring market hours.

### 3. Test Summary Generation
```bash
python bot.py --summary
```
Generates portfolio summary without sending.

### 4. Test Buy Signals
```bash
python bot.py --scan
```
Scans watchlist for opportunities.

### 5. Testing Mode
Set in `config.py`:
```python
TESTING_MODE = True
```
Bypasses market hours check for development.

---

## 🚀 Deployment Options

### Option 1: Local Computer
**Pros:** Free, full control  
**Cons:** Must keep computer on

```bash
python bot.py
```

### Option 2: Replit (Cloud)
**Pros:** 24/7 uptime, free tier  
**Cons:** May sleep after inactivity

1. Import GitHub repo to Replit
2. Set secrets in Replit environment
3. Use UptimeRobot to keep it alive

### Option 3: AWS/DigitalOcean
**Pros:** Professional, reliable  
**Cons:** Costs $5-10/month

```bash
# On Linux server:
nohup python3 bot.py &
```

### Option 4: Docker Container
**Pros:** Portable, reproducible  
**Cons:** Requires Docker knowledge

```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
```

---

## 🔧 Customization Guide

### Add a New Alert Rule

**Step 1:** Define rule in `rules.py`
```python
def check_volume_spike(self, symbol: str) -> bool:
    """Alert when volume is 2x average"""
    data = self.get_stock_data(symbol, period="1mo")
    
    current_volume = data['Volume'].iloc[-1]
    avg_volume = data['Volume'].mean()
    
    if current_volume > avg_volume * 2:
        self.alert_system.send_alert(
            f"Volume Spike: {symbol} - {current_volume:,.0f} vs avg {avg_volume:,.0f}"
        )
        return True
    return False
```

**Step 2:** Call it in `evaluate_portfolio()`
```python
def evaluate_portfolio(self, holdings):
    for holding in holdings:
        # ... existing checks
        self.check_volume_spike(holding["symbol"])
```

### Change Alert Thresholds

Edit `config.py`:
```python
HARD_STOP_MULTIPLIER = 0.88   # Change to 12% loss
PROFIT_TARGET_MULTIPLIER = 1.50  # Change to 50% gain
```

### Add Custom Notification Channel

**Step 1:** Create new function in `alerts.py`
```python
def send_discord(self, message: str) -> bool:
    """Send message to Discord webhook"""
    webhook_url = config.DISCORD_WEBHOOK_URL
    payload = {"content": message}
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 204
```

**Step 2:** Call it in `send_alert()`
```python
def send_alert(self, message: str, subject=None):
    self.send_telegram(message)
    self.send_email(subject, message)
    self.send_discord(message)  # Add this
```

---

## 📚 Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.8+ | Core application |
| Scheduler | `schedule` | Run jobs every 5 minutes |
| Market Data | `yfinance` | Free stock prices & history |
| Notifications | Telegram Bot API | Primary alerts |
| Email | Resend API | Fallback alerts |
| Data Processing | `pandas` | Technical indicators |
| Timezone | `pytz` | Eastern Time handling |
| HTTP Requests | `requests` | API communications |

---

## 🐛 Common Issues & Solutions

### Issue: "yfinance returns None"
**Cause:** Yahoo Finance rate limiting or invalid ticker  
**Solution:** Wait a few minutes, verify ticker symbol

### Issue: "Telegram API 401 Unauthorized"
**Cause:** Invalid bot token or chat ID  
**Solution:** Double-check credentials, message bot once first

### Issue: "Bot doesn't run during market hours"
**Cause:** Timezone mismatch or incorrect market hours  
**Solution:** Verify system time, check `config.py` settings

### Issue: "Multiple alerts for same condition"
**Cause:** Alert deduplication not working  
**Solution:** Check `triggered_alerts` dict in `rules.py`

---

## 📈 Performance Considerations

**API Call Limits:**
- yfinance: ~2,000 requests/hour
- Telegram: 30 messages/second
- Resend: 100 emails/day (free tier)

**Optimization Tips:**
1. Fetch data once per interval, not per rule
2. Cache technical indicators between checks
3. Use batch API calls when possible
4. Implement exponential backoff for rate limits

---

## 🔮 Future Enhancements

**Potential Features:**
- [ ] Web dashboard with portfolio visualization
- [ ] Backtesting framework for strategy validation
- [ ] Support for multiple portfolios
- [ ] Integration with broker APIs for auto-execution
- [ ] Machine learning price predictions
- [ ] Sentiment analysis from news/Twitter
- [ ] Options tracking & Greeks monitoring
- [ ] Portfolio optimization suggestions

---

## 📞 Contributing

Want to improve the bot? Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

**Code Style:**
- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include comments for complex logic
- Keep functions under 50 lines when possible

---

**Built with ❤️ for smart traders who want to stay informed without watching charts all day.**

