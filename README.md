# CanIBuyanAI
This project tries to solve Wheel of Fortune puzzles.

## Requirements
Tested using Python 3.6.

## Scraper
See the [Puzzle Scraper README](./src/PuzzleScraper/README.md) for details.

Install the scraper dependencies:
```bash
pip install requests beautifulsoup4
```
## How to Play

Play a random Wheel of Fortune puzzle against simple computer strategies using [play_random_puzzle.py](./src/PlayGame/play_random_puzzle.py).

- Player types: `human`, `morse`, `oxford`, `trigram`, `smart`, `conservative`, `aggressive`
- As a human, you’ll be prompted each turn: 1 = Spin, 2 = Buy Vowel, 3 = Solve
- Smart AI players (`smart`, `conservative`, `aggressive`) use advanced decision-making logic to optimize spin vs buy vowel choices
- Run from the `src/PlayGame` directory so relative paths resolve (uses `../../data/puzzles/valid.csv` and `bigrams.txt`)

Example:
```bash
cd src/PlayGame
python3 play_random_puzzle.py human morse oxford
# or, let it pick defaults if you omit/shorten the args
python3 play_random_puzzle.py
```

Tip: To visualize the wheel segment values used by the game, see the [ASCII Wheel](#ascii-wheel-optional) section below.

## 🆕 NEW: Advanced AI Optimization Features

This project now includes a comprehensive AI optimization system that provides strategic suggestions for Wheel of Fortune gameplay!

### 🤖 Optimized AI Players

Three new AI player types with advanced decision-making:
- `optimized` - Balanced strategy with comprehensive analysis
- `opt_conservative` - Risk-averse approach, preserves winnings
- `opt_aggressive` - High-risk/high-reward strategy

### 🧠 AI Features

**Probability Analysis:**
- Calculates exact wheel spin probabilities (bankruptcy: 8.3%, lose turn: 4.2%, success: 87.5%)
- Expected value calculations for all possible actions
- Risk vs reward analysis based on current game state

**Strategic Analysis:**
- Competitive positioning (leading vs trailing analysis)
- Optimal timing for solving puzzles
- Letter frequency analysis and recommendations
- Financial impact assessment

**Human Player Support:**
- Press **4** during your turn to get AI suggestions
- Detailed reasoning for each recommendation
- Confidence scores and risk levels
- Alternative action suggestions

### 🎯 Quick Start with Optimized AI

```bash
cd src/PlayGame

# Play against optimized AI with suggestions
python3 play_random_puzzle.py human optimized opt_conservative

# Demo all optimization features
python3 demo_optimizer.py

# Test different AI personalities
python3 optimized_player.py
```

### 📊 What the AI Considers

The optimization system analyzes:
- **Wheel Probabilities**: Bankruptcy risk, lose turn risk, expected values
- **Letter Analysis**: Frequency-based recommendations for vowels and consonants  
- **Competitive Position**: Your standing vs opponents, urgency factors
- **Game Stage**: Early game (vowel focus) vs late game (solving focus)
- **Financial Situation**: Risk tolerance based on current winnings
- **Puzzle Completion**: Optimal timing for solve attempts

Try it out and see how the AI can help optimize your Wheel of Fortune strategy!

## ASCII Wheel (Optional)

Render an ASCII-art wheel of the segment values:

```bash
cd src/PlayGame
python3 ascii_wheel.py --label short
# long labels (BANKRUPT / LOSE TURN) and a larger radius
python3 ascii_wheel.py --label long --radius 14
# custom values
python3 ascii_wheel.py --values "0,-1,500,550,600,650,700,750,800,850,900,-1,500,550,600,650,700,750,800,850,900,500,550,600"
```

