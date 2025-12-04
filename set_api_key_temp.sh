#!/bin/bash
# Temporary API Key Setup Script
# Replace YOUR_API_KEY_HERE with your actual key

echo "🔑 Setting OpenAI API Key Temporarily"
echo "======================================"

# Replace this with your actual API key
export OPENAI_API_KEY="YOUR_API_KEY_HERE"

echo "✅ API Key set for this session"
echo "🧪 Testing the integration..."

cd src/PlayGame
python3 test_chatgpt.py

echo ""
echo "🎮 If the test passed, you can now play with AI commentary:"
echo "   python3 play_with_commentary.py"
echo ""
echo "⚠️  Note: This key will be lost when you close the terminal"
echo "   For permanent setup, see Method B in the instructions"