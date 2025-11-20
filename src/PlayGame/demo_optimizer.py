#!/usr/bin/env python3
"""
Demo script showcasing the advanced AI optimization features for Wheel of Fortune.

This script demonstrates:
1. Comprehensive probability analysis
2. Risk vs reward calculations
3. Competitive positioning analysis
4. Strategic recommendations for different game scenarios
5. Human-friendly suggestion interface
"""

import sys
import time
from ai_optimizer import WheelOfFortuneOptimizer, GameState, format_recommendation_for_human
from optimized_player import OptimizedPlayer


def demo_probability_analysis():
    """Demonstrate the probability analysis capabilities."""
    print("🎰 WHEEL PROBABILITY ANALYSIS")
    print("=" * 50)
    
    optimizer = WheelOfFortuneOptimizer()
    wheel_analysis = optimizer.analyze_wheel_probabilities()
    
    print(f"Expected Value per Spin: ${wheel_analysis.expected_value:.2f}")
    print(f"Success Probability: {wheel_analysis.success_probability:.1%}")
    print(f"Bankruptcy Risk: {wheel_analysis.bankruptcy_probability:.1%}")
    print(f"Lose Turn Risk: {wheel_analysis.lose_turn_probability:.1%}")
    print(f"High Value (>$700) Probability: {wheel_analysis.high_value_probability:.1%}")
    print(f"Average Positive Value: ${wheel_analysis.average_positive_value:.0f}")
    print(f"Overall Risk Score: {wheel_analysis.risk_score:.3f}")
    
    print("\n💡 Key Insights:")
    print(f"  • You have an {wheel_analysis.success_probability:.1%} chance of landing on a positive value")
    print(f"  • Risk of losing everything: {wheel_analysis.bankruptcy_probability:.1%}")
    print(f"  • Risk of losing turn: {wheel_analysis.lose_turn_probability:.1%}")
    print(f"  • Expected gain per successful spin: ${wheel_analysis.average_positive_value:.0f}")


def demo_competitive_analysis():
    """Demonstrate competitive positioning analysis."""
    print("\n\n🏆 COMPETITIVE ANALYSIS")
    print("=" * 50)
    
    scenarios = [
        {
            'name': 'Leading Position',
            'winnings': [1500, 800, 600],
            'player': 0
        },
        {
            'name': 'Trailing Slightly',
            'winnings': [800, 1200, 600],
            'player': 0
        },
        {
            'name': 'Trailing Badly',
            'winnings': [300, 1800, 1500],
            'player': 0
        }
    ]
    
    optimizer = WheelOfFortuneOptimizer()
    
    for scenario in scenarios:
        print(f"\n📊 {scenario['name']}:")
        print(f"Winnings: {scenario['winnings']}")
        
        game_state = GameState(
            showing="T_E _U_C_ _RO__ _O_",
            puzzle="",
            winnings=scenario['winnings'],
            previous_guesses=['T', 'E', 'C', 'O'],
            current_player=scenario['player'],
            turn_number=4
        )
        
        comp_analysis = optimizer.analyze_competitive_position(game_state)
        
        print(f"  Position: {comp_analysis['relative_position'].upper()}")
        print(f"  Gap to leader: ${abs(comp_analysis['winnings_gap'])}")
        print(f"  Pressure level: {comp_analysis['pressure_level'].upper()}")
        print(f"  Urgency factor: {comp_analysis['urgency_factor']:.2f}")


