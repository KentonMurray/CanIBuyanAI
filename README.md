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

- Player types: `human`, `morse`, `oxford`, `trigram`
- As a human, you’ll be prompted each turn: 1 = Spin, 2 = Buy Vowel, 3 = Solve
- Run from the `src/PlayGame` directory so relative paths resolve (uses `../../data/puzzles/valid.csv` and `bigrams.txt`)

Example:
```bash
cd src/PlayGame
python3 play_random_puzzle.py human morse oxford
# or, let it pick defaults if you omit/shorten the args
python3 play_random_puzzle.py
```

