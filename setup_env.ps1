# Setup Environment Variables for Trading Bot
# Creates .env file from env.example template

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   🔐 Environment Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if .env already exists
if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Overwrite? (y/N)"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "Cancelled. Keeping existing .env file." -ForegroundColor Gray
        exit
    }
}

# Check if env.example exists
if (-not (Test-Path "env.example")) {
    Write-Host "❌ env.example not found!" -ForegroundColor Red
    Write-Host "Make sure you're in the trading-bot directory." -ForegroundColor Yellow
    exit 1
}

# Copy template
Copy-Item "env.example" ".env"

Write-Host "✅ Created .env file from template" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Open .env in a text editor" -ForegroundColor White
Write-Host "   2. Fill in your actual credentials:" -ForegroundColor White
Write-Host "      - TELEGRAM_BOT_TOKEN" -ForegroundColor Gray
Write-Host "      - TELEGRAM_CHAT_ID" -ForegroundColor Gray
Write-Host "      - RESEND_API_KEY" -ForegroundColor Gray
Write-Host "      - EMAIL_FROM" -ForegroundColor Gray
Write-Host "      - EMAIL_TO" -ForegroundColor Gray
Write-Host "   3. Save the file" -ForegroundColor White
Write-Host "`n⚠️  IMPORTANT: Never commit .env to GitHub!" -ForegroundColor Red
Write-Host "   It's already in .gitignore for safety.`n" -ForegroundColor Gray