def demo_strategic_recommendations():
    """Demonstrate strategic recommendations for different scenarios."""
    print("\n\n🧠 STRATEGIC RECOMMENDATIONS")
    print("=" * 50)
    
    scenarios = [
        {
            'name': 'Early Game - Fresh Start',
            'showing': '_ _ _ _ _ _ _ _',
            'winnings': [0, 0, 0],
            'previous_guesses': [],
            'description': 'Beginning of the game, no letters guessed yet'
        },
        {
            'name': 'Mid Game - Vowel Heavy',
            'showing': '_A_E _O_E _O_E_',
            'winnings': [600, 800, 400],
            'previous_guesses': ['A', 'E', 'O'],
            'description': 'Many vowels revealed, consonants needed'
        },
        {
            'name': 'Late Game - Nearly Complete',
            'showing': 'THE QUICK _RO_N _O_',
            'winnings': [1200, 1000, 800],
            'previous_guesses': ['T', 'H', 'E', 'Q', 'U', 'I', 'C', 'K', 'R', 'O', 'N'],
            'description': 'Puzzle almost complete, solve decision critical'
        },
        {
            'name': 'High Stakes - Trailing',
            'showing': '_E_ _OR_ _A__',
            'winnings': [400, 2000, 1800],
            'previous_guesses': ['E', 'O', 'R', 'A'],
            'description': 'Trailing significantly, need aggressive play'
        }
    ]
    
    optimizer = WheelOfFortuneOptimizer()
    
    for i, scenario in enumerate(scenarios):
        print(f"\n🎯 Scenario {i+1}: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Puzzle: {scenario['showing']}")
        print(f"Winnings: {scenario['winnings']}")
        print(f"Previous Guesses: {scenario['previous_guesses']}")
        
        game_state = GameState(
            showing=scenario['showing'],
            puzzle="",
            winnings=scenario['winnings'],
            previous_guesses=scenario['previous_guesses'],
            current_player=0,
            turn_number=len(scenario['previous_guesses'])
        )
        
        recommendation = optimizer.get_optimal_recommendation(game_state)
        
        # Show condensed recommendation
        action_emoji = {'spin': '🎰', 'buy_vowel': '💰', 'solve': '🧩'}
        print(f"\n{action_emoji.get(recommendation.action, '❓')} RECOMMENDATION: {recommendation.action.replace('_', ' ').upper()}")
        print(f"Confidence: {recommendation.confidence:.1%} | Risk: {recommendation.risk_level.upper()} | Expected: ${recommendation.expected_gain:.0f}")
        
        # Show top 2 reasons
        for j, reason in enumerate(recommendation.reasoning[:2]):
            print(f"  {j+1}. {reason}")
        
        if recommendation.letter_suggestion:
            print(f"  💡 Suggested letter: {recommendation.letter_suggestion}")


def demo_player_personalities():
    """Demonstrate different AI player personalities."""
    print("\n\n🎭 AI PLAYER PERSONALITIES")
    print("=" * 50)
    
    # Test scenario
    showing = "T_E _U_C_ _RO__ _O_"
    winnings = [800, 1200, 600]  # Player is trailing
    previous_guesses = ['T', 'E', 'C', 'O']
    turn = 0
    
    print(f"Test Scenario:")
    print(f"  Puzzle: {showing}")
    print(f"  Winnings: {winnings} (Player 0 is trailing)")
    print(f"  Previous Guesses: {previous_guesses}")
    
    personalities = [
        ('Balanced', 'balanced'),
        ('Conservative', 'conservative'),
        ('Aggressive', 'aggressive')
    ]
    
    for name, personality in personalities:
        print(f"\n🤖 {name} AI Player:")
        
        player = OptimizedPlayer(personality)
        
        # Create game state for analysis
        game_state = GameState(
            showing=showing,
            puzzle="",
            winnings=winnings,
            previous_guesses=previous_guesses,
            current_player=0,
            turn_number=4
        )
        
        # Get base recommendation
        recommendation = player.optimizer.get_optimal_recommendation(game_state)
        
        # Apply personality adjustments
        adjusted_action = player._apply_personality_adjustments(recommendation, game_state)
        
        print(f"  Base recommendation: {recommendation.action}")
        print(f"  Personality adjustment: {adjusted_action}")
        print(f"  Reasoning: {personality.title()} players tend to...")
        
        if personality == 'conservative':
            print("    • Preserve winnings and avoid high-risk spins")
            print("    • Buy vowels when affordable for steady progress")
            print("    • Solve only when very confident")
        elif personality == 'aggressive':
            print("    • Take calculated risks for higher rewards")
            print("    • Spin more often to maximize point potential")
            print("    • Solve earlier when trailing to catch up")
        else:  # balanced
            print("    • Balance risk and reward based on game state")
            print("    • Adapt strategy to competitive position")
            print("    • Make data-driven decisions")


