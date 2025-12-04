"""
Smart Computer Player for Wheel of Fortune
Uses the smart decision function to make optimal choices.
"""

try:
    from smart_decision import (
        should_spin_or_buy_vowel,
        get_best_vowel_guess,
        get_best_consonant_guess,
        estimate_solution_distribution,
    )
except Exception:
    from src.PlayGame.smart_decision import (
        should_spin_or_buy_vowel,
        get_best_vowel_guess,
        get_best_consonant_guess,
        estimate_solution_distribution,
    )
import random
import re

# Confidence threshold for attempting a solve (AI will attempt when top candidate >= this)
SOLVE_CONFIDENCE_THRESHOLD = 0.75


def computer_turn_smart(showing, winnings, previous_guesses, turn):
    """
    Smart computer player that uses advanced decision-making logic.
    
    Args:
        showing: Current puzzle state with blanks
        winnings: List of winnings for all players
        previous_guesses: List of already guessed letters
        turn: Current turn number
    
    Returns:
        Tuple of (guess, dollar_value)
    """
    
    player_winnings = winnings[turn % 3]
    # Build opponents list and use smart decision function
    opponents = [w for i, w in enumerate(winnings) if i != (turn % 3)]
    decision, reasoning = should_spin_or_buy_vowel(
        showing, player_winnings, previous_guesses, opponents_winnings=opponents, strategy='optimized'
    )
    
    print(f"Smart AI reasoning: {reasoning}")
    
    if decision == 'solve':
        # Always attempt a solve when the decision says 'solve'. Use the top
        # corpus candidate if available; otherwise synthesize a best-effort
        # guess by filling blanks with the common vowel 'E'. The game loop
        # will validate the attempt.
        sol = estimate_solution_distribution(showing, previous_guesses)
        top = sol.get('candidates', [])
        if top:
            candidate = top[0][0]
        else:
            from smart_decision import synthesize_candidate
            candidate = synthesize_candidate(showing, previous_guesses)
        print(f"Smart AI attempting to solve: {candidate} (p={sol.get('top_probability', 0.0):.2f})")
        return f"SOLVE:{candidate}", 0
    
    if decision == 'buy_vowel':
        # Ensure the actual winnings array shows sufficient funds; in some
        # contexts decision reasoning can be stale, so check the real state.
        if winnings[turn % 3] >= 250:
            vowel = get_best_vowel_guess(showing, previous_guesses)
            print(f"Smart AI bought vowel: {vowel}")
            winnings[turn % 3] -= 250
            return vowel, 0
        else:
            print("Smart AI wanted to buy a vowel but lacks funds, spinning instead")
            decision = 'spin'
    
    else:  # decision == 'spin'
        # Spin the wheel and guess best consonant
        try:
            from play_random_puzzle import spin_wheel
            dollar = spin_wheel()
        except Exception:
            # local lightweight fallback
            wheel_values = [0, -1, 500, 550, 600, 650, 700, 750, 800, 850, 900, -1,
                            500, 550, 600, 650, 700, 750, 800, 850, 900, 500, 550, 600]
            dollar = random.choice(wheel_values)
        
        if dollar == 0:
            print("Smart AI lost a turn")
            return "_", 0
        elif dollar == -1:
            print("Smart AI went bankrupt")
            winnings[turn % 3] = 0
            return "_", 0
        else:
            consonant = get_best_consonant_guess(showing, previous_guesses)
            print(f"Smart AI guessed consonant: {consonant}")
            return consonant, dollar


def computer_turn_smart_conservative(showing, winnings, previous_guesses, turn):
    """
    Conservative version of smart player - more likely to buy vowels.
    """
    
    player_winnings = winnings[turn % 3]
    
    # Modify the decision by being more conservative
    opponents = [w for i, w in enumerate(winnings) if i != (turn % 3)]
    decision, reasoning = should_spin_or_buy_vowel(
        showing, player_winnings, previous_guesses, opponents_winnings=opponents, strategy='optimized'
    )
    
    # Conservative adjustment: if we have money and there might be vowels, buy them
    blank_count = showing.count('_')
    vowels_guessed = sum(1 for v in 'AEIOU' if v in previous_guesses)
    
    if (player_winnings >= 250 and blank_count > 3 and vowels_guessed < 3 and 
        decision == 'spin'):
        decision = 'buy_vowel'
        reasoning = "Conservative strategy: preserving money for vowels"
    
    print(f"Conservative AI reasoning: {reasoning}")
    
    if decision == 'buy_vowel':
        # Double-check actual funds before buying (avoid stale reasoning)
        if winnings[turn % 3] >= 250:
            vowel = get_best_vowel_guess(showing, previous_guesses)
            print(f"Conservative AI bought vowel: {vowel}")
            winnings[turn % 3] -= 250
            return vowel, 0
        else:
            print("Conservative AI wanted to buy a vowel but lacks funds, spinning instead")
            decision = 'spin'
    else:
        if decision == 'solve':
            sol = estimate_solution_distribution(showing, previous_guesses)
            top = sol.get('candidates', [])
            if top:
                candidate = top[0][0]
            else:
                from smart_decision import synthesize_candidate
                candidate = synthesize_candidate(showing, previous_guesses)
            print(f"Conservative AI attempting to solve: {candidate} (p={sol.get('top_probability', 0.0):.2f})")
            return f"SOLVE:{candidate}", 0

        try:
            from play_random_puzzle import spin_wheel
            dollar = spin_wheel()
        except Exception:
            wheel_values = [0, -1, 500, 550, 600, 650, 700, 750, 800, 850, 900, -1,
                            500, 550, 600, 650, 700, 750, 800, 850, 900, 500, 550, 600]
            dollar = random.choice(wheel_values)
        
        if dollar == 0:
            print("Conservative AI lost a turn")
            return "_", 0
        elif dollar == -1:
            print("Conservative AI went bankrupt")
            winnings[turn % 3] = 0
            return "_", 0
        else:
            consonant = get_best_consonant_guess(showing, previous_guesses)
            print(f"Conservative AI guessed consonant: {consonant}")
            return consonant, dollar


