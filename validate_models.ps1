# Model validation script for AI Development Team (PowerShell version)

Write-Host "🔍 Validating AI Development Team Model Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Check if ollama is available
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaPath) {
    Write-Host "❌ Ollama not found. Please install Ollama first:" -ForegroundColor Red
    Write-Host "   https://ollama.com/download" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Ollama command found" -ForegroundColor Green

# Check if qwen3-coder model is available
Write-Host ""
Write-Host "📋 Checking for qwen3-coder model..." -ForegroundColor Cyan
$models = ollama list
if ($models -match "qwen3-coder") {
    Write-Host "✅ ollama/qwen3-coder model is available locally" -ForegroundColor Green
} else {
    Write-Host "❌ ollama/qwen3-coder model NOT found" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 To install the model, run:" -ForegroundColor Yellow
    Write-Host "   ollama pull qwen3-coder" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚠️  Note: The dev_bot agent requires this model for Golang development" -ForegroundColor Yellow
    exit 1
}

# Show model details
Write-Host ""
Write-Host "📊 Model Information:" -ForegroundColor Cyan
try {
    ollama show qwen3-coder --modelfile | Select-Object -First 20
} catch {
    Write-Host "   (Model details available via 'ollama show qwen3-coder')"
}

# Test basic inference
Write-Host ""
Write-Host "🧪 Testing basic inference..." -ForegroundColor Cyan
try {
    $result = & ollama run qwen3-coder "Say 'OK' if you can hear me:"
    if ($result -match "(?i)ok") {
        Write-Host "✅ Basic inference test passed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Basic inference test had issues (may be normal for first run)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Could not complete inference test" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Development Team Model Status:" -ForegroundColor Cyan
Write-Host "   • pm_bot: Flexible/OpenRouter (planning)" -ForegroundColor Green
Write-Host "   • dev_bot: ✅ ollama/qwen3-coder (local) - CONFIRMED" -ForegroundColor Green
Write-Host "   • qa_bot: Flexible/OpenRouter (review)" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Ready for AI-assisted Golang development!" -ForegroundColor Green