def demo_human_suggestions():
    """Demonstrate the human suggestion interface."""
    print("\n\n👤 HUMAN PLAYER SUGGESTIONS")
    print("=" * 50)
    
    print("This is what a human player would see when requesting AI assistance:")
    
    # Example scenario
    showing = "_A_E _O_E _O_E_"
    winnings = [400, 1200, 800]
    previous_guesses = ['A', 'E', 'O']
    turn = 0
    
    game_state = GameState(
        showing=showing,
        puzzle="",
        winnings=winnings,
        previous_guesses=previous_guesses,
        current_player=0,
        turn_number=3
    )
    
    optimizer = WheelOfFortuneOptimizer()
    recommendation = optimizer.get_optimal_recommendation(game_state)
    
    # Show the formatted suggestion
    suggestion = format_recommendation_for_human(recommendation, detailed=True)
    print(suggestion)


def demo_risk_reward_analysis():
    """Demonstrate detailed risk vs reward analysis."""
    print("\n\n⚖️ RISK VS REWARD ANALYSIS")
    print("=" * 50)
    
    optimizer = WheelOfFortuneOptimizer()
    
    # Different financial situations
    scenarios = [
        {'winnings': 100, 'desc': 'Low funds - high bankruptcy risk'},
        {'winnings': 500, 'desc': 'Moderate funds - balanced approach'},
        {'winnings': 1500, 'desc': 'High funds - can afford risks'}
    ]
    
    showing = "T_E _U_C_ _RO__ _O_"
    previous_guesses = ['T', 'E', 'C', 'O']
    
    for scenario in scenarios:
        print(f"\n💰 {scenario['desc']} (${scenario['winnings']})")
        
        game_state = GameState(
            showing=showing,
            puzzle="",
            winnings=[scenario['winnings'], 800, 600],
            previous_guesses=previous_guesses,
            current_player=0,
            turn_number=4
        )
        
        # Calculate expected values
        wheel_analysis = optimizer.analyze_wheel_probabilities()
        letter_analysis = optimizer.analyze_letters(game_state)
        
        spin_ev = optimizer.calculate_spin_expected_value(game_state, wheel_analysis, letter_analysis)
        vowel_ev = optimizer.calculate_vowel_expected_value(game_state, letter_analysis)
        solve_ev = optimizer.calculate_solve_expected_value(game_state)
        
        print(f"  Spin Expected Value: ${spin_ev:.0f}")
        print(f"  Vowel Expected Value: ${vowel_ev:.0f}")
        print(f"  Solve Expected Value: ${solve_ev:.0f}")
        
        # Risk analysis
        bankruptcy_loss = scenario['winnings'] * wheel_analysis.bankruptcy_probability
        print(f"  Potential Bankruptcy Loss: ${bankruptcy_loss:.0f}")
        print(f"  Risk-Adjusted Spin Value: ${spin_ev - bankruptcy_loss:.0f}")


def main():
    """Run the complete demo."""
    print("🎰 WHEEL OF FORTUNE AI OPTIMIZER DEMONSTRATION")
    print("=" * 60)
    print("This demo showcases the advanced AI optimization features that help")
    print("players make strategic decisions in Wheel of Fortune.")
    print("=" * 60)
    
    # Run all demos
    demo_probability_analysis()
    demo_competitive_analysis()
    demo_strategic_recommendations()
    demo_player_personalities()
    demo_human_suggestions()
    demo_risk_reward_analysis()
    
    print("\n\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("The AI optimizer provides:")
    print("✅ Comprehensive probability analysis")
    print("✅ Risk vs reward calculations")
    print("✅ Competitive positioning insights")
    print("✅ Strategic recommendations")
    print("✅ Multiple AI personalities")
    print("✅ Human-friendly suggestions")
    print("✅ Real-time decision support")
    
    print("\nTo use in the game:")
    print("• Run: python3 play_random_puzzle.py human optimized opt_conservative")
    print("• Choose option 4 during your turn for AI suggestions")
    print("• Try different AI player types: optimized, opt_aggressive, opt_conservative")


if __name__ == "__main__":
    main()