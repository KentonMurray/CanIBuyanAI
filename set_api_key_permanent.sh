#!/bin/bash
# Permanent API Key Setup Script
# Replace YOUR_API_KEY_HERE with your actual key

echo "🔑 Setting OpenAI API Key Permanently"
echo "====================================="

# Replace this with your actual API key
API_KEY="YOUR_API_KEY_HERE"

if [ "$API_KEY" = "YOUR_API_KEY_HERE" ]; then
    echo "❌ Please edit this script and replace YOUR_API_KEY_HERE with your actual API key"
    echo "   1. Open set_api_key_permanent.sh"
    echo "   2. Replace YOUR_API_KEY_HERE with your sk-... key"
    echo "   3. Run this script again"
    exit 1
fi

echo "Adding API key to your shell profile..."

# Add to .bashrc (most common)
if [ -f ~/.bashrc ]; then
    echo "export OPENAI_API_KEY=\"$API_KEY\"" >> ~/.bashrc
    echo "✅ Added to ~/.bashrc"
fi

# Add to .zshrc (if using zsh)
if [ -f ~/.zshrc ]; then
    echo "export OPENAI_API_KEY=\"$API_KEY\"" >> ~/.zshrc
    echo "✅ Added to ~/.zshrc"
fi

# Set for current session
export OPENAI_API_KEY="$API_KEY"

echo "✅ API Key set permanently!"
echo "🔄 Reloading shell configuration..."

# Reload the shell configuration
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi
if [ -f ~/.zshrc ]; then
    source ~/.zshrc
fi

echo "🧪 Testing the integration..."
cd src/PlayGame
python3 test_chatgpt.py

echo ""
echo "🎉 Setup complete! Your API key will now work in all new terminal sessions."
echo "🎮 You can now play with AI commentary:"
echo "   python3 play_with_commentary.py"