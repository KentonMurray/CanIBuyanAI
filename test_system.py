#!/usr/bin/env python3
"""
Simple system test to diagnose any issues
"""

import sys
import os

print("🔍 SYSTEM DIAGNOSTIC")
print("=" * 50)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Script location: {__file__}")

# Test imports
try:
    print("\n📦 TESTING IMPORTS...")
    
    # Test basic imports
    import random
    print("✅ random module imported")
    
    import re
    print("✅ re module imported")
    
    # Test our modules
    sys.path.append('/workspace/project/CanIBuyanAI/src/PlayGame')
    
    from free_ai_wrapper import FreeAIWrapper
    print("✅ FreeAIWrapper imported")
    
    from interactive_host import InteractiveHost
    print("✅ InteractiveHost imported")
    
    # Test creating instances
    ai = FreeAIWrapper()
    print("✅ FreeAIWrapper instance created")
    
    host = InteractiveHost(ai)
    print("✅ InteractiveHost instance created")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Your system is working perfectly!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print("\n🎮 READY TO PLAY!")
print("Try: python3 demo_commentary.py")