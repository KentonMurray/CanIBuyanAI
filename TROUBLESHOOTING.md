# 🔧 Troubleshooting Guide

## 🚨 Common Issues and Solutions

### ❌ "python3: command not found" or "python exe not found"

**Solution 1: Try different Python commands**
```bash
# Try these in order:
python3 demo_commentary.py
python demo_commentary.py
py demo_commentary.py
```

**Solution 2: Use our helper scripts**
```bash
# Linux/Mac:
./run_game.sh

# Windows:
run_game.bat
```

**Solution 3: Install Python**
- **Windows**: Download from https://python.org
- **Mac**: `brew install python3` or download from python.org
- **Linux**: `sudo apt install python3` (Ubuntu/Debian) or `sudo yum install python3` (CentOS/RHEL)

### ❌ "Permission denied" when running ./script.py

**Solution:**
```bash
chmod +x *.py
chmod +x run_game.sh
```

### ❌ "No module named 'interactive_host'"

**Solution: Make sure you're in the right directory**
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 demo_commentary.py
```

### ❌ Script starts but stops immediately

**This is normal!** The game is waiting for your input. Look for prompts like:
```
1: Spin, 2: Buy Vowel, 3: Solve ....
```

## 🎯 Step-by-Step Diagnosis

### Step 1: Test Your System
```bash
cd /workspace/project/CanIBuyanAI
python3 test_system.py
```

### Step 2: Run the Demo (No Input Required)
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 demo_commentary.py
```

### Step 3: Try the Interactive Game
```bash
python3 play_with_commentary.py smart smart smart
```

## 🎮 Different Ways to Run

### Method 1: Direct Python Command
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
python3 play_with_commentary.py
```

### Method 2: Executable Script
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame
./play_with_commentary.py
```

### Method 3: Helper Scripts
```bash
cd /workspace/project/CanIBuyanAI
./run_game.sh          # Linux/Mac
run_game.bat           # Windows
```

### Method 4: From Any Directory
```bash
python3 /workspace/project/CanIBuyanAI/src/PlayGame/demo_commentary.py
```

## 🔍 What Should Happen

### Successful Start:
```
📦 Hugging Face transformers not installed
   Install with: pip install transformers torch
   Using enhanced templates instead (still great!)
🆓 FREE AI MODE ACTIVATED!
   Using enhanced template system (still awesome!)

🎪 INTERACTIVE HOST MODE ACTIVATED! 🎪
Pat Sajak and our contestants are ready to entertain!
```

### If You See This - It's Working!
The system is waiting for input. Follow the prompts:
```
1: Spin, 2: Buy Vowel, 3: Solve ....
```

## 🆘 Still Having Issues?

### Check Python Installation
```bash
python3 --version      # Should show Python 3.x
which python3          # Should show path to python3
```

### Check File Permissions
```bash
ls -la *.py            # Should show -rwxr-xr-x (executable)
```

### Check Current Directory
```bash
pwd                    # Should end with /src/PlayGame
ls                     # Should show play_with_commentary.py
```

### Run System Test
```bash
python3 test_system.py # Should show "ALL TESTS PASSED!"
```

## 🎪 Quick Success Test

**Try this simple command:**
```bash
cd /workspace/project/CanIBuyanAI/src/PlayGame && python3 -c "print('🎪 Python is working!'); from free_ai_wrapper import FreeAIWrapper; print('✅ System ready!')"
```

**Expected output:**
```
🎪 Python is working!
📦 Hugging Face transformers not installed
   Install with: pip install transformers torch
   Using enhanced templates instead (still great!)
🆓 FREE AI MODE ACTIVATED!
   Using enhanced template system (still awesome!)
✅ System ready!
```

---

## 🎯 If Nothing Works

The system is designed to work with **zero setup**. If you're still having issues:

1. **Try the system test**: `python3 test_system.py`
2. **Check the exact error message** you're seeing
3. **Try different Python commands**: `python3`, `python`, `py`
4. **Make sure you're in the right directory**: `/workspace/project/CanIBuyanAI/src/PlayGame`

The system is **100% free** and should work immediately!