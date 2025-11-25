"""
Trading Alert Bot - Main Application
Monitors portfolio and sends alerts during market hours
"""

import schedule
import time
import pytz
from datetime import datetime, date
from typing import List
import config
import portfolio
from rules import TradingRules
from alerts import AlertSystem


class TradingBot:
    """
    Main trading bot that runs on a schedule
    """
    
    def __init__(self):
        """Initialize the trading bot"""
        self.rules_engine = TradingRules()
        self.alert_system = AlertSystem()
        self.eastern = pytz.timezone('America/New_York')
        self.last_summary_date = None
        
        print("\n" + "="*60)
        print("🤖 TRADING ALERT BOT INITIALIZED")
        print("="*60)
        print(f"Portfolio Holdings: {len(portfolio.holdings)} positions")
        print(f"Watchlist: {len(portfolio.watchlist)} symbols")
        print(f"Check Interval: Every {config.CHECK_INTERVAL_MINUTES} minutes")
        print(f"Market Hours: {config.MARKET_OPEN_HOUR}:{config.MARKET_OPEN_MINUTE:02d} - "
              f"{config.MARKET_CLOSE_HOUR}:{config.MARKET_CLOSE_MINUTE:02d} ET")
        print("="*60 + "\n")
    
    def is_market_holiday(self) -> bool:
        """
        Check if today is a market holiday
        
        Returns:
            True if today is a holiday
        """
        today_str = date.today().strftime("%Y-%m-%d")
        return today_str in config.MARKET_HOLIDAYS_2025
    
    def is_market_hours(self) -> bool:
        """
        Check if current time is within market hours
        
        Returns:
            True if market is currently open
        """
        # Testing mode bypasses market hours check
        if config.TESTING_MODE:
            return True
        
        # Check if today is a holiday
        if self.is_market_holiday():
            print("📅 Market is closed today (holiday)")
            return False
        
        # Get current time in Eastern timezone
        now_et = datetime.now(self.eastern)
        
        # Check if it's a weekday (0=Monday, 6=Sunday)
        if now_et.weekday() >= 5:  # Saturday or Sunday
            return False
        
        # Market open time
        market_open = now_et.replace(
            hour=config.MARKET_OPEN_HOUR,
            minute=config.MARKET_OPEN_MINUTE,
            second=0,
            microsecond=0
        )
        
        # Market close time
        market_close = now_et.replace(
            hour=config.MARKET_CLOSE_HOUR,
            minute=config.MARKET_CLOSE_MINUTE,
            second=0,
            microsecond=0
        )
        
        # Check if current time is between open and close
        return market_open <= now_et <= market_close
    
    def should_send_daily_summary(self) -> bool:
        """
        Check if it's time to send the daily summary (5pm ET, once per day)
        
        Returns:
            True if summary should be sent
        """
        now_et = datetime.now(self.eastern)
        today = now_et.date()
        
        # Skip weekends and holidays
        if now_et.weekday() >= 5 or self.is_market_holiday():
            return False
        
        # Check if we already sent summary today
        if self.last_summary_date == today:
            return False
        
        # Check if it's after 5pm ET
        summary_time = now_et.replace(
            hour=config.DAILY_SUMMARY_HOUR,
            minute=config.DAILY_SUMMARY_MINUTE,
            second=0,
            microsecond=0
        )
        
        return now_et >= summary_time
    
    def check_portfolio(self) -> None:
        """
        Main job: Check portfolio against all rules
        Runs every 5 minutes during market hours
        """
        # Check if market is open
        if not self.is_market_hours():
            print(f"⏸️  Market is closed - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return
        
        try:
            # Log to file if enabled
            if config.LOG_TO_FILE:
                self.log_to_file("Starting portfolio check")
            
            # Evaluate all portfolio positions
            self.rules_engine.evaluate_portfolio(portfolio.holdings)
            
            # Optional: Scan watchlist for buy opportunities
            if config.ENABLE_WATCHLIST_SCANNING:
                self.rules_engine.scan_watchlist(portfolio.watchlist)
            
        except Exception as e:
            error_msg = f"❌ Error during portfolio check: {e}"
            print(error_msg)
            if config.LOG_TO_FILE:
                self.log_to_file(error_msg)
    
    def send_daily_summary(self) -> None:
        """
        Send daily portfolio summary at 5pm ET
        """
        if not self.should_send_daily_summary():
            return
        
        try:
            print("\n📊 Generating daily summary...")
            
            summary_text = self.rules_engine.generate_daily_summary(portfolio.holdings)
            self.alert_system.send_daily_summary(summary_text)
            
            # Mark that we sent summary today
            self.last_summary_date = datetime.now(self.eastern).date()
            
            if config.LOG_TO_FILE:
                self.log_to_file("Daily summary sent")
                
        except Exception as e:
            error_msg = f"❌ Error generating daily summary: {e}"
            print(error_msg)
            if config.LOG_TO_FILE:
                self.log_to_file(error_msg)
    
    def reset_daily_state(self) -> None:
        """
        Reset daily tracking at market open
        """
        now_et = datetime.now(self.eastern)
        
        # Only run once at market open
        if (now_et.hour == config.MARKET_OPEN_HOUR and 
            now_et.minute == config.MARKET_OPEN_MINUTE):
            
            print("\n🔄 New trading day - resetting state...")
            self.rules_engine.reset_daily_alerts()
            self.last_summary_date = None
    
    def log_to_file(self, message: str) -> None:
        """
        Write log message to file
        
        Args:
            message: Log message to write
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(config.LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(f"⚠️  Failed to write to log file: {e}")
    
    def run_test_check(self) -> None:
        """
        Run a single portfolio check for testing purposes
        """
        print("\n🧪 Running test check (ignoring market hours)...\n")
        
        # Temporarily enable testing mode
        original_mode = config.TESTING_MODE
        config.TESTING_MODE = True
        
        try:
            self.check_portfolio()
        finally:
            config.TESTING_MODE = original_mode
        
        print("\n✅ Test check complete!\n")
    
    def run(self) -> None:
        """
        Start the bot with scheduled tasks
        """
        print("\n🚀 Starting Trading Alert Bot...")
        print(f"⏰ Will check portfolio every {config.CHECK_INTERVAL_MINUTES} minutes during market hours")
        print(f"📊 Daily summary will be sent at {config.DAILY_SUMMARY_HOUR}:00 ET")
        print("\n⌨️  Press Ctrl+C to stop\n")
        
        # Log startup
        if config.LOG_TO_FILE:
            self.log_to_file("="*60)
            self.log_to_file("Bot started")
            self.log_to_file("="*60)
        
        # Schedule the main portfolio check
        schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(self.check_portfolio)
        
        # Schedule daily summary check (runs every minute to catch the right time)
        schedule.every(1).minutes.do(self.send_daily_summary)
        
        # Schedule daily reset check
        schedule.every(1).minutes.do(self.reset_daily_state)
        
        # Run initial check immediately
        self.check_portfolio()
        
        # Main loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)  # Check every second
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Bot stopped by user")
            if config.LOG_TO_FILE:
                self.log_to_file("Bot stopped by user")
                self.log_to_file("="*60)
        
        except Exception as e:
            error_msg = f"❌ Fatal error: {e}"
            print(f"\n{error_msg}")
            if config.LOG_TO_FILE:
                self.log_to_file(error_msg)
                self.log_to_file("="*60)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """
    Main function to run the trading bot
    """
    import sys
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # Run a single test check
            bot = TradingBot()
            bot.run_test_check()
            return
        
        elif sys.argv[1] == "--test-alerts":
            # Test notification system
            from alerts import test_alerts
            test_alerts()
            return
        
        elif sys.argv[1] == "--verify":
            # Verify Telegram setup
            from alerts import verify_telegram_setup
            verify_telegram_setup()
            return
        
        elif sys.argv[1] == "--summary":
            # Generate and print summary
            bot = TradingBot()
            summary = bot.rules_engine.generate_daily_summary(portfolio.holdings)
            print(summary)
            return
        
        elif sys.argv[1] == "--scan":
            # Scan watchlist for buy opportunities
            bot = TradingBot()
            bot.rules_engine.scan_watchlist(portfolio.watchlist)
            return
        
        elif sys.argv[1] == "--help":
            print("\n🤖 Trading Alert Bot - Usage:")
            print("\nCommands:")
            print("  python bot.py              - Start the bot (runs continuously)")
            print("  python bot.py --test       - Run a single portfolio check")
            print("  python bot.py --test-alerts - Test Telegram and email notifications")
            print("  python bot.py --verify     - Verify Telegram bot setup")
            print("  python bot.py --summary    - Generate portfolio summary")
            print("  python bot.py --scan       - Scan watchlist for buy signals")
            print("  python bot.py --help       - Show this help message")
            print()
            return
        
        else:
            print(f"❌ Unknown command: {sys.argv[1]}")
            print("Run 'python bot.py --help' for usage information")
            return
    
    # Default: start the bot
    bot = TradingBot()
    bot.run()


if __name__ == "__main__":
    main()

