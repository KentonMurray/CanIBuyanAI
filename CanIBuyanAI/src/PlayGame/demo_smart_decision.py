#!/usr/bin/env python3
"""
Demonstration of the Smart Decision Function for Wheel of Fortune

This script shows how the smart decision function works with various game scenarios.
"""

try:
    from smart_decision import (
        should_spin_or_buy_vowel,
        get_best_vowel_guess,
        get_best_consonant_guess,
        estimate_solution_distribution,
        compute_spin_expected_cash,
        analyze_spin_risk,
        analyze_game_state,
        analyze_vowel_value,
    )
except Exception:
    # Support running as a module from repo root
    from src.PlayGame.smart_decision import (
        should_spin_or_buy_vowel,
        get_best_vowel_guess,
        get_best_consonant_guess,
        estimate_solution_distribution,
        compute_spin_expected_cash,
        analyze_spin_risk,
        analyze_game_state,
        analyze_vowel_value,
    )
import random
import time
import re


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


def run_telemetry_demo(rounds: int = 5):
    """Run multiple rounds for each scenario and show telemetry each time."""
    scenarios = [
        {
            'name': 'Early Game - Fresh Puzzle',
            'showing': '_ _ _ _ _ _ _ _',
            'winnings': 0,
            'previous_guesses': [],
        },
        {
            'name': 'Mid Game - Some Letters Revealed',
            'showing': 'T_E _U_C_ _RO__ _O_',
            'winnings': 800,
            'previous_guesses': ['T', 'E', 'C', 'O'],
        },
        {
            'name': 'Late Game - Almost Complete',
            'showing': 'THE QUICK _RO_N _O_',
            'winnings': 1200,
            'previous_guesses': ['T', 'H', 'E', 'Q', 'U', 'I', 'C', 'K', 'R', 'O', 'N'],
        },
    ]

    print("\nRunning telemetry demo — multiple rounds per scenario")
    print("=" * 70)

    for scenario in scenarios:
        print(f"\nScenario: {scenario['name']}")
        for r in range(1, rounds + 1):
            # Randomize simple opponent state to show competitive effect
            opponents = [random.randint(0, 1500), random.randint(0, 1500)]

            # Call the decision function with competitive context
            decision, reasoning = should_spin_or_buy_vowel(
                scenario['showing'], scenario['winnings'], scenario['previous_guesses'],
                opponents_winnings=opponents, strategy='optimized'
            )

            # Telemetry: confidence, spin EV, analysis
            sol_dist = estimate_solution_distribution(scenario['showing'], scenario['previous_guesses'])
            confidence = sol_dist.get('top_probability', 0.0)
            spin_analysis = analyze_spin_risk()
            vowel_analysis = analyze_vowel_value(
                analyze_game_state(scenario['showing'], scenario['previous_guesses']),
                scenario['previous_guesses']
            )
            spin_ev = compute_spin_expected_cash(
                analyze_game_state(scenario['showing'], scenario['previous_guesses']), spin_analysis
            )

            # Expected utilities (mirrors decision logic)
            expected_downside = (
                spin_analysis['bankrupt_probability'] * scenario['winnings'] +
                spin_analysis['lose_turn_probability'] * (scenario['winnings'] * 0.1)
            )
            spin_utility = spin_ev - expected_downside
            vowel_utility = vowel_analysis.get('expected_letters', 0) * 80 - 250

            print(f"Round {r}: decision={decision.upper()} | reason={reasoning}")
            print(f"  Confidence: {confidence:.1%} | Spin EV: ${spin_ev:.0f} | Spin util: ${spin_utility:.0f} | Vowel util: ${vowel_utility:.0f}")
            print(f"  Wheel: bankrupt={spin_analysis['bankrupt_probability']:.1%}, lose-turn={spin_analysis['lose_turn_probability']:.1%}, success={spin_analysis['success_probability']:.1%}")
            print(f"  Vowel expected letters: {vowel_analysis.get('expected_letters',0):.2f} | available vowels: {vowel_analysis.get('available_vowels',0)}")
            print(f"  Opponents: {opponents}")
            time.sleep(0.15)


def _reveal_letter(showing: str, puzzle: str, letter: str):
    """Reveal all occurrences of `letter` in `puzzle` into `showing`.

    showing and puzzle are strings of equal length (spaces included).
    Returns tuple (new_showing, count_revealed).
    """
    showing_list = list(showing)
    count = 0
    # Normalize inputs
    p = puzzle.upper()
    for i, ch in enumerate(p):
        if ch == letter and showing_list[i] == '_':
            showing_list[i] = letter
            count += 1
    return ''.join(showing_list), count


