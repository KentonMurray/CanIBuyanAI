# 🔑 Complete Setup Guide: OpenAI API Key

## 🎯 Quick Summary
1. **Get API key** from OpenAI (free account, requires payment method)
2. **Set the key** as environment variable 
3. **Test it works** with our test script
4. **Play the game** with AI commentary!

---

## Step 1: Get Your OpenAI API Key

### 1.1 Create Account
1. Go to **https://platform.openai.com/**
2. Click **"Sign up"** (or "Log in" if you have an account)
3. Complete registration with email/password

### 1.2 Add Payment Method ⚠️ REQUIRED
1. Click **"Billing"** in left sidebar
2. Click **"Add payment method"**
3. Add credit card (usage is very cheap - usually under $0.10 per game session)

### 1.3 Generate API Key
1. Click **"API Keys"** in left sidebar
2. Click **"Create new secret key"**
3. Name it "Wheel of Fortune Game"
4. Click **"Create secret key"**
5. **COPY THE KEY IMMEDIATELY** - looks like: `sk-1234567890abcdef...`
6. **SAVE IT SAFELY** - you can't see it again!

---

## Step 2: Set Your API Key

### 🚀 EASIEST METHOD: Use Our Setup Scripts

#### Option A: Temporary Setup (for testing)
```bash
cd /workspace/project/CanIBuyanAI
nano set_api_key_temp.sh
# Replace YOUR_API_KEY_HERE with your actual key
# Save and exit (Ctrl+X, Y, Enter)

chmod +x set_api_key_temp.sh
source set_api_key_temp.sh
```

#### Option B: Permanent Setup (recommended)
```bash
cd /workspace/project/CanIBuyanAI
nano set_api_key_permanent.sh
# Replace YOUR_API_KEY_HERE with your actual key
# Save and exit (Ctrl+X, Y, Enter)

chmod +x set_api_key_permanent.sh
./set_api_key_permanent.sh
```

### 🔧 MANUAL METHOD: Set Environment Variable

#### Linux/Mac (Bash)
```bash
# Temporary (this session only)
export OPENAI_API_KEY="sk-your-actual-key-here"

# Permanent (add to ~/.bashrc)
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Linux/Mac (Zsh)
```bash
# Permanent (add to ~/.zshrc)
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### Windows (Command Prompt)
```cmd
setx OPENAI_API_KEY "sk-your-actual-key-here"
# Restart command prompt after this
```

#### Windows (PowerShell)
```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-your-actual-key-here", "User")
# Restart PowerShell after this
```

---

## Step 3: Test Your Setup

### 3.1 Check API Key is Set
```bash
echo $OPENAI_API_KEY
# Should show: sk-your-key...
```

### 3.2 Run Integration Test
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 test_chatgpt.py
```

**✅ SUCCESS looks like:**
```
✅ API Key found: sk-1234...abcd
✅ ChatGPT wrapper initialized successfully
✅ Using model: gpt-3.5-turbo
✅ API call successful!
📝 Sample commentary: And here comes our contestant with a confident spin!
🎉 ChatGPT integration is working perfectly!
```

**❌ FAILURE looks like:**
```
❌ No OpenAI API key found!
```

### 3.3 Play the Game!
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 play_with_commentary.py
```

---

## 🔍 Troubleshooting

### Problem: "No OpenAI API key found"
**Solution:** The environment variable isn't set
```bash
# Check if it's set:
echo $OPENAI_API_KEY

# If empty, set it:
export OPENAI_API_KEY="sk-your-key-here"
```

### Problem: "No module named 'openai'"
**Solution:** Install the OpenAI package
```bash
pip install openai --upgrade
```

### Problem: "API call failed" or "Invalid API key"
**Solutions:**
1. **Check your key is correct** - it should start with `sk-`
2. **Verify billing is set up** - OpenAI requires a payment method
3. **Check you have credits** - go to platform.openai.com billing
4. **Try a new key** - generate a fresh API key

### Problem: "Rate limit exceeded"
**Solution:** Wait a moment, then try again. The system will fall back to templates automatically.

### Problem: Works in terminal but not in new sessions
**Solution:** The key isn't permanently saved
```bash
# Add to your shell profile:
echo 'export OPENAI_API_KEY="sk-your-key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 💰 Cost Information

**ChatGPT usage is very affordable:**
- **Model:** GPT-3.5-turbo ($0.0015 per 1K tokens)
- **Per commentary:** ~50-100 tokens (~$0.0001-0.0002)
- **Typical game:** 20-50 commentaries (~$0.002-0.01)
- **Victory speech:** ~200 tokens (~$0.0003)

**Example costs:**
- **1 game:** ~$0.01
- **10 games:** ~$0.10  
- **100 games:** ~$1.00

---

## 🎮 Usage Examples

### With ChatGPT (AI Commentary)
```bash
export OPENAI_API_KEY="sk-your-key"
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 play_with_commentary.py
```

### Without ChatGPT (Template Commentary - Still Great!)
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 play_with_commentary.py
```

### Demo Mode
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 demo_commentary.py
```

---

## 🎪 What You Get

### Without API Key (Template Mode)
- ✅ Pat Sajak commentary using rich templates
- ✅ Player personalities with character responses
- ✅ Interactive commentary system
- ✅ Victory speeches
- ✅ All features work perfectly!

### With API Key (AI Mode)
- 🤖 **Dynamic commentary** - Never repeats, always fresh
- 🎭 **Personality-driven responses** - AI matches character traits
- 🏆 **Custom victory speeches** - Personalized to your gameplay
- ✨ **Natural conversation** - More engaging and realistic

---

## 🆘 Still Need Help?

### Quick Test Commands
```bash
# Test 1: Check if key is set
echo "Key status: $OPENAI_API_KEY"

# Test 2: Test the integration
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 test_chatgpt.py

# Test 3: Play the game
python3 play_with_commentary.py
```

### Common Issues & Solutions
1. **Key not found** → Set environment variable
2. **Module not found** → Run `pip install openai`
3. **API call failed** → Check billing setup on OpenAI
4. **Works once then stops** → Add key to shell profile permanently

---

## 🎉 Ready to Play!

Once your API key is set up:

```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 play_with_commentary.py human smart conservative
```

**You'll see:**
```
🎪 INTERACTIVE HOST MODE ACTIVATED! 🎪
Pat Sajak and our contestants are ready to entertain!

Meet our contestants:
🎭 Amazing Player 1 the Teacher: Optimistic, Strategic, Confident
🎭 Incredible Player 2 from Boston: Aggressive, Dramatic, Lucky

🎙️ Pat Sajak: Welcome to Wheel of Fortune! Let's see what our contestants can do...
```

**Enjoy your AI-powered Wheel of Fortune experience!** 🎪