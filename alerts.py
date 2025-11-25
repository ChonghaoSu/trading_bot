"""
Alert System - Handles Telegram and Email Notifications
Sends alerts when trading rules are breached
"""

import requests
from datetime import datetime
from typing import Optional
import config


class AlertSystem:
    """
    Manages notifications via Telegram and Email
    """
    
    def __init__(self):
        """Initialize the alert system"""
        self.telegram_enabled = config.TELEGRAM_ENABLED
        self.email_enabled = config.EMAIL_ENABLED
        self.telegram_token = config.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = config.TELEGRAM_CHAT_ID
        self.resend_api_key = config.RESEND_API_KEY
        self.email_from = config.EMAIL_FROM
        self.email_to = config.EMAIL_TO
        
    def send_telegram(self, message: str) -> bool:
        """
        Send a message via Telegram Bot
        
        Args:
            message: The text message to send
            
        Returns:
            True if successful, False otherwise
        """
        if not self.telegram_enabled:
            return False
            
        if "YOUR_" in self.telegram_token or "YOUR_" in self.telegram_chat_id:
            print("⚠️  Telegram not configured - skipping notification")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            # Convert chat_id to int if it's a numeric string
            chat_id = self.telegram_chat_id
            if isinstance(chat_id, str) and chat_id.isdigit():
                chat_id = int(chat_id)
            
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"  # Allows basic formatting
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ Telegram notification sent successfully")
                return True
            else:
                error_data = response.json() if response.text else {}
                error_desc = error_data.get("description", response.text)
                
                # Provide helpful error messages
                if "chat not found" in error_desc.lower():
                    print(f"❌ Telegram error: Chat not found")
                    print(f"   💡 SOLUTION: Open Telegram and send a message to your bot first!")
                    print(f"   💡 Then the bot will be able to message you back.")
                elif "unauthorized" in error_desc.lower():
                    print(f"❌ Telegram error: Invalid bot token")
                    print(f"   💡 Check your TELEGRAM_BOT_TOKEN in config.py")
                else:
                    print(f"❌ Telegram API error: {response.status_code} - {error_desc}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}")
            return False
    
    def send_email(self, subject: str, body: str) -> bool:
        """
        Send an email via Resend API
        
        Args:
            subject: Email subject line
            body: Email body content (HTML supported)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.email_enabled:
            return False
            
        if "YOUR_" in self.resend_api_key or "YOUR_" in self.email_from:
            print("⚠️  Email not configured - skipping notification")
            return False
        
        try:
            url = "https://api.resend.com/emails"
            
            headers = {
                "Authorization": f"Bearer {self.resend_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "from": self.email_from,
                "to": [self.email_to],
                "subject": subject,
                "html": f"<pre>{body}</pre>"  # Preserve formatting with <pre> tag
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ Email notification sent successfully")
                return True
            else:
                print(f"❌ Resend API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def send_alert(self, message: str, subject: Optional[str] = None) -> None:
        """
        Send an alert via both Telegram and Email
        
        Args:
            message: The alert message
            subject: Email subject (optional, auto-generated if None)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add timestamp to message
        formatted_message = f"🚨 TRADING ALERT 🚨\n{timestamp}\n\n{message}"
        
        # Generate subject if not provided
        if subject is None:
            subject = f"Trading Alert - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        print("\n" + "="*60)
        print(formatted_message)
        print("="*60 + "\n")
        
        # Send via Telegram (primary)
        self.send_telegram(formatted_message)
        
        # Send via Email (fallback)
        self.send_email(subject, formatted_message)
    
    def send_hard_stop_alert(self, symbol: str, current_price: float, 
                            avg_cost: float, loss_percent: float) -> None:
        """
        Critical alert: Hard stop loss triggered
        """
        message = (
            f"🔴 HARD STOP TRIGGERED - SELL NOW! 🔴\n\n"
            f"Symbol: {symbol}\n"
            f"Current Price: ${current_price:.2f}\n"
            f"Your Avg Cost: ${avg_cost:.2f}\n"
            f"Loss: {loss_percent:.1f}%\n\n"
            f"⚠️ ACTION REQUIRED: Sell 100% of position immediately!"
        )
        self.send_alert(message, f"🔴 HARD STOP: {symbol} - SELL NOW")
    
    def send_warning_alert(self, symbol: str, current_price: float,
                          avg_cost: float, loss_percent: float) -> None:
        """
        Warning alert: Approaching stop loss
        """
        message = (
            f"⚠️ EARLY WARNING - Approaching Stop Loss\n\n"
            f"Symbol: {symbol}\n"
            f"Current Price: ${current_price:.2f}\n"
            f"Your Avg Cost: ${avg_cost:.2f}\n"
            f"Loss: {loss_percent:.1f}%\n\n"
            f"📊 Prepare to sell if it drops further to ${avg_cost * 0.91:.2f}"
        )
        self.send_alert(message, f"⚠️ WARNING: {symbol} Approaching Stop")
    
    def send_profit_alert(self, symbol: str, current_price: float,
                         avg_cost: float, gain_percent: float) -> None:
        """
        Profit-taking alert: 30% target hit
        """
        message = (
            f"🎯 PROFIT TARGET HIT - Consider Taking Gains! 🎯\n\n"
            f"Symbol: {symbol}\n"
            f"Current Price: ${current_price:.2f}\n"
            f"Your Avg Cost: ${avg_cost:.2f}\n"
            f"Gain: +{gain_percent:.1f}%\n\n"
            f"💰 Consider selling 60-75% to lock in profits"
        )
        self.send_alert(message, f"🎯 PROFIT: {symbol} +30% Target Hit")
    
    def send_sma_breach_alert(self, symbol: str, current_price: float,
                              sma_200: float) -> None:
        """
        200-day SMA breach alert (Friday close)
        """
        message = (
            f"📉 200-DAY SMA BREACH DETECTED\n\n"
            f"Symbol: {symbol}\n"
            f"Closing Price: ${current_price:.2f}\n"
            f"200-Day SMA: ${sma_200:.2f}\n\n"
            f"⚠️ PLAN TO SELL: Consider selling on Monday morning"
        )
        self.send_alert(message, f"📉 {symbol} - 200-Day MA Breach")
    
    def send_recommendation(self, symbol: str, current_price: float,
                           sma_50: float, high_52w: float, 
                           pullback_percent: float, rsi: float) -> None:
        """
        Buy recommendation: Momentum + Pullback detected
        """
        message = (
            f"💡 BUY OPPORTUNITY DETECTED\n\n"
            f"Symbol: {symbol}\n"
            f"Current Price: ${current_price:.2f}\n"
            f"50-Day SMA: ${sma_50:.2f}\n"
            f"52-Week High: ${high_52w:.2f}\n"
            f"Pullback: {pullback_percent:.1f}% from high\n"
            f"RSI(14): {rsi:.1f}\n\n"
            f"✅ Momentum + Pullback criteria met\n"
            f"📈 Consider buying - price above 50-day MA with healthy pullback"
        )
        self.send_alert(message, f"💡 BUY SIGNAL: {symbol}")
    
    def send_daily_summary(self, summary_text: str) -> None:
        """
        Send daily portfolio summary (5pm ET)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"📊 DAILY PORTFOLIO SUMMARY\n{timestamp}\n\n{summary_text}"
        
        print("\n" + "="*60)
        print(message)
        print("="*60 + "\n")
        
        self.send_telegram(message)
        self.send_email("📊 Daily Portfolio Summary", message)
    
    def test_notifications(self) -> None:
        """
        Send test notifications to verify setup
        """
        print("\n🧪 Testing notification systems...\n")
        
        test_message = (
            f"✅ Trading Bot Test Alert\n\n"
            f"This is a test message to verify your notification setup.\n"
            f"If you received this, everything is working correctly!\n\n"
            f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # Test Telegram
        telegram_success = False
        if self.telegram_enabled:
            print("Testing Telegram...")
            telegram_success = self.send_telegram(test_message)
            if not telegram_success:
                print("\n📋 Telegram Setup Checklist:")
                print("   1. Did you create a bot with @BotFather?")
                print("   2. Did you get your chat_id from @userinfobot?")
                print("   3. ⚠️  IMPORTANT: Have you sent a message to your bot yet?")
                print("      → Open Telegram, search for your bot, and send it '/start'")
                print("      → The bot can't message you until you message it first!")
        
        # Test Email
        email_success = False
        if self.email_enabled:
            print("\nTesting Email...")
            email_success = self.send_email("Trading Bot - Test Alert", test_message)
        
        print("\n" + "="*60)
        if telegram_success and email_success:
            print("✅ All notifications working! You're all set.")
        elif email_success:
            print("✅ Email working, but Telegram needs setup (see above)")
        elif telegram_success:
            print("✅ Telegram working, but Email needs setup")
        else:
            print("⚠️  Some notifications need configuration")
        print("="*60 + "\n")


# =============================================================================
# TESTING FUNCTION
# =============================================================================

def verify_telegram_setup() -> bool:
    """
    Verify Telegram bot can access the chat
    Returns True if setup is correct
    """
    import config
    
    if "YOUR_" in config.TELEGRAM_BOT_TOKEN or "YOUR_" in config.TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials not configured in config.py")
        return False
    
    try:
        # Try to get bot info first
        bot_info_url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(bot_info_url, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Invalid bot token. Check TELEGRAM_BOT_TOKEN in config.py")
            return False
        
        bot_info = response.json()
        bot_username = bot_info.get("result", {}).get("username", "Unknown")
        print(f"✅ Bot found: @{bot_username}")
        
        # Try to get chat info
        chat_id = config.TELEGRAM_CHAT_ID
        if isinstance(chat_id, str) and chat_id.isdigit():
            chat_id = int(chat_id)
        
        chat_url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getChat"
        chat_response = requests.post(chat_url, json={"chat_id": chat_id}, timeout=10)
        
        if chat_response.status_code == 200:
            print(f"✅ Chat ID verified: {config.TELEGRAM_CHAT_ID}")
            print(f"✅ Setup looks good! Try sending a message to @{bot_username} first if you haven't.")
            return True
        else:
            error_data = chat_response.json() if chat_response.text else {}
            error_desc = error_data.get("description", chat_response.text)
            
            if "chat not found" in error_desc.lower():
                print(f"❌ Chat not found. This usually means:")
                print(f"   1. You haven't messaged the bot yet")
                print(f"   2. The chat_id might be incorrect")
                print(f"\n💡 SOLUTION:")
                print(f"   → Open Telegram and search for @{bot_username}")
                print(f"   → Send the bot a message (like '/start')")
                print(f"   → Then run the test again")
            else:
                print(f"❌ Error: {error_desc}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
        return False


def test_alerts():
    """
    Run this to test your alert setup
    Usage: python -c "from alerts import test_alerts; test_alerts()"
    """
    print("\n" + "="*60)
    print("🔍 VERIFYING TELEGRAM SETUP")
    print("="*60)
    verify_telegram_setup()
    print()
    
    alert_system = AlertSystem()
    alert_system.test_notifications()


if __name__ == "__main__":
    # Allow testing alerts directly: python alerts.py
    test_alerts()