def run_simulated_game(puzzle: str, player_types=None, max_turns: int = 200):
    """Simulate a short 3-player game demonstrating the decision logic.

    - `puzzle` should be the full solution (letters and spaces).
    - `player_types` is a list like ['smart','random','random'].
    """
    if player_types is None:
        player_types = ['smart', 'random', 'random']

    random.seed(0)

    # Normalize puzzle and showing
    puzzle_norm = re.sub(r'[^A-Z ]', '', puzzle.upper())
    showing = ''.join('_' if ch != ' ' else ' ' for ch in puzzle_norm)

    previous_guesses = []
    winnings = [0, 0, 0]
    wheel_values = [0, -1, 500, 550, 600, 650, 700, 750, 800, 850, 900, -1,
                   500, 550, 600, 650, 700, 750, 800, 850, 900, 500, 550, 600]

    print('\nStarting simulated game:')
    print(f'Puzzle: {puzzle_norm}')
    print(f'Starting showing: {showing}')

    turn = 0
    for t in range(max_turns):
        cur = turn % 3
        ptype = player_types[cur] if cur < len(player_types) else 'random'
        player_w = winnings[cur]

        # Build opponents list
        opponents = [w for i, w in enumerate(winnings) if i != cur]

        # Ask smart decision function for action if smart
        if ptype == 'smart':
            decision, reasoning = should_spin_or_buy_vowel(showing, player_w, previous_guesses, opponents_winnings=opponents, strategy='optimized')
        elif ptype == 'conservative':
            # simple conservative heuristic
            decision = 'buy_vowel' if player_w >= 250 and showing.count('_') > 3 else 'spin'
            reasoning = 'Conservative fallback'
        else:  # random
            # random player: prefer spin, sometimes buy vowel if can
            if player_w >= 250 and random.random() < 0.2:
                decision = 'buy_vowel'
            else:
                decision = 'spin'
            reasoning = 'Random fallback'

        # Execute decision
        print(f"Turn {t+1}: Player {cur} ({ptype}) decides: {decision.upper()} — {reasoning}")

        if decision == 'solve':
            # Try solve: if we're very close (>=90% revealed) accept solve for demo
            gs = analyze_game_state(showing, previous_guesses)
            if gs.get('completion_ratio', 0) >= 0.9:
                print(f"Player {cur} solved (forced) and wins ${winnings[cur]}!")
                return
            # Otherwise attempt to pick top candidate from corpus
            sol = estimate_solution_distribution(showing, previous_guesses)
            candidates = sol.get('candidates', [])
            top = candidates[0][0] if candidates else ''
            if top and top.replace(' ', '') == puzzle_norm.replace(' ', ''):
                print(f"Player {cur} solved correctly with '{top}' and wins ${winnings[cur]}!")
                return
            else:
                print(f"Player {cur} attempted to solve with '{top}' and was incorrect.")
                # incorrect solve -> lose turn
        elif decision == 'buy_vowel':
            # Buy vowel
            if winnings[cur] < 250:
                print(f"Player {cur} cannot afford a vowel.")
            else:
                winnings[cur] -= 250
                vowel = get_best_vowel_guess(showing, previous_guesses)
                previous_guesses.append(vowel)
                showing, found = _reveal_letter(showing, puzzle_norm, vowel)
                print(f"Player {cur} bought vowel '{vowel}' — found {found} occurrences. Winnings now ${winnings[cur]}")
                if showing.replace(' ', '') == puzzle_norm.replace(' ', ''):
                    print(f"Player {cur} completed the puzzle and wins ${winnings[cur]}!")
                    return
        elif decision == 'spin':
            landed = random.choice(wheel_values)
            if landed == 0:
                print(f"Player {cur} spun LOSE A TURN (0).")
            elif landed == -1:
                print(f"Player {cur} spun BANKRUPT! Winnings reset to $0.")
                winnings[cur] = 0
            else:
                consonant = get_best_consonant_guess(showing, previous_guesses)
                previous_guesses.append(consonant)
                showing, found = _reveal_letter(showing, puzzle_norm, consonant)
                if found > 0:
                    winnings[cur] += landed * found
                    print(f"Player {cur} guessed consonant '{consonant}' and found {found} -> +${landed*found} (winnings ${winnings[cur]})")
                    if showing.replace(' ', '') == puzzle_norm.replace(' ', ''):
                        print(f"Player {cur} completed the puzzle and wins ${winnings[cur]}!")
                        return
                else:
                    print(f"Player {cur} guessed consonant '{consonant}' and it was not in the puzzle.")
        else:
            print(f"Player {cur} chose unknown action '{decision}'.")

        turn += 1

    print('Max turns reached. Final state:')
    print(f'Showing: {showing}')
    print(f'Winnings: {winnings}')


if __name__ == "__main__":
    demo_decision_function()
    print("\n" + "=" * 60)
    print("Running a short simulated game with one smart player...")
    # pick a puzzle for deterministic demo
    test_puzzle = 'THE QUICK BROWN FOX'
    run_simulated_game(test_puzzle, player_types=['smart', 'random', 'random'], max_turns=200)
    print("\nDemo finished. To experiment interactively, call run_simulated_game(...).")