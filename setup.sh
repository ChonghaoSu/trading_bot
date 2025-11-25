#!/bin/bash
# Trading Bot Setup Script for Mac/Linux
# Run this script to set up the bot automatically

echo ""
echo "========================================"
echo "   🤖 Trading Alert Bot Setup"
echo "========================================"
echo ""

# Check if Python is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Found: $PYTHON_VERSION"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✅ Found: $PYTHON_VERSION"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Python not found! Please install Python from python.org"
    exit 1
fi

# Install required packages
echo ""
echo "Installing required packages..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Packages installed successfully"
else
    echo "❌ Failed to install packages"
    exit 1
fi

# Check if config.py exists
if [ ! -f "config.py" ]; then
    echo ""
    echo "⚠️  config.py not found!"
    echo "Creating config.py from template..."
    cp config.example.py config.py
    echo "✅ config.py created"
    echo ""
    echo "⚠️  IMPORTANT: Edit config.py and add your credentials!"
    echo "   1. Telegram Bot Token"
    echo "   2. Telegram Chat ID"
    echo "   3. Resend API Key"
    echo "   4. Email addresses"
    echo ""
fi

echo ""
echo "========================================"
echo "   ✅ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Edit config.py with your credentials"
echo "  2. Update portfolio.py with your holdings"
echo "  3. Test notifications: $PYTHON_CMD bot.py --test-alerts"
echo "  4. Run the bot: $PYTHON_CMD bot.py"
echo ""
echo "📖 See QUICKSTART.md for detailed instructions"
echo ""

# Make the script executable
chmod +x setup.sh

