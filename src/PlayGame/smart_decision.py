"""
Smart Decision Function for Wheel of Fortune
Decides whether to spin the wheel or buy a vowel based on game state analysis.
"""

import re
import random
from typing import Tuple, Dict, List


def should_spin_or_buy_vowel(
    showing: str,
    winnings: int,
    previous_guesses: List[str],
    next_letter_candidate: str = None
) -> Tuple[str, str]:
    """
    Intelligent decision function for Wheel of Fortune gameplay.
    
    Args:
        showing: Current state of the puzzle with blanks as underscores
        winnings: Current player winnings
        previous_guesses: List of letters already guessed
        next_letter_candidate: The letter we're considering guessing (optional)
    
    Returns:
        Tuple of (decision, reasoning) where decision is 'spin', 'buy_vowel', or 'solve'
        and reasoning explains the decision logic
    """
    
    # Analyze current game state
    game_state = analyze_game_state(showing, previous_guesses)
    
    # If we can't afford a vowel, we must spin
    if winnings < 250:
        return 'spin', "Insufficient funds to buy vowel ($250 required)"
    
    # If puzzle is nearly complete (>80% revealed), consider solving
    if game_state['completion_ratio'] > 0.8:
        return 'solve', f"Puzzle is {game_state['completion_ratio']:.1%} complete - time to solve"
    
    # Calculate expected values and risks
    spin_analysis = analyze_spin_risk()
    vowel_analysis = analyze_vowel_value(game_state, previous_guesses)
    
    # Decision logic based on multiple factors
    decision_score = calculate_decision_score(
        game_state, spin_analysis, vowel_analysis, winnings
    )
    
    if decision_score['buy_vowel'] > decision_score['spin']:
        return 'buy_vowel', decision_score['reasoning']
    else:
        return 'spin', decision_score['reasoning']


def analyze_game_state(showing: str, previous_guesses: List[str]) -> Dict:
    """Analyze the current state of the puzzle."""
    
    total_letters = len(re.sub(r'[^A-Z_]', '', showing))
    blank_count = showing.count('_')
    revealed_count = total_letters - blank_count
    
    # Count vowels and consonants in revealed letters
    revealed_letters = re.sub(r'[^A-Z]', '', showing.replace('_', ''))
    vowels_revealed = sum(1 for c in revealed_letters if c in 'AEIOU')
    consonants_revealed = len(revealed_letters) - vowels_revealed
    
    # Estimate remaining vowels and consonants
    # Based on English letter frequency: ~40% vowels, ~60% consonants
    estimated_total_vowels = max(1, int(total_letters * 0.4))
    estimated_total_consonants = total_letters - estimated_total_vowels
    
    estimated_remaining_vowels = max(0, estimated_total_vowels - vowels_revealed)
    estimated_remaining_consonants = max(0, estimated_total_consonants - consonants_revealed)
    
    return {
        'total_letters': total_letters,
        'blank_count': blank_count,
        'revealed_count': revealed_count,
        'completion_ratio': revealed_count / total_letters if total_letters > 0 else 0,
        'vowels_revealed': vowels_revealed,
        'consonants_revealed': consonants_revealed,
        'estimated_remaining_vowels': estimated_remaining_vowels,
        'estimated_remaining_consonants': estimated_remaining_consonants,
        'vowel_density': estimated_remaining_vowels / blank_count if blank_count > 0 else 0
    }


def analyze_spin_risk() -> Dict:
    """Analyze the risk and expected value of spinning the wheel."""
    
    # Wheel values from the game
    wheel_values = [0, -1, 500, 550, 600, 650, 700, 750, 800, 850, 900, -1, 
                   500, 550, 600, 650, 700, 750, 800, 850, 900, 500, 550, 600]
    
    positive_values = [v for v in wheel_values if v > 0]
    lose_turn_count = wheel_values.count(0)
    bankrupt_count = wheel_values.count(-1)
    
    total_segments = len(wheel_values)
    
    return {
        'expected_value': sum(positive_values) / total_segments,
        'lose_turn_probability': lose_turn_count / total_segments,
        'bankrupt_probability': bankrupt_count / total_segments,
        'success_probability': len(positive_values) / total_segments,
        'average_positive_value': sum(positive_values) / len(positive_values)
    }


def analyze_vowel_value(game_state: Dict, previous_guesses: List[str]) -> Dict:
    """Analyze the expected value of buying a vowel."""
    
    # Common vowel frequencies in English
    vowel_frequencies = {'A': 0.082, 'E': 0.127, 'I': 0.070, 'O': 0.075, 'U': 0.028}
    
    # Filter out already guessed vowels
    available_vowels = {v: f for v, f in vowel_frequencies.items() 
                       if v not in previous_guesses}
    
    if not available_vowels:
        return {'expected_letters': 0, 'probability_of_hit': 0}
    
    # Estimate probability that a vowel will appear
    vowel_density = game_state['vowel_density']
    
    # Most frequent available vowel
    best_vowel_freq = max(available_vowels.values()) if available_vowels else 0
    
    # Expected number of letters revealed by buying a vowel
    expected_letters = vowel_density * game_state['blank_count'] * best_vowel_freq * 2
    
    return {
        'expected_letters': expected_letters,
        'probability_of_hit': min(0.9, vowel_density * 2),  # Cap at 90%
        'available_vowels': len(available_vowels),
        'best_vowel_frequency': best_vowel_freq
    }


