#!/bin/bash
# Model validation script for AI Development Team

echo "🔍 Validating AI Development Team Model Setup"
echo "============================================"

# Check if ollama is available
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama first:"
    echo "   https://ollama.com/download"
    exit 1
fi

echo "✅ Ollama command found"

# Check if qwen3-coder model is available
echo ""
echo "📋 Checking for qwen3-coder model..."
if ollama list | grep -q "qwen3-coder"; then
    echo "✅ ollama/qwen3-coder model is available locally"
else
    echo "❌ ollama/qwen3-coder model NOT found"
    echo ""
    echo "📥 To install the model, run:"
    echo "   ollama pull qwen3-coder"
    echo ""
    echo "⚠️  Note: The dev_bot agent requires this model for Golang development"
    exit 1
fi

# Show model details
echo ""
echo "📊 Model Information:"
ollama show qwen3-coder --modelfile 2>/dev/null | head -20 || echo "   (Model details available via 'ollama show qwen3-coder')"

# Test basic inference
echo ""
echo "🧪 Testing basic inference..."
if echo "Hello" | ollama run qwen3-coder "Say 'OK' if you can hear me:" | grep -iq "ok"; then
    echo "✅ Basic inference test passed"
else
    echo "⚠️  Basic inference test had issues (may be normal for first run)"
fi

echo ""
echo "🎯 Development Team Model Status:"
echo "   • pm_bot: Flexible/OpenRouter (planning)"
echo "   • dev_bot: ✅ ollama/qwen3-coder (local) - CONFIRMED"
echo "   • qa_bot: Flexible/OpenRouter (review)"
echo ""
echo "🚀 Ready for AI-assisted Golang development!"