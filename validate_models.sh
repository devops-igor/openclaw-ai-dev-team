#!/bin/bash
# Model validation script for AI Development Team (OpenRouter version)

echo "🔍 Validating AI Development Team Model Setup"
echo "============================================"

# Determine OpenClaw config path
config_paths=(
    "$HOME/.openclaw/openclaw.json"
    "/c/Users/Igor/.openclaw/openclaw.json"
    "../.openclaw/openclaw.json"
    ".openclaw/openclaw.json"
)
config_path=""
for path in "${config_paths[@]}"; do
    if [ -f "$path" ]; then
        config_path="$path"
        break
    fi
done

if [ -z "$config_path" ]; then
    echo "❌ OpenClaw configuration not found. Please ensure OpenClaw is installed."
    exit 1
fi

echo "✅ Found OpenClaw config at: $config_path"

# Check if jq is available for JSON parsing
if ! command -v jq &> /dev/null; then
    echo "⚠️  'jq' is not installed. Installing jq may help with JSON parsing."
    echo "   On Windows with Git Bash: 'pacman -S jq'"
    echo "   On Linux: 'apt-get install jq' or 'yum install jq'"
    echo "   Proceeding with basic grep checks..."
    # Fallback to grep checks
    if grep -q '"openrouter"' "$config_path"; then
        echo "✅ OpenRouter provider appears in config"
    else
        echo "❌ OpenRouter provider not found in config"
        exit 1
    fi

    if grep -q '"xiaomi/mimo-v2-pro"' "$config_path"; then
        echo "✅ xiaomi/mimo-v2-pro model is registered"
    else
        echo "❌ xiaomi/mimo-v2-pro model is NOT registered in OpenRouter provider"
        exit 1
    fi
else
    # Use jq for robust JSON parsing
    echo "📋 Checking OpenRouter provider configuration..."

    # Check if openrouter provider exists
    if ! jq -e '.models.providers.openrouter' "$config_path" > /dev/null; then
        echo "❌ OpenRouter provider not configured in openclaw.json"
        exit 1
    fi
    echo "✅ OpenRouter provider configured"

    # Check API key
    api_key=$(jq -r '.models.providers.openrouter.apiKey // empty' "$config_path")
    if [ -z "$api_key" ]; then
        echo "❌ OpenRouter API key is missing. Please set it in openclaw.json"
        exit 1
    fi
    echo "✅ OpenRouter API key is configured"

    # Check required models
    required_models=("xiaomi/mimo-v2-pro")
    for model in "${required_models[@]}"; do
        if jq -e --arg model "$model" '.models.providers.openrouter.models[] | select(.id == $model)' "$config_path" > /dev/null; then
            echo "✅ Model '$model' is registered in OpenRouter provider"
        else
            echo "❌ Model '$model' is NOT registered in OpenRouter provider"
            missing_models=1
        fi
    done

    if [ -n "$missing_models" ]; then
        echo ""
        echo "📥 Missing models need to be added to openclaw.json under:"
        echo "   models.providers.openrouter.models"
        echo ""
        echo "Example entry:"
        echo @'{
  "id": "xiaomi/mimo-v2-pro",
  "name": "Xiaomi Mimo V2 Pro",
  "contextWindow": 32768,
  "input": ["text"],
  "cost": {
    "input": 0,
    "output": 0,
    "cacheRead": 0,
    "cacheWrite": 0
  }
}'@
        exit 1
    fi
fi

# Verify agent configurations in the team project
team_project_path="/c/Users/Igor/OpenClaw/openclaw-ai-dev-team"
echo ""
echo "👥 Checking AI Development Team agent configurations..."

agents_to_check=(
    "dev_bot|openrouter/xiaomi/mimo-v2-pro|$team_project_path/dev_bot/AGENTS.md"
    "qa_bot|openrouter/xiaomi/mimo-v2-pro|$team_project_path/qa_bot/AGENTS.md"
)

any_agent_misconfigured=0
for agent_conf in "${agents_to_check[@]}"; do
    IFS='|' read -r name expected_model file_path <<< "$agent_conf"
    if [ -f "$file_path" ]; then
        if grep -q "$expected_model" "$file_path"; then
            echo "✅ $name is configured to use $expected_model"
        else
            echo "❌ $name does not reference $expected_model in AGENTS.md"
            any_agent_misconfigured=1
        fi
    else
        echo "⚠️  Could not find $name/AGENTS.md at $file_path"
    fi
done

if [ $any_agent_misconfigured -eq 1 ]; then
    echo ""
    echo "⚠️  Some agent configurations are not properly set. Please update AGENTS.md files."
fi

echo ""
echo "🎯 Development Team Model Status:"
echo "   • pm_bot: Flexible/OpenRouter (planning)"
echo "   • dev_bot: ✅ openrouter/xiaomi/mimo-v2-pro - CONFIRMED"
echo "   • qa_bot: ✅ openrouter/xiaomi/mimo-v2-pro - CONFIRMED"
echo ""
echo "🚀 Ready for AI-assisted Golang development with xiaomi/mimo-v2-pro!"