def calculate_decision_score(
    game_state: Dict, 
    spin_analysis: Dict, 
    vowel_analysis: Dict, 
    winnings: int
) -> Dict:
    """Calculate scores for each decision option."""
    
    # Base scores
    spin_score = 0
    buy_vowel_score = 0
    
    # Factor 1: Expected value
    # Spinning: expected wheel value * probability of success * estimated consonants
    spin_expected = (spin_analysis['average_positive_value'] * 
                    spin_analysis['success_probability'] * 
                    min(3, game_state['estimated_remaining_consonants']))
    
    # Buying vowel: fixed cost but guaranteed if vowels exist
    vowel_expected = vowel_analysis['expected_letters'] * 100  # Arbitrary value per letter
    
    spin_score += spin_expected * 0.3
    buy_vowel_score += vowel_expected * 0.3
    
    # Factor 2: Risk assessment
    # Penalize spinning if high risk of bankruptcy/lose turn
    risk_penalty = (spin_analysis['bankrupt_probability'] * 500 + 
                   spin_analysis['lose_turn_probability'] * 200)
    spin_score -= risk_penalty * 0.2
    
    # Factor 3: Game stage
    completion = game_state['completion_ratio']
    
    if completion < 0.3:  # Early game - vowels more valuable
        buy_vowel_score += 100
    elif completion > 0.6:  # Late game - spinning for points more valuable
        spin_score += 100
    
    # Factor 4: Vowel density
    if game_state['vowel_density'] > 0.4:  # High vowel density
        buy_vowel_score += 150
    elif game_state['vowel_density'] < 0.2:  # Low vowel density
        spin_score += 100
    
    # Factor 5: Financial situation
    if winnings > 1000:  # Comfortable - can afford risks
        spin_score += 50
    elif winnings < 500:  # Conservative - preserve money for vowels
        buy_vowel_score += 75
    
    # Generate reasoning
    if buy_vowel_score > spin_score:
        reasoning = f"Buy vowel: High vowel density ({game_state['vowel_density']:.2f}), " \
                   f"expected {vowel_analysis['expected_letters']:.1f} letters revealed"
    else:
        reasoning = f"Spin wheel: Expected value ${spin_expected:.0f}, " \
                   f"{spin_analysis['success_probability']:.1%} success rate"
    
    return {
        'spin': spin_score,
        'buy_vowel': buy_vowel_score,
        'reasoning': reasoning
    }


def get_best_vowel_guess(showing: str, previous_guesses: List[str]) -> str:
    """Determine the best vowel to guess based on common patterns."""
    
    vowel_frequencies = {'E': 0.127, 'A': 0.082, 'O': 0.075, 'I': 0.070, 'U': 0.028}
    
    # Filter available vowels
    available_vowels = {v: f for v, f in vowel_frequencies.items() 
                       if v not in previous_guesses}
    
    if not available_vowels:
        return 'E'  # Fallback
    
    # Return most frequent available vowel
    return max(available_vowels.keys(), key=lambda x: available_vowels[x])


def get_best_consonant_guess(showing: str, previous_guesses: List[str]) -> str:
    """Determine the best consonant to guess based on patterns and frequency."""
    
    # Common consonant frequencies
    consonant_frequencies = {
        'T': 0.091, 'N': 0.067, 'S': 0.063, 'H': 0.061, 'R': 0.060,
        'D': 0.043, 'L': 0.040, 'C': 0.028, 'M': 0.024, 'W': 0.024,
        'F': 0.022, 'G': 0.020, 'Y': 0.020, 'P': 0.019, 'B': 0.013,
        'V': 0.010, 'K': 0.008, 'J': 0.001, 'X': 0.001, 'Q': 0.001, 'Z': 0.001
    }
    
    # Filter available consonants
    available_consonants = {c: f for c, f in consonant_frequencies.items() 
                           if c not in previous_guesses}
    
    if not available_consonants:
        return 'T'  # Fallback
    
    # Return most frequent available consonant
    return max(available_consonants.keys(), key=lambda x: available_consonants[x])


# Example usage and testing
if __name__ == "__main__":
    # Test scenarios
    test_scenarios = [
        {
            'showing': 'T_E _U_C_ _RO__ _O_',
            'winnings': 800,
            'previous_guesses': ['T', 'E', 'C', 'O'],
            'description': 'Mid-game with some vowels revealed'
        },
        {
            'showing': '_ _ _ _ _',
            'winnings': 300,
            'previous_guesses': [],
            'description': 'Early game, fresh puzzle'
        },
        {
            'showing': 'TH_ QU_CK _RO_N _O_',
            'winnings': 1500,
            'previous_guesses': ['T', 'H', 'Q', 'U', 'C', 'K', 'R', 'O', 'N'],
            'description': 'Late game, nearly complete'
        }
    ]
    
    print("Smart Decision Function Test Results:")
    print("=" * 50)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nScenario {i}: {scenario['description']}")
        print(f"Puzzle: {scenario['showing']}")
        print(f"Winnings: ${scenario['winnings']}")
        print(f"Previous guesses: {scenario['previous_guesses']}")
        
        decision, reasoning = should_spin_or_buy_vowel(
            scenario['showing'],
            scenario['winnings'],
            scenario['previous_guesses']
        )
        
        print(f"Decision: {decision.upper()}")
        print(f"Reasoning: {reasoning}")
        
        if decision == 'buy_vowel':
            best_vowel = get_best_vowel_guess(scenario['showing'], scenario['previous_guesses'])
            print(f"Recommended vowel: {best_vowel}")
        elif decision == 'spin':
            best_consonant = get_best_consonant_guess(scenario['showing'], scenario['previous_guesses'])
            print(f"Recommended consonant: {best_consonant}")