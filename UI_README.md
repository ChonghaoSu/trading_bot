# 🌐 Trading Bot Web UI

Beautiful web interface to manage your trading bot settings without editing code files!

## 🚀 Quick Start

### 1. Install Flask (if not already installed)

```powershell
pip install flask
```

Or install all requirements:

```powershell
pip install -r requirements.txt
```

### 2. Start the Web UI

```powershell
python app.py
```

### 3. Open in Browser

Open your web browser and go to:

**http://localhost:5000**

You'll see a beautiful control panel with three tabs:

- **📊 Holdings** - Manage your portfolio positions
- **👀 Watchlist** - Add/remove stocks to scan for buy signals
- **⚙️ Settings** - Configure email and strategy parameters

---

## 📋 Features

### Holdings Management
- ✅ View all your current holdings in a clean table
- ✅ Add new positions (symbol, shares, avg cost)
- ✅ Delete holdings you've sold
- ✅ Automatic calculation of total position value

### Watchlist Management
- ✅ View all stocks being scanned for buy opportunities
- ✅ Add new symbols to watchlist
- ✅ Remove symbols you no longer want to track
- ✅ Visual grid layout for easy browsing

### Settings Configuration
- ✅ **Email Settings**: Update your email addresses
- ✅ **Alert Thresholds**: 
  - Hard Stop Loss multiplier
  - Early Warning multiplier
  - Profit Target multiplier
- ✅ **Buy Signal Criteria**:
  - Pullback percentage from 52-week high
  - Maximum RSI threshold

---

## 🎨 UI Features

- **Modern Design** - Clean, professional interface
- **Responsive** - Works on desktop, tablet, and mobile
- **Real-time Updates** - Changes save immediately
- **Toast Notifications** - Visual feedback for all actions
- **Tab Navigation** - Easy switching between sections

---

## 📝 Usage Examples

### Adding a New Holding

1. Go to **📊 Holdings** tab
2. Fill in the form:
   - **Stock Symbol**: `AAPL`
   - **Shares**: `10`
   - **Avg Cost**: `150.00`
3. Click **Add Holding**
4. ✅ Done! The stock appears in your table

### Adding to Watchlist

1. Go to **👀 Watchlist** tab
2. Enter a stock symbol (e.g., `MSFT`)
3. Click **Add Symbol**
4. ✅ The symbol is added to your watchlist

### Changing Strategy Parameters

1. Go to **⚙️ Settings** tab
2. Scroll to **Alert Thresholds**
3. Adjust any multiplier (e.g., change Hard Stop from `0.91` to `0.90`)
4. Click **Save Strategy Settings**
5. ✅ Your bot will use the new thresholds

### Updating Email

1. Go to **⚙️ Settings** tab
2. Scroll to **Email Settings**
3. Update your email addresses
4. Click **Save Email Settings**
5. ✅ New alerts will go to the updated email

---

## 🔧 Technical Details

### Files Created

- `app.py` - Flask web server
- `templates/index.html` - Main UI template
- `static/style.css` - Modern styling
- `static/script.js` - Interactive JavaScript

### How It Works

1. **Reads** your existing `portfolio.py` and `config.py` files
2. **Parses** the data using regex patterns
3. **Displays** everything in a user-friendly interface
4. **Saves** changes back to the original files when you submit forms

### Data Safety

- ✅ All changes are written directly to your files
- ✅ Original file structure is preserved
- ✅ Comments and formatting are maintained
- ✅ Always backup before making major changes

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```powershell
pip install flask
```

### "Port 5000 already in use"

**Solution:** Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Changes not saving

**Check:**
1. Make sure `portfolio.py` and `config.py` are in the same directory as `app.py`
2. Check file permissions (should be writable)
3. Look at the terminal for error messages

### UI looks broken

**Solution:**
1. Make sure `templates/` and `static/` folders exist
2. Check that `index.html`, `style.css`, and `script.js` are in the right places
3. Hard refresh your browser (Ctrl+F5)

---

## 💡 Tips

1. **Keep UI Open**: Leave the web UI running in a browser tab for quick access
2. **Run Bot Separately**: The UI and bot can run at the same time
3. **Backup First**: Always backup `portfolio.py` and `config.py` before major changes
4. **Test Changes**: After updating settings, test with `python bot.py --test`

---

## 🔐 Security Note

The web UI runs on `localhost:5000` by default, which means:
- ✅ Only accessible from your computer
- ✅ Safe for local use
- ⚠️ If deploying to cloud, add authentication!

For cloud deployment, add password protection or use a VPN.

---

## 🎯 Next Steps

1. **Start the UI**: `python app.py`
2. **Open browser**: http://localhost:5000
3. **Add your holdings** if not already in `portfolio.py`
4. **Customize watchlist** with stocks you want to track
5. **Adjust thresholds** to match your risk tolerance

---

**Enjoy your beautiful trading bot control panel! 🚀**

