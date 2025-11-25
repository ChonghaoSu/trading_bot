# Trading Bot Setup Script for Windows PowerShell
# Run this script to set up the bot automatically

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   🤖 Trading Alert Bot Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python from python.org" -ForegroundColor Red
    exit 1
}

# Install required packages
Write-Host "`nInstalling required packages..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install packages" -ForegroundColor Red
    exit 1
}

# Check if config.py exists
if (-Not (Test-Path "config.py")) {
    Write-Host "`n⚠️  config.py not found!" -ForegroundColor Yellow
    Write-Host "Creating config.py from template..." -ForegroundColor Yellow
    Copy-Item "config.example.py" "config.py"
    Write-Host "✅ config.py created" -ForegroundColor Green
    Write-Host "`n⚠️  IMPORTANT: Edit config.py and add your credentials!" -ForegroundColor Red
    Write-Host "   1. Telegram Bot Token" -ForegroundColor White
    Write-Host "   2. Telegram Chat ID" -ForegroundColor White
    Write-Host "   3. Resend API Key" -ForegroundColor White
    Write-Host "   4. Email addresses`n" -ForegroundColor White
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   ✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Edit config.py with your credentials" -ForegroundColor White
Write-Host "  2. Update portfolio.py with your holdings" -ForegroundColor White
Write-Host "  3. Test notifications: python bot.py --test-alerts" -ForegroundColor White
Write-Host "  4. Run the bot: python bot.py`n" -ForegroundColor White

Write-Host "📖 See QUICKSTART.md for detailed instructions`n" -ForegroundColor Cyan

