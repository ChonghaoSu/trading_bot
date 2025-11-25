"""
Trading Rules Engine - Evaluates Alert Conditions
Contains all logic for stop losses, profit targets, and buy signals
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import config
from alerts import AlertSystem


class TradingRules:
    """
    Evaluates trading rules against current market data
    """
    
    def __init__(self):
        """Initialize the trading rules engine"""
        self.alert_system = AlertSystem()
        self.triggered_alerts = {}  # Track which alerts already fired to avoid spam
        
    def get_stock_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data from yfinance
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1y, 6mo, etc.)
            
        Returns:
            DataFrame with historical data or None if failed
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                print(f"⚠️  No data available for {symbol}")
                return None
            
            return data
            
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")
            return None
    
    def calculate_sma(self, data: pd.DataFrame, window: int) -> pd.Series:
        """
        Calculate Simple Moving Average
        
        Args:
            data: DataFrame with 'Close' column
            window: Number of periods for SMA
            
        Returns:
            Series with SMA values
        """
        return data['Close'].rolling(window=window).mean()
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> float:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            data: DataFrame with 'Close' column
            period: RSI period (default 14)
            
        Returns:
            Current RSI value
        """
        try:
            # Calculate price changes
            delta = data['Close'].diff()
            
            # Separate gains and losses
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            # Calculate RS and RSI
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.iloc[-1]  # Return most recent RSI
            
        except Exception as e:
            print(f"❌ Error calculating RSI: {e}")
            return 50  # Return neutral RSI on error
    
    def check_hard_stop(self, symbol: str, current_price: float, 
                       avg_cost: float) -> bool:
        """
        Rule 1: Hard stop loss - price ≤ avg_cost × 0.91
        
        Returns:
            True if alert should be sent
        """
        threshold = avg_cost * config.HARD_STOP_MULTIPLIER
        
        if current_price <= threshold:
            loss_percent = ((current_price - avg_cost) / avg_cost) * 100
            
            # Check if we already alerted on this
            alert_key = f"hard_stop_{symbol}"
            if alert_key not in self.triggered_alerts:
                self.alert_system.send_hard_stop_alert(
                    symbol, current_price, avg_cost, abs(loss_percent)
                )
                self.triggered_alerts[alert_key] = datetime.now()
                return True
        
        return False
    
    def check_warning(self, symbol: str, current_price: float,
                     avg_cost: float) -> bool:
        """
        Rule 2: Early warning - price ≤ avg_cost × 0.95
        
        Returns:
            True if alert should be sent
        """
        threshold = avg_cost * config.WARNING_MULTIPLIER
        hard_stop_threshold = avg_cost * config.HARD_STOP_MULTIPLIER
        
        # Only warn if between warning and hard stop levels
        if hard_stop_threshold < current_price <= threshold:
            loss_percent = ((current_price - avg_cost) / avg_cost) * 100
            
            alert_key = f"warning_{symbol}"
            if alert_key not in self.triggered_alerts:
                self.alert_system.send_warning_alert(
                    symbol, current_price, avg_cost, abs(loss_percent)
                )
                self.triggered_alerts[alert_key] = datetime.now()
                return True
        
        return False
    
    def check_profit_target(self, symbol: str, current_price: float,
                           avg_cost: float) -> bool:
        """
        Rule 3: Profit taking - price ≥ avg_cost × 1.30
        
        Returns:
            True if alert should be sent
        """
        threshold = avg_cost * config.PROFIT_TARGET_MULTIPLIER
        
        if current_price >= threshold:
            gain_percent = ((current_price - avg_cost) / avg_cost) * 100
            
            alert_key = f"profit_{symbol}"
            if alert_key not in self.triggered_alerts:
                self.alert_system.send_profit_alert(
                    symbol, current_price, avg_cost, gain_percent
                )
                self.triggered_alerts[alert_key] = datetime.now()
                return True
        
        return False
    
    def check_sma_200_breach(self, symbol: str) -> bool:
        """
        Rule 4: 200-day SMA breach check (Fridays after 4pm ET only)
        
        Returns:
            True if alert should be sent
        """
        # Only check on Fridays after market close
        now = datetime.now()
        if now.weekday() != 4:  # 4 = Friday
            return False
        
        if now.hour < 16:  # Before 4pm ET
            return False
        
        # Get historical data
        data = self.get_stock_data(symbol, period="1y")
        if data is None:
            return False
        
        # Calculate 200-day SMA
        sma_200 = self.calculate_sma(data, 200)
        
        if len(sma_200) < 200:
            print(f"⚠️  {symbol}: Not enough data for 200-day SMA")
            return False
        
        current_price = data['Close'].iloc[-1]
        current_sma_200 = sma_200.iloc[-1]
        
        # Check if price closed below 200-day SMA
        if current_price < current_sma_200:
            alert_key = f"sma200_{symbol}_{now.date()}"
            if alert_key not in self.triggered_alerts:
                self.alert_system.send_sma_breach_alert(
                    symbol, current_price, current_sma_200
                )
                self.triggered_alerts[alert_key] = datetime.now()
                return True
        
        return False
    
    def check_momentum_pullback(self, symbol: str) -> bool:
        """
        Rule 5: Momentum + Pullback buy signal
        Criteria:
        - Price > 50-day SMA
        - Pulled back ≥8% from 52-week high
        - RSI(14) < 65
        
        Returns:
            True if alert should be sent
        """
        # Get historical data
        data = self.get_stock_data(symbol, period="1y")
        if data is None:
            return False
        
        current_price = data['Close'].iloc[-1]
        
        # Check minimum price requirement
        if current_price < config.RECOMMENDATION_MIN_PRICE:
            return False
        
        # Calculate 50-day SMA
        sma_50 = self.calculate_sma(data, 50)
        if len(sma_50) < 50:
            return False
        current_sma_50 = sma_50.iloc[-1]
        
        # Check if price > 50-day SMA
        if current_price <= current_sma_50:
            return False
        
        # Get 52-week high
        high_52w = data['Close'].max()
        
        # Calculate pullback percentage from 52-week high
        pullback_percent = ((high_52w - current_price) / high_52w) * 100
        
        # Check if pullback >= 8%
        if pullback_percent < config.RECOMMENDATION_PULLBACK_PERCENT:
            return False
        
        # Calculate RSI
        rsi = self.calculate_rsi(data, period=14)
        
        # Check if RSI < 65
        if rsi >= config.RECOMMENDATION_RSI_MAX:
            return False
        
        # All criteria met - send recommendation
        alert_key = f"recommend_{symbol}_{datetime.now().date()}"
        if alert_key not in self.triggered_alerts:
            self.alert_system.send_recommendation(
                symbol, current_price, current_sma_50, 
                high_52w, pullback_percent, rsi
            )
            self.triggered_alerts[alert_key] = datetime.now()
            return True
        
        return False
    
    def evaluate_portfolio(self, holdings: List[Dict]) -> None:
        """
        Check all portfolio positions against alert rules
        
        Args:
            holdings: List of portfolio holdings
        """
        print(f"\n{'='*60}")
        print(f"🔍 CHECKING PORTFOLIO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        for holding in holdings:
            symbol = holding["symbol"]
            avg_cost = holding["avg_cost"]
            
            print(f"Analyzing {symbol}...")
            
            # Get current price
            data = self.get_stock_data(symbol, period="3mo")
            if data is None:
                continue
            
            current_price = data['Close'].iloc[-1]
            pnl_percent = ((current_price - avg_cost) / avg_cost) * 100
            
            print(f"  Current: ${current_price:.2f} | Avg Cost: ${avg_cost:.2f} | "
                  f"P&L: {'+' if pnl_percent >= 0 else ''}{pnl_percent:.1f}%")
            
            # Check all rules
            self.check_hard_stop(symbol, current_price, avg_cost)
            self.check_warning(symbol, current_price, avg_cost)
            self.check_profit_target(symbol, current_price, avg_cost)
            self.check_sma_200_breach(symbol)
        
        print(f"\n{'='*60}")
        print("✅ Portfolio check complete")
        print(f"{'='*60}\n")
    
    def scan_watchlist(self, watchlist: List[str]) -> None:
        """
        Scan watchlist for buy opportunities
        
        Args:
            watchlist: List of ticker symbols to analyze
        """
        print(f"\n{'='*60}")
        print(f"🔎 SCANNING WATCHLIST FOR BUY SIGNALS")
        print(f"{'='*60}\n")
        
        recommendations_found = 0
        
        for symbol in watchlist:
            try:
                if self.check_momentum_pullback(symbol):
                    recommendations_found += 1
            except Exception as e:
                print(f"⚠️  Error analyzing {symbol}: {e}")
        
        if recommendations_found == 0:
            print("No buy opportunities found at this time.")
        else:
            print(f"\n✅ Found {recommendations_found} buy recommendation(s)")
        
        print(f"\n{'='*60}\n")
    
    def generate_daily_summary(self, holdings: List[Dict]) -> str:
        """
        Generate daily portfolio summary report
        
        Args:
            holdings: List of portfolio holdings
            
        Returns:
            Formatted summary text
        """
        lines = []
        lines.append("="*50)
        lines.append("📊 PORTFOLIO SUMMARY")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("="*50)
        lines.append("")
        
        total_value = 0
        total_cost = 0
        
        for holding in holdings:
            symbol = holding["symbol"]
            shares = holding["shares"]
            avg_cost = holding["avg_cost"]
            
            # Get current price
            data = self.get_stock_data(symbol, period="5d")
            if data is None:
                continue
            
            current_price = data['Close'].iloc[-1]
            position_value = shares * current_price
            cost_basis = shares * avg_cost
            pnl = position_value - cost_basis
            pnl_percent = (pnl / cost_basis) * 100
            
            total_value += position_value
            total_cost += cost_basis
            
            # Calculate distance to stop loss
            hard_stop_price = avg_cost * config.HARD_STOP_MULTIPLIER
            distance_to_stop = ((current_price - hard_stop_price) / current_price) * 100
            
            # Format position line
            lines.append(f"{symbol:6s} | "
                        f"Price: ${current_price:7.2f} | "
                        f"Value: ${position_value:8.2f} | "
                        f"P&L: {'+' if pnl >= 0 else ''}{pnl_percent:6.1f}% | "
                        f"To Stop: {distance_to_stop:.1f}%")
        
        total_pnl = total_value - total_cost
        total_pnl_percent = (total_pnl / total_cost) * 100 if total_cost > 0 else 0
        
        lines.append("")
        lines.append("="*50)
        lines.append(f"TOTAL VALUE:  ${total_value:,.2f}")
        lines.append(f"TOTAL COST:   ${total_cost:,.2f}")
        lines.append(f"TOTAL P&L:    {'+' if total_pnl >= 0 else ''}${total_pnl:,.2f} "
                    f"({'+' if total_pnl_percent >= 0 else ''}{total_pnl_percent:.2f}%)")
        lines.append("="*50)
        
        return "\n".join(lines)
    
    def reset_daily_alerts(self) -> None:
        """
        Reset alerts that should re-trigger daily
        Call this at market open or once per day
        """
        # Keep hard stops, warnings, and profit alerts
        # Only clear recommendation alerts older than 1 day
        one_day_ago = datetime.now() - timedelta(days=1)
        
        keys_to_remove = []
        for key, timestamp in self.triggered_alerts.items():
            if "recommend_" in key and timestamp < one_day_ago:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.triggered_alerts[key]
        
        if keys_to_remove:
            print(f"🔄 Reset {len(keys_to_remove)} old alert(s)")

