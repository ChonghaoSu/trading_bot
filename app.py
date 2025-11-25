"""
Trading Bot Web UI
Beautiful interface to manage holdings, watchlist, and settings
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
import os
import re
from datetime import datetime
import yfinance as yf

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def read_portfolio_file():
    """Read and parse portfolio.py file"""
    try:
        with open('portfolio.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract holdings
        holdings_match = re.search(r'holdings\s*=\s*\[(.*?)\]', content, re.DOTALL)
        holdings = []
        if holdings_match:
            holdings_text = holdings_match.group(1)
            # Parse each holding
            for match in re.finditer(r'\{"symbol":\s*"([^"]+)",\s*"shares":\s*([\d.]+),\s*"avg_cost":\s*([\d.]+)\}', holdings_text):
                holdings.append({
                    'symbol': match.group(1),
                    'shares': float(match.group(2)),
                    'avg_cost': float(match.group(3))
                })
        
        # Extract watchlist
        watchlist_match = re.search(r'watchlist\s*=\s*\[(.*?)\]', content, re.DOTALL)
        watchlist = []
        if watchlist_match:
            watchlist_text = watchlist_match.group(1)
            # Extract all quoted strings
            for match in re.finditer(r'"([A-Z]+[A-Z0-9]*)"', watchlist_text):
                watchlist.append(match.group(1))
        
        return holdings, watchlist
    except Exception as e:
        print(f"Error reading portfolio.py: {e}")
        return [], []


def write_portfolio_file(holdings, watchlist):
    """Write holdings and watchlist back to portfolio.py"""
    try:
        # Read existing file
        with open('portfolio.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Format holdings
        holdings_str = '[\n'
        for h in holdings:
            holdings_str += f'    {{"symbol": "{h["symbol"]}", "shares": {h["shares"]}, "avg_cost": {h["avg_cost"]}}},\n'
        holdings_str = holdings_str.rstrip(',\n') + '\n]'
        
        # Replace holdings
        content = re.sub(
            r'holdings\s*=\s*\[.*?\]',
            f'holdings = {holdings_str}',
            content,
            flags=re.DOTALL
        )
        
        # Format watchlist
        watchlist_str = '[\n'
        for w in watchlist:
            watchlist_str += f'    "{w}",\n'
        watchlist_str = watchlist_str.rstrip(',\n') + '\n]'
        
        # Replace watchlist
        content = re.sub(
            r'watchlist\s*=\s*\[.*?\]',
            f'watchlist = {watchlist_str}',
            content,
            flags=re.DOTALL
        )
        
        # Write back
        with open('portfolio.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error writing portfolio.py: {e}")
        return False


def read_config_file():
    """Read config.py and extract editable settings"""
    try:
        # Import config module directly to get actual values
        import config as config_module
        
        config = {
            'email_from': getattr(config_module, 'EMAIL_FROM', ''),
            'email_to': getattr(config_module, 'EMAIL_TO', ''),
            'hard_stop': getattr(config_module, 'HARD_STOP_MULTIPLIER', 0.91),
            'warning': getattr(config_module, 'WARNING_MULTIPLIER', 0.95),
            'profit_target': getattr(config_module, 'PROFIT_TARGET_MULTIPLIER', 1.30),
            'pullback': getattr(config_module, 'RECOMMENDATION_PULLBACK_PERCENT', 8.0),
            'rsi_max': getattr(config_module, 'RECOMMENDATION_RSI_MAX', 65),
        }
        
        return config
    except Exception as e:
        print(f"Error reading config.py: {e}")
        # Return defaults if import fails
        return {
            'email_from': '',
            'email_to': '',
            'hard_stop': 0.91,
            'warning': 0.95,
            'profit_target': 1.30,
            'pullback': 8.0,
            'rsi_max': 65,
        }


def write_config_file(config):
    """Write config settings back to config.py (updates default values in get_env calls)"""
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update email settings - match get_env("EMAIL_FROM", "default_value")
        content = re.sub(
            r'EMAIL_FROM\s*=\s*get_env\([^,]+,\s*"[^"]+"',
            f'EMAIL_FROM = get_env("EMAIL_FROM", "{config["email_from"]}"',
            content
        )
        content = re.sub(
            r'EMAIL_TO\s*=\s*get_env\([^,]+,\s*"[^"]+"',
            f'EMAIL_TO = get_env("EMAIL_TO", "{config["email_to"]}"',
            content
        )
        
        # Update strategy parameters - match get_env("KEY", default_value, type_func)
        # Use more specific patterns that match the exact format
        content = re.sub(
            r'HARD_STOP_MULTIPLIER\s*=\s*get_env\([^,]+,\s*[\d.]+',
            f'HARD_STOP_MULTIPLIER = get_env("HARD_STOP_MULTIPLIER", {config["hard_stop"]}',
            content
        )
        content = re.sub(
            r'WARNING_MULTIPLIER\s*=\s*get_env\([^,]+,\s*[\d.]+',
            f'WARNING_MULTIPLIER = get_env("WARNING_MULTIPLIER", {config["warning"]}',
            content
        )
        content = re.sub(
            r'PROFIT_TARGET_MULTIPLIER\s*=\s*get_env\([^,]+,\s*[\d.]+',
            f'PROFIT_TARGET_MULTIPLIER = get_env("PROFIT_TARGET_MULTIPLIER", {config["profit_target"]}',
            content
        )
        content = re.sub(
            r'RECOMMENDATION_PULLBACK_PERCENT\s*=\s*get_env\([^,]+,\s*[\d.]+',
            f'RECOMMENDATION_PULLBACK_PERCENT = get_env("RECOMMENDATION_PULLBACK_PERCENT", {config["pullback"]}',
            content
        )
        content = re.sub(
            r'RECOMMENDATION_RSI_MAX\s*=\s*get_env\([^,]+,\s*[\d.]+',
            f'RECOMMENDATION_RSI_MAX = get_env("RECOMMENDATION_RSI_MAX", {config["rsi_max"]}',
            content
        )
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error writing config.py: {e}")
        return False


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    """Main dashboard"""
    holdings, watchlist = read_portfolio_file()
    config = read_config_file()
    
    return render_template('index.html', 
                         holdings=holdings, 
                         watchlist=watchlist,
                         config=config)


@app.route('/api/holdings', methods=['GET'])
def get_holdings():
    """Get current holdings with real-time prices"""
    holdings, _ = read_portfolio_file()
    
    # Fetch real-time prices for all holdings
    symbols = [h['symbol'] for h in holdings]
    if symbols:
        try:
            # Get current prices
            tickers = yf.Tickers(' '.join(symbols))
            prices = {}
            
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    # Try to get most recent price (may be delayed 15-20 min for free data)
                    # Use '1d' period with '1m' interval for intraday data
                    data = ticker.history(period='1d', interval='1m')
                    if not data.empty:
                        # Get the most recent close price
                        prices[symbol] = float(data['Close'].iloc[-1])
                    else:
                        # Fallback: try daily data
                        data = ticker.history(period='5d', interval='1d')
                        if not data.empty:
                            prices[symbol] = float(data['Close'].iloc[-1])
                        else:
                            # Last resort: try info (may be more delayed)
                            info = ticker.info
                            if 'regularMarketPrice' in info:
                                prices[symbol] = float(info['regularMarketPrice'])
                            elif 'currentPrice' in info:
                                prices[symbol] = float(info['currentPrice'])
                            else:
                                prices[symbol] = None
                except Exception as e:
                    print(f"Error fetching price for {symbol}: {e}")
                    prices[symbol] = None
        except Exception as e:
            print(f"Error fetching prices: {e}")
            prices = {symbol: None for symbol in symbols}
    else:
        prices = {}
    
    # Add real-time data to holdings
    enriched_holdings = []
    for holding in holdings:
        symbol = holding['symbol']
        current_price = prices.get(symbol)
        
        enriched = {
            'symbol': symbol,
            'shares': holding['shares'],
            'avg_cost': holding['avg_cost'],
            'current_price': current_price,
            'cost_basis': holding['shares'] * holding['avg_cost'],
            'current_value': holding['shares'] * current_price if current_price else None,
            'pnl': (holding['shares'] * current_price - holding['shares'] * holding['avg_cost']) if current_price else None,
            'pnl_percent': ((current_price - holding['avg_cost']) / holding['avg_cost'] * 100) if current_price else None
        }
        enriched_holdings.append(enriched)
    
    return jsonify(enriched_holdings)


@app.route('/api/holdings', methods=['POST'])
def add_holding():
    """Add a new holding"""
    data = request.json
    holdings, watchlist = read_portfolio_file()
    
    # Validate
    symbol = data.get('symbol', '').upper().strip()
    shares = float(data.get('shares', 0))
    avg_cost = float(data.get('avg_cost', 0))
    
    if not symbol or shares <= 0 or avg_cost <= 0:
        return jsonify({'success': False, 'error': 'Invalid data'}), 400
    
    # Check if already exists
    if any(h['symbol'] == symbol for h in holdings):
        return jsonify({'success': False, 'error': 'Stock already in holdings'}), 400
    
    # Add
    holdings.append({
        'symbol': symbol,
        'shares': shares,
        'avg_cost': avg_cost
    })
    
    if write_portfolio_file(holdings, watchlist):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to save'}), 500


@app.route('/api/holdings/<symbol>', methods=['DELETE'])
def delete_holding(symbol):
    """Delete a holding"""
    holdings, watchlist = read_portfolio_file()
    holdings = [h for h in holdings if h['symbol'] != symbol.upper()]
    
    if write_portfolio_file(holdings, watchlist):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to save'}), 500


@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    """Get current watchlist"""
    _, watchlist = read_portfolio_file()
    return jsonify(watchlist)


@app.route('/api/watchlist', methods=['POST'])
def add_watchlist_item():
    """Add to watchlist"""
    data = request.json
    symbol = data.get('symbol', '').upper().strip()
    
    if not symbol:
        return jsonify({'success': False, 'error': 'Invalid symbol'}), 400
    
    holdings, watchlist = read_portfolio_file()
    
    # Check if already exists
    if symbol in watchlist:
        return jsonify({'success': False, 'error': 'Already in watchlist'}), 400
    
    watchlist.append(symbol)
    
    if write_portfolio_file(holdings, watchlist):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to save'}), 500


@app.route('/api/watchlist/<symbol>', methods=['DELETE'])
def delete_watchlist_item(symbol):
    """Delete from watchlist"""
    holdings, watchlist = read_portfolio_file()
    watchlist = [w for w in watchlist if w != symbol.upper()]
    
    if write_portfolio_file(holdings, watchlist):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to save'}), 500


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    data = request.json
    config = read_config_file()
    
    # Update with new values
    if 'email_from' in data:
        config['email_from'] = data['email_from']
    if 'email_to' in data:
        config['email_to'] = data['email_to']
    if 'hard_stop' in data:
        config['hard_stop'] = float(data['hard_stop'])
    if 'warning' in data:
        config['warning'] = float(data['warning'])
    if 'profit_target' in data:
        config['profit_target'] = float(data['profit_target'])
    if 'pullback' in data:
        config['pullback'] = float(data['pullback'])
    if 'rsi_max' in data:
        config['rsi_max'] = float(data['rsi_max'])
    
    if write_config_file(config):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to save'}), 500


if __name__ == '__main__':
    import logging
    
    # Reduce Flask debugger console noise
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)
    
    print("\n" + "="*60)
    print("🌐 Trading Bot Web UI")
    print("="*60)
    print("\n📱 Open your browser and go to: http://localhost:5000")
    print("⌨️  Press Ctrl+C to stop the server\n")
    
    # Set debug=False for production, or True for development
    # debug=True shows detailed error pages but more console output
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

