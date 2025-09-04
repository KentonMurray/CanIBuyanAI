# Smart Decision Function for Wheel of Fortune

This document explains the intelligent decision-making system implemented for Wheel of Fortune gameplay.

## Overview

The smart decision function (`smart_decision.py`) analyzes the current game state and makes optimal decisions about whether to spin the wheel or buy a vowel. It considers multiple factors including game progression, risk assessment, expected values, and strategic positioning.

## Key Features

### 1. Game State Analysis
- **Completion Ratio**: Tracks how much of the puzzle is revealed
- **Letter Distribution**: Analyzes vowel vs consonant density
- **Blank Count**: Considers remaining letters to be guessed
- **Pattern Recognition**: Estimates remaining vowels and consonants

### 2. Risk Assessment
- **Wheel Analysis**: Calculates expected value, bankruptcy risk, and success probability
- **Financial Planning**: Considers current winnings vs vowel costs ($250)
- **Turn Optimization**: Balances risk vs reward based on game stage

### 3. Strategic Decision Making
- **Early Game**: Prioritizes vowels for maximum puzzle revelation
- **Mid Game**: Balances vowel purchases with strategic spinning
- **Late Game**: Focuses on high-value spins or puzzle solving

## Player Types

### Smart Player (`smart`)
Uses the core decision algorithm with balanced risk assessment.

**Decision Factors:**
- Expected value calculations
- Risk-reward analysis
- Game stage optimization
- Financial management

### Conservative Player (`conservative`)
More likely to buy vowels and preserve winnings.

**Characteristics:**
- Buys vowels when funds allow and blanks remain
- Avoids high-risk spins early in the game
- Prioritizes puzzle completion over point maximization

### Aggressive Player (`aggressive`)
More likely to spin for higher rewards.

**Characteristics:**
- Prefers spinning unless vowel density is very high
- Takes calculated risks for higher point values
- Optimizes for maximum winnings

## Decision Algorithm

### Step 1: Financial Check
```python
if winnings < 250:
    return 'spin'  # Must spin if can't afford vowel
```

### Step 2: Completion Analysis
```python
if completion_ratio > 0.8:
    return 'solve'  # Consider solving if nearly complete
```

### Step 3: Multi-Factor Scoring
The algorithm scores both options based on:

1. **Expected Value** (30% weight)
   - Spin: `wheel_expected_value × success_probability × remaining_consonants`
   - Vowel: `expected_letters_revealed × value_per_letter`

2. **Risk Assessment** (20% weight)
   - Bankruptcy probability penalty
   - Lose turn probability penalty

3. **Game Stage** (varies)
   - Early game: +100 points for vowel buying
   - Late game: +100 points for spinning

4. **Vowel Density** (varies)
   - High density (>40%): +150 points for vowel buying
   - Low density (<20%): +100 points for spinning

5. **Financial Situation** (varies)
   - High winnings (>$1000): +50 points for spinning
   - Low winnings (<$500): +75 points for vowel buying

### Step 4: Letter Selection
- **Best Vowel**: Selected by frequency (E > A > O > I > U)
- **Best Consonant**: Selected by frequency (T > N > S > H > R > ...)

## Usage Examples

### Basic Usage
```python
from smart_decision import should_spin_or_buy_vowel

decision, reasoning = should_spin_or_buy_vowel(
    showing="T_E _U_C_ _RO__ _O_",
    winnings=800,
    previous_guesses=['T', 'E', 'C', 'O']
)

print(f"Decision: {decision}")
print(f"Reasoning: {reasoning}")
```

### Integration with Game
```python
from smart_player import computer_turn_smart

# In game loop
if player_type == "smart":
    guess, dollar = computer_turn_smart(showing, winnings, previous_guesses, turn)
```

## Performance Characteristics

### Advantages
- **Data-Driven**: Decisions based on statistical analysis
- **Adaptive**: Adjusts strategy based on game state
- **Risk-Aware**: Considers probability of negative outcomes
- **Flexible**: Multiple player personalities available

### Considerations
- **Complexity**: More computationally intensive than simple strategies
- **Tuning**: Decision weights may need adjustment based on testing
- **Context**: Optimized for standard Wheel of Fortune rules

## Testing

Run the test suite to see the decision function in action:

```bash
cd src/PlayGame
python3 smart_decision.py
```

This will show decisions for various game scenarios with detailed reasoning.

## Future Enhancements

Potential improvements to the decision system:

1. **Machine Learning**: Train on historical game data
2. **Opponent Modeling**: Consider other players' strategies
3. **Dynamic Tuning**: Adjust weights based on success rates
4. **Puzzle Category**: Factor in puzzle type (phrase, person, etc.)
5. **Advanced Patterns**: Use n-gram analysis for better letter prediction

## Integration Notes

The smart decision system is designed to be:
- **Modular**: Easy to integrate with existing game code
- **Extensible**: Simple to add new decision factors
- **Configurable**: Player personalities can be easily modified
- **Testable**: Comprehensive test scenarios included

For questions or improvements, see the source code in `smart_decision.py` and `smart_player.py`.