"""
Demo script for the Interactive Host Commentary System
Shows the system in action without requiring user input
"""

from interactive_host import InteractiveHost
import time

def demo_commentary_system():
    """Demonstrate the commentary system with simulated game actions"""
    
    print("🎮 WHEEL OF FORTUNE INTERACTIVE HOST DEMO 🎮")
    print("=" * 60)
    
    # Initialize the interactive host
    host = InteractiveHost()
    host.enable_interactive_mode()
    
    print("\n" + "=" * 60)
    print("🎲 SIMULATING GAME ACTIONS...")
    print("=" * 60)
    
    # Simulate a series of game actions
    game_actions = [
        {'type': 'spin', 'player': 1, 'details': 'spun wheel, landed on $600'},
        {'type': 'guess_consonant', 'player': 1, 'details': 'letter: R, count: 2, correct'},
        {'type': 'spin', 'player': 2, 'details': 'spun wheel, landed on $500'},  # This will trigger user commentary
        {'type': 'guess_consonant', 'player': 2, 'details': 'letter: S, count: 1, correct'},
        {'type': 'buy_vowel', 'player': 1, 'details': 'letter: E, count: 3, correct'},
        {'type': 'spin', 'player': 2, 'details': 'spun wheel, landed on BANKRUPT'},  # This will trigger player commentary
        {'type': 'spin', 'player': 1, 'details': 'spun wheel, landed on $750'},
        {'type': 'guess_consonant', 'player': 1, 'details': 'letter: T, count: 2, correct'},
        {'type': 'wrong_guess', 'player': 2, 'details': 'letter: N, count: 0'},  # This will trigger user commentary
    ]
    
    # Override the user input function to provide automatic responses
    original_prompt_user = host._prompt_user_commentary
    
    def mock_user_commentary(action):
        """Mock user commentary to avoid input prompts"""
        print(f"\n🎤 Your turn to comment! What do you think about what just happened?")
        print(f"(Action: {action['details']})")
        
        # Provide some sample user responses
        sample_responses = [
            "That was an exciting spin! The wheel really knows how to keep us on our toes!",
            "Great strategy there! I love seeing the players think through their moves.",
            "Ouch! That's the risk you take in Wheel of Fortune, but don't give up!",
            "What a fantastic guess! Those letters are really adding up on the board.",
            "The suspense is killing me! This game is so unpredictable and fun!"
        ]
        
        import random
        user_response = random.choice(sample_responses)
        print(f"🎤 You: {user_response}")
        
        # Pat responds
        pat_responses = [
            "Great observation!",
            "You're absolutely right!",
            "That's exactly what I was thinking!",
            "You know this game well!",
            "Excellent point!"
        ]
        
        pat_response = random.choice(pat_responses)
        print(f"🎙️ Pat Sajak: {pat_response}")
        time.sleep(1)
    
    # Replace the user input function
    host._prompt_user_commentary = mock_user_commentary
    
    # Execute the game actions
    for i, action in enumerate(game_actions, 1):
        print(f"\n--- Action {i}: {action['type'].upper()} ---")
        host.log_game_action(action['type'], action['player'], action['details'])
        time.sleep(1.5)  # Pause between actions for readability
    
    print("\n" + "=" * 60)
    print("🏆 VICTORY SPEECH DEMO")
    print("=" * 60)
    
    # Demonstrate victory speech
    host.generate_victory_speech(1, 4500)
    
    print("\n" + "=" * 60)
    print("✨ DEMO COMPLETE!")
    print("=" * 60)
    print("🎪 Features demonstrated:")
    print("   ✅ Player personality generation (50+ traits)")
    print("   ✅ Pat Sajak commentary (1st & 2nd actions)")
    print("   ✅ Interactive commentary system (3rd actions)")
    print("   ✅ Player personality-based responses")
    print("   ✅ Victory speech generation")
    print("   ✅ ChatGPT integration (with template fallback)")
    print("\n🎮 To play with commentary: python3 play_with_commentary.py")
    print("🎮 To play without commentary: python3 play_with_commentary.py --no-commentary")

if __name__ == "__main__":
    demo_commentary_system()