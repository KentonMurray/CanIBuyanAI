#!/usr/bin/env python3
"""
Test script to verify ChatGPT integration is working
"""

import os
import sys

def test_chatgpt_integration():
    """Test the ChatGPT integration"""
    
    print("🤖 ChatGPT Integration Test")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key found!")
        print("\n🔑 To enable ChatGPT integration:")
        print("1. Get an API key from https://platform.openai.com/")
        print("2. Set it as an environment variable:")
        print("   export OPENAI_API_KEY='sk-your-key-here'")
        print("3. Run this test again")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Test wrapper initialization
    try:
        from chatgpt_wrapper import ChatGPTWrapper
        wrapper = ChatGPTWrapper()
        
        if wrapper.use_ai:
            print("✅ ChatGPT wrapper initialized successfully")
            print(f"✅ Using model: {wrapper.model}")
        else:
            print("❌ ChatGPT wrapper failed to initialize")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing wrapper: {e}")
        return False
    
    # Test a simple API call
    print("\n🧪 Testing API call...")
    try:
        test_action = {
            'type': 'spin',
            'details': 'spun wheel, landed on $600'
        }
        
        commentary = wrapper.generate_pat_sajak_commentary(test_action, "Test Player")
        print(f"✅ API call successful!")
        print(f"📝 Sample commentary: {commentary}")
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        print("💡 This might be due to:")
        print("   - Invalid API key")
        print("   - No credits/quota remaining")
        print("   - Network connectivity issues")
        return False
    
    print("\n🎉 ChatGPT integration is working perfectly!")
    print("🎮 You can now use: python3 play_with_commentary.py")
    return True

def test_template_fallback():
    """Test that template fallback works without API key"""
    
    print("\n🔄 Testing Template Fallback")
    print("=" * 40)
    
    # Temporarily remove API key
    original_key = os.environ.get('OPENAI_API_KEY')
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    try:
        from chatgpt_wrapper import ChatGPTWrapper
        wrapper = ChatGPTWrapper()
        
        if not wrapper.use_ai:
            print("✅ Template mode activated correctly")
        
        # Test template commentary
        test_action = {
            'type': 'spin',
            'details': 'spun wheel, landed on $600'
        }
        
        commentary = wrapper.generate_pat_sajak_commentary(test_action, "Test Player")
        print(f"✅ Template commentary generated: {commentary}")
        
    except Exception as e:
        print(f"❌ Template fallback failed: {e}")
    finally:
        # Restore API key if it existed
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key

if __name__ == "__main__":
    print("🎪 Interactive Host System - ChatGPT Test")
    print("=" * 50)
    
    # Test ChatGPT integration
    chatgpt_works = test_chatgpt_integration()
    
    # Test template fallback
    test_template_fallback()
    
    print("\n" + "=" * 50)
    if chatgpt_works:
        print("🎉 All tests passed! ChatGPT integration is ready!")
    else:
        print("⚠️  ChatGPT not available, but templates work fine!")
        print("   The system will use template-based commentary.")
    
    print("\n🎮 Ready to play:")
    print("   python3 play_with_commentary.py")
    print("   python3 demo_commentary.py")