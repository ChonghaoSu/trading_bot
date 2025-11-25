# Start Trading Bot Web UI
# Run this script to launch the web interface

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   🌐 Starting Trading Bot Web UI" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Flask is installed
Write-Host "Checking Flask installation..." -ForegroundColor Yellow
try {
    python -c "import flask" 2>$null
    Write-Host "✅ Flask is installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Flask not found. Installing..." -ForegroundColor Yellow
    pip install flask
}

Write-Host "`n🚀 Starting web server..." -ForegroundColor Yellow
Write-Host "📱 Open your browser and go to: http://localhost:5000" -ForegroundColor Cyan
Write-Host "⌨️  Press Ctrl+C to stop the server`n" -ForegroundColor Gray

# Start the Flask app
python app.py



