#!/usr/bin/env python3
"""
Diagnostic script to identify OpenAI import issues
Run this to see exactly where the OpenAI import error is coming from
"""

import sys
import traceback

def test_import(module_name, description):
    """Test importing a module and report results"""
    print(f"\n🔍 Testing {description}...")
    try:
        if module_name == "interactive_host":
            from interactive_host import InteractiveHost
            print(f"✅ {description} imported successfully")
            return True
        elif module_name == "chatgpt_wrapper":
            from chatgpt_wrapper import ChatGPTWrapper
            print(f"✅ {description} imported successfully")
            return True
        elif module_name == "free_ai_wrapper":
            from free_ai_wrapper import FreeAIWrapper
            print(f"✅ {description} imported successfully")
            return True
        elif module_name == "openai":
            import openai
            print(f"✅ {description} imported successfully")
            return True
        else:
            exec(f"import {module_name}")
            print(f"✅ {description} imported successfully")
            return True
    except ImportError as e:
        print(f"📦 {description} import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False

def main():
    print("🔧 OpenAI Import Diagnostic Tool")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {sys.path[0]}")
    
    # Test basic imports first
    test_import("sys", "sys module")
    test_import("os", "os module")
    
    # Test our custom modules
    test_import("free_ai_wrapper", "FreeAIWrapper")
    test_import("chatgpt_wrapper", "ChatGPTWrapper") 
    test_import("interactive_host", "InteractiveHost")
    
    # Test OpenAI specifically
    test_import("openai", "OpenAI package")
    
    # Test the full play_with_commentary import
    print(f"\n🔍 Testing play_with_commentary.py import...")
    try:
        import play_with_commentary
        print("✅ play_with_commentary.py imported successfully")
    except Exception as e:
        print(f"❌ play_with_commentary.py import failed: {e}")
        print("Full traceback:")
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSIS COMPLETE")
    print("\nIf you see any ❌ errors above, that's where the problem is!")
    print("If everything shows ✅, then the issue might be in your specific environment.")

if __name__ == "__main__":
    main()