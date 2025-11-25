# GitHub Readiness Verification Script
# Run this before pushing to GitHub

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   🔍 GitHub Readiness Check" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$issues = @()
$warnings = @()

# Check 1: Verify .gitignore exists
Write-Host "Checking .gitignore..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    Write-Host "✅ .gitignore exists" -ForegroundColor Green
    
    # Check if config.py is in .gitignore
    $gitignore = Get-Content ".gitignore" -Raw
    if ($gitignore -match "config\.py") {
        Write-Host "✅ config.py is in .gitignore" -ForegroundColor Green
    } else {
        $issues += "config.py is NOT in .gitignore"
        Write-Host "❌ config.py is NOT in .gitignore" -ForegroundColor Red
    }
    
    if ($gitignore -match "\.env") {
        Write-Host "✅ .env is in .gitignore" -ForegroundColor Green
    } else {
        $issues += ".env is NOT in .gitignore"
        Write-Host "❌ .env is NOT in .gitignore" -ForegroundColor Red
    }
} else {
    $issues += ".gitignore file missing"
    Write-Host "❌ .gitignore not found" -ForegroundColor Red
}

# Check 2: Verify env.example exists
Write-Host "`nChecking env.example..." -ForegroundColor Yellow
if (Test-Path "env.example") {
    Write-Host "✅ env.example exists" -ForegroundColor Green
    
    # Check if it has placeholder values
    $envExample = Get-Content "env.example" -Raw
    if ($envExample -match "YOUR_|your_|placeholder") {
        Write-Host "✅ env.example has placeholder values" -ForegroundColor Green
    } else {
        $warnings += "env.example might contain real values - verify manually"
        Write-Host "⚠️  env.example might have real values" -ForegroundColor Yellow
    }
} else {
    $issues += "env.example missing"
    Write-Host "❌ env.example not found" -ForegroundColor Red
}

# Check 3: Check if config.py has real credentials (warning only, it's in .gitignore)
Write-Host "`nChecking config.py (for reference)..." -ForegroundColor Yellow
if (Test-Path "config.py") {
    $config = Get-Content "config.py" -Raw
    if ($config -match "8202402702|re_4ysnWD1w|8447327070") {
        $warnings += "config.py contains real credentials (but it's in .gitignore, so safe)"
        Write-Host "⚠️  config.py has real credentials (protected by .gitignore)" -ForegroundColor Yellow
    } else {
        Write-Host "✅ config.py has no hardcoded credentials" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  config.py not found (will need to be created from config.example.py)" -ForegroundColor Yellow
}

# Check 4: Verify essential files exist
Write-Host "`nChecking essential files..." -ForegroundColor Yellow
$essentialFiles = @(
    "bot.py",
    "rules.py",
    "alerts.py",
    "portfolio.py",
    "app.py",
    "requirements.txt",
    "README.md"
)

foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        $issues += "$file is missing"
        Write-Host "❌ $file missing" -ForegroundColor Red
    }
}

# Check 5: Check if .env exists (should not be committed)
Write-Host "`nChecking for .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $warnings += ".env file exists (make sure it's in .gitignore)"
    Write-Host "⚠️  .env file exists (should be in .gitignore)" -ForegroundColor Yellow
} else {
    Write-Host "✅ No .env file (good - use env.example template)" -ForegroundColor Green
}

# Check 6: Verify config.example.py exists
Write-Host "`nChecking config.example.py..." -ForegroundColor Yellow
if (Test-Path "config.example.py") {
    Write-Host "✅ config.example.py exists" -ForegroundColor Green
} else {
    $warnings += "config.example.py missing (optional but recommended)"
    Write-Host "⚠️  config.example.py not found (optional)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   📊 Summary" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if ($issues.Count -eq 0) {
    Write-Host "✅ READY TO PUSH!" -ForegroundColor Green
    Write-Host "   No critical issues found.`n" -ForegroundColor Green
} else {
    Write-Host "❌ NOT READY - Fix these issues first:" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "   - $issue" -ForegroundColor Red
    }
    Write-Host ""
}

if ($warnings.Count -gt 0) {
    Write-Host "⚠️  Warnings (optional improvements):" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "   - $warning" -ForegroundColor Yellow
    }
    Write-Host ""
}

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "   1. Review the issues above" -ForegroundColor White
Write-Host "   2. Run: git status (to see what will be committed)" -ForegroundColor White
Write-Host "   3. Run: git add ." -ForegroundColor White
Write-Host "   4. Run: git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "   5. Push to GitHub`n" -ForegroundColor White