def computer_turn_smart_aggressive(showing, winnings, previous_guesses, turn):
    """
    Aggressive version of smart player - more likely to spin for higher rewards.
    """
    
    player_winnings = winnings[turn % 3]
    
    opponents = [w for i, w in enumerate(winnings) if i != (turn % 3)]
    decision, reasoning = should_spin_or_buy_vowel(
        showing, player_winnings, previous_guesses, opponents_winnings=opponents, strategy='optimized'
    )
    
    # Aggressive adjustment: prefer spinning unless vowels are very likely
    vowel_density = showing.count('_') / max(1, len(showing.replace(' ', '')))
    
    if decision == 'buy_vowel' and vowel_density < 0.5:
        decision = 'spin'
        reasoning = "Aggressive strategy: spinning for higher rewards"
    
    print(f"Aggressive AI reasoning: {reasoning}")
    
    if decision == 'buy_vowel':
        # Double-check actual funds before buying (avoid stale reasoning)
        if winnings[turn % 3] >= 250:
            vowel = get_best_vowel_guess(showing, previous_guesses)
            print(f"Aggressive AI bought vowel: {vowel}")
            winnings[turn % 3] -= 250
            return vowel, 0
        else:
            print("Aggressive AI wanted to buy a vowel but lacks funds, spinning instead")
            decision = 'spin'
    else:
        if decision == 'solve':
            sol = estimate_solution_distribution(showing, previous_guesses)
            top = sol.get('candidates', [])
            if top:
                candidate = top[0][0]
            else:
                from smart_decision import synthesize_candidate
                candidate = synthesize_candidate(showing, previous_guesses)
            print(f"Aggressive AI attempting to solve: {candidate} (p={sol.get('top_probability', 0.0):.2f})")
            return f"SOLVE:{candidate}", 0

        try:
            from play_random_puzzle import spin_wheel
            dollar = spin_wheel()
        except Exception:
            wheel_values = [0, -1, 500, 550, 600, 650, 700, 750, 800, 850, 900, -1,
                            500, 550, 600, 650, 700, 750, 800, 850, 900, 500, 550, 600]
            dollar = random.choice(wheel_values)
        
        if dollar == 0:
            print("Aggressive AI lost a turn")
            return "_", 0
        elif dollar == -1:
            print("Aggressive AI went bankrupt")
            winnings[turn % 3] = 0
            return "_", 0
        else:
            consonant = get_best_consonant_guess(showing, previous_guesses)
            print(f"Aggressive AI guessed consonant: {consonant}")
            return consonant, dollar


# Test the smart players
if __name__ == "__main__":
    # Test scenario
    showing = "T_E _U_C_ _RO__ _O_"
    winnings = [800, 600, 400]
    previous_guesses = ['T', 'E', 'C', 'O']
    turn = 0
    
    print("Testing Smart Players:")
    print("=" * 30)
    print(f"Puzzle: {showing}")
    print(f"Winnings: {winnings}")
    print(f"Previous guesses: {previous_guesses}")
    print()
    
    # Test each player type
    players = [
        ("Smart", computer_turn_smart),
        ("Conservative", computer_turn_smart_conservative),
        ("Aggressive", computer_turn_smart_aggressive)
    ]
    
    for name, player_func in players:
        print(f"{name} Player:")
        # Make a copy of winnings to avoid modifying original
        test_winnings = winnings.copy()
        try:
            guess, dollar = player_func(showing, test_winnings, previous_guesses, turn)
            print(f"Result: guess='{guess}', dollar={dollar}")
            print(f"Updated winnings: {test_winnings}")
        except Exception as e:
            print(f"Error: {e}")
        print()
