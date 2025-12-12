Andy-Li15: summarize all the parts of this file

GitHub Copilot: I'll create a short todo list and then read the file to summarize its parts.

Created 3 todos

Read [](file:///home/li126/CanIBuyanAI/src/PlayGame/play_random_puzzle.py)

Now that I've read the file, I'll mark exploration done and start summarizing its sections.

Starting: *Summarize sections* (2/3)

**Summary of play_random_puzzle.py**

**Purpose:**  
- Runs a Wheel-of-Fortune style single-round game using puzzles from `../../data/puzzles/valid.csv`. Supports human and several computer player strategies.

**Imports:**  
- `random, re, sys, time` : standard utilities for randomness, regex, argv, delays.  
- `ascii_wheel` : draws a wheel (used by `spin_wheel`).  
- `smart_player` : imports three strategies: `computer_turn_smart`, `computer_turn_smart_conservative`, `computer_turn_smart_aggressive`.

**Helper predicates / small utilities:**  
- `is_consonant(guess)`: returns True if `guess` in consonant string.  
- `is_vowel(guess)`: returns True if `guess` in "AEIOU".  
- `print_board(showing)`: prints the current masked puzzle with spaces between letters.  
- `spin_wheel()`: displays wheel animation with `ascii_wheel.draw_ascii_wheel`, chooses a random wheel value from `wheel_values`, and returns it. Uses `time.sleep(2)` for drama. Wheel values include `0` (lose a turn), `-1` (bankrupt), and dollar amounts.

**Puzzle source:**  
- `get_random_puzzle()`: opens `../../data/puzzles/valid.csv`, chooses a random line (random int 0..900), parses `puzzle, clue, date, game_type`, decodes `&amp;` HTML entities, and returns the tuple.

**Human interaction:**  
- `human_turn(showing, winnings, previous_guesses, turn, puzzle)`: prompts user to choose Spin / Buy Vowel / Solve.  
  - For Solve: reads string; if correct, prints win and calls `exit()`.  
  - For Buy Vowel: deducts 250 from player's winnings and prompts for a vowel.  
  - For Spin: calls `spin_wheel` and then prompts for a consonant; handles `0` and `-1` outcomes.  
  - Returns `(guess, dollar)` where `guess` is the letter guessed (or "_" for failed/bankrupt) and `dollar` is wheel outcome.

**Computer player strategies (multiple variants):**  
- Simple ordered strategies:
  - `computer_turn(showing, winnings, previous_guesses, turn)`: iterates `A..Z` and picks the first unguessed letter; buys vowels only if player has >= 250. Spins the wheel for consonants.
  - `computer_turn_morse(...)`: same logic but uses frequency order `"ETAINOSHRDLUCMFWYGPBVKQJXZ"`.
  - `computer_turn_oxford(...)`: uses `"EARIOTNSLCUDPMHGBFYWKVXZJQ"` order (Oxford-derived).
- Context-aware strategy:
  - `computer_turn_trigrams_bigrams(...)`: more advanced:
    - Builds candidate trigrams and bigrams from the current masked `showing`.
    - Tries common trigrams first (list hard-coded), matching patterns like `"AB_"`.
    - Falls back to bigrams loaded from `bigrams.txt` (reads first 128 bigrams from that file).
    - If still nothing, backs off to unigram frequency (same alphabet as Oxford).
    - Decides whether vowels are allowed based on player's current winnings (>=250).
    - Handles wheel outcomes and bankrupt/lose-a-turn logic similarly to other computer turns.
- Smart players:
  - Delegated to functions imported from `smart_player`: `computer_turn_smart`, `computer_turn_smart_conservative`, `computer_turn_smart_aggressive` and invoked in the main loop when `type_of_players` selects `"smart"`, `"conservative"`, or `"aggressive"`.

**Main game loop / orchestration:**  
- `play_random_game(type_of_players)`: core of the game:
  - Fetches a random puzzle and prints clue and masked puzzle (replaces letters with `_`).
  - Tracks `previous_guesses`, `winnings` (list of 3 ints), `turn` index, `is_solved`.
  - Loop: while `showing != puzzle`:
    - Determine player type for current turn (`type_of_players[turn % 3]`).
    - Call appropriate turn function (human or chosen computer strategy) to get `(guess, dollar)`.
    - Skip already-guessed letters (except `_`), otherwise append guess to `previous_guesses`.
    - Find positions where `puzzle` equals `guess` and update `showing` accordingly.
    - Update winnings for the current player: `winnings[(turn % 3)] += dollar * number_of_occurrences`.
    - Print current `winnings`, `previous_guesses`, clue, and board.
  - After masked equals puzzle, offers final solve attempts in turn order until someone solves (humans prompted; computer players automatically "solve" by using the current `showing`).

**Command-line entrypoint:**  
- If run as `__main__`, reads `sys.argv[1:]` as `type_of_players`. If not exactly 3 players provided, prints help and sets default `["human","smart","conservative"]` after a short sleep, then calls `play_random_game(type_of_players)`.

**External files / dependencies used by this script:**  
- `../../data/puzzles/valid.csv` : puzzle source.  
- `bigrams.txt` (in same folder as this script) : used by trigram/bigram strategy.  
- `ascii_wheel` module : for wheel drawing.  
- `smart_player` module : for alternate AI strategies.

**Notable behaviors, assumptions, and TODOs / caveats:**  
- Buying a vowel always costs 250 and is allowed only when player has >= 250 (this check is done in several places).  
- The script uses `exit()` in `human_turn` when a human correctly solves (abrupt termination). There's a `# TODO` remark about not simply `exit()`.  
- Some code uses `"_"` as a sentinel for a failed guess (spin lost or bankrupt). That can be confusing in logic since `"_"` might be a valid character in `showing`; but current code treats it as a special case.  
- `get_random_puzzle()` assumes ~901 puzzles (random 0..900); if file smaller, may not find a match.  
- `bigrams.txt` must exist and be formatted as "bigram count" or similar (the code splits on space and uppercases first token).  
- `spin_wheel()` blocks for 2 seconds and calls `ascii_wheel.draw_ascii_wheel(...)` — requires that module to be importable.  
- There is no input validation against repeating `previous_guesses` for underscores and some edge cases; comments mention quirks (e.g., buying 'E' causes issues).

**Quick suggestions (optional):**  
- Replace abrupt `exit()` with a cleaner return/raise so the caller can handle end-of-game.  
- Improve handling of `"_"` sentinel vs actual characters — consider returning a boolean for "no-letter" instead.  
- Make `get_random_puzzle()` robust to file length (use list and random.choice or count lines first).  
- Add unit-testable separations (pure functions) for selection logic so AI strategies can be tested independently.

Would you like me to (pick one):  
- open and annotate specific functions inline,  
- convert abrupt `exit()` into a clean return, or  
- add a simple unit test for one of the AI strategies?