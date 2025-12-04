#!/usr/bin/env python3
"""
Demonstration of the Smart Decision Function for Wheel of Fortune

This script shows how the smart decision function works with various game scenarios.
"""

from smart_decision import should_spin_or_buy_vowel, get_best_vowel_guess, get_best_consonant_guess


def demo_decision_function():
    """Demonstrate the smart decision function with various scenarios."""
    
    print("🎡 WHEEL OF FORTUNE - SMART DECISION DEMO 🎡")
    print("=" * 60)
    print()
    
    scenarios = [
        {
            'name': '🎯 Early Game - Fresh Puzzle',
            'showing': '_ _ _ _ _ _ _ _',
            'winnings': 0,
            'previous_guesses': [],
            'description': 'Brand new puzzle, no money yet'
        },
        {
            'name': '💰 Early Game - Some Money',
            'showing': '_ _ _ _ _ _ _ _',
            'winnings': 500,
            'previous_guesses': [],
            'description': 'Fresh puzzle but player has some winnings'
        },
        {
            'name': '🔤 Mid Game - Some Letters Revealed',
            'showing': 'T_E _U_C_ _RO__ _O_',
            'winnings': 800,
            'previous_guesses': ['T', 'E', 'C', 'O'],
            'description': 'Several letters guessed, good winnings'
        },
        {
            'name': '🎪 Mid Game - Low on Cash',
            'showing': 'T_E _U_C_ _RO__ _O_',
            'winnings': 200,
            'previous_guesses': ['T', 'E', 'C', 'O'],
            'description': 'Same puzzle but low winnings'
        },
        {
            'name': '🏁 Late Game - Almost Complete',
            'showing': 'THE QUICK _RO_N _O_',
            'winnings': 1200,
            'previous_guesses': ['T', 'H', 'E', 'Q', 'U', 'I', 'C', 'K', 'R', 'O', 'N'],
            'description': 'Puzzle nearly solved, high winnings'
        },
        {
            'name': '🔍 Vowel-Heavy Puzzle',
            'showing': '_E_U_I_U_ _A_E',
            'winnings': 600,
            'previous_guesses': ['E', 'U', 'I', 'A'],
            'description': 'Many vowels already revealed'
        },
        {
            'name': '🚫 No Money for Vowels',
            'showing': '_O_SO_A_T _U__LE',
            'winnings': 150,
            'previous_guesses': ['O', 'S', 'A', 'T', 'U', 'L', 'E'],
            'description': 'Cannot afford vowels'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Puzzle: {scenario['showing']}")
        print(f"Winnings: ${scenario['winnings']}")
        print(f"Previous guesses: {scenario['previous_guesses']}")
        print()
        
        # Get decision
        decision, reasoning = should_spin_or_buy_vowel(
            scenario['showing'],
            scenario['winnings'],
            scenario['previous_guesses']
        )
        
        # Display decision
        if decision == 'spin':
            print("🎡 DECISION: SPIN THE WHEEL")
            consonant = get_best_consonant_guess(scenario['showing'], scenario['previous_guesses'])
            print(f"📝 Recommended consonant: {consonant}")
        elif decision == 'buy_vowel':
            print("💰 DECISION: BUY A VOWEL")
            vowel = get_best_vowel_guess(scenario['showing'], scenario['previous_guesses'])
            print(f"📝 Recommended vowel: {vowel}")
        elif decision == 'solve':
            print("🎯 DECISION: SOLVE THE PUZZLE")
        
        print(f"🧠 Reasoning: {reasoning}")
        print("-" * 60)
        print()


def interactive_demo():
    """Allow user to input their own scenario."""
    
    print("🎮 INTERACTIVE DEMO")
    print("Enter your own Wheel of Fortune scenario!")
    print()
    
    try:
        showing = input("Enter the puzzle (use _ for blanks): ").upper()
        winnings = int(input("Enter current winnings: $"))
        guesses_input = input("Enter previous guesses (separated by spaces): ").upper()
        previous_guesses = guesses_input.split() if guesses_input.strip() else []
        
        print()
        print("🎡 ANALYZING YOUR SCENARIO...")
        print("-" * 40)
        print(f"Puzzle: {showing}")
        print(f"Winnings: ${winnings}")
        print(f"Previous guesses: {previous_guesses}")
        print()
        
        decision, reasoning = should_spin_or_buy_vowel(showing, winnings, previous_guesses)
        
        if decision == 'spin':
            print("🎡 RECOMMENDATION: SPIN THE WHEEL")
            consonant = get_best_consonant_guess(showing, previous_guesses)
            print(f"📝 Best consonant to guess: {consonant}")
        elif decision == 'buy_vowel':
            print("💰 RECOMMENDATION: BUY A VOWEL")
            vowel = get_best_vowel_guess(showing, previous_guesses)
            print(f"📝 Best vowel to buy: {vowel}")
        elif decision == 'solve':
            print("🎯 RECOMMENDATION: SOLVE THE PUZZLE")
        
        print(f"🧠 Reasoning: {reasoning}")
        
    except (ValueError, KeyboardInterrupt):
        print("\nDemo cancelled or invalid input.")


if __name__ == "__main__":
    demo_decision_function()
    
    print("\n" + "=" * 60)
    interactive_demo()
    
    print("\n🎉 Thanks for trying the Smart Decision Demo!")
    print("💡 Tip: Try running the full game with smart players:")
    print("   python3 play_random_puzzle.py smart conservative aggressive")