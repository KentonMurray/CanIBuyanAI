"""
Smart Decision Function for Wheel of Fortune
Decides whether to spin the wheel or buy a vowel based on game state analysis.
"""

import re
from collections import Counter
from pathlib import Path
from typing import Tuple, Dict, List

_DICT_CACHE: List[str] = []


def should_spin_or_buy_vowel(
    showing: str,
    winnings: int,
    previous_guesses: List[str],
    next_letter_candidate: str = None,
    opponents_winnings: List[int] = None,
    strategy: str = 'optimized'
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
    letter_model = build_letter_probability_model(showing, previous_guesses)
    
    # If we can't afford a vowel, we must spin
    if winnings < 250:
        return 'spin', "Insufficient funds to buy vowel ($250 required)"
    
    # Calculate expected values and risks
    spin_analysis = analyze_spin_risk()
    vowel_analysis = analyze_vowel_value(game_state, previous_guesses, letter_model)

    # Estimate how confident we are about the full puzzle solution by
    # matching the showing pattern against the known puzzle corpus or synthesis.
    solution_dist = estimate_solution_distribution(showing, previous_guesses, letter_model=letter_model)
    solution_confidence = solution_dist.get('top_probability', 0.0)
    synthesized = solution_dist.get('synthesized', False)
    candidate_count = solution_dist.get('candidate_count', 0)

    # If puzzle is nearly complete (>80% revealed) try to solve only when
    # we have some confidence or a real candidate from the corpus.
    if game_state['completion_ratio'] > 0.8 and (solution_confidence >= 0.6 or candidate_count > 0):
        return 'solve', f"Puzzle is {game_state['completion_ratio']:.1%} complete - time to solve"

    # Strategy overrides
    if strategy == 'always_spin':
        return 'spin', 'Strategy: always spin'
    if strategy == 'always_solve' and solution_confidence > 0:
        return 'solve', 'Strategy: always solve when any confidence exists'

    # Compute spin expected value (cash per spin given expected consonant hits)
    spin_ev = compute_spin_expected_cash(game_state, spin_analysis, letter_model)

    # If we're confident enough in the solution, attempt to solve
    solve_threshold = 0.75
    # Competitive modelling: reduce threshold if opponents are close to winning
    if opponents_winnings:
        max_opp = max(opponents_winnings)
        if max_opp > winnings + 500:
            # opponent is far ahead -> be more aggressive about solving
            solve_threshold -= 0.15

    if solution_confidence >= solve_threshold:
        reasoning = f"Solve: top candidate has probability {solution_confidence:.1%}"
        return 'solve', reasoning

    # Otherwise compare EV of spinning vs expected losses from negative wedges
    # Estimate expected downside of spinning (bankruptcy/lose-turn cost)
    expected_downside = (
        spin_analysis['bankrupt_probability'] * winnings +
        spin_analysis['lose_turn_probability'] * (winnings * 0.1)
    )

    # Rough expected utility for spinning vs buying vowel
    spin_utility = spin_ev - expected_downside
    info_bonus = vowel_analysis.get('best_info_gain', 0) * 80
    vowel_utility = vowel_analysis.get('expected_letters', 0) * 90 + info_bonus - 250

    # Use existing decision score as a fallback tie-breaker
    decision_score = calculate_decision_score(
        game_state, spin_analysis, vowel_analysis, winnings
    )

    # Choose according to optimized model
    if strategy == 'optimized':
        # If vowels remove a lot of uncertainty, lean toward buying even when EVs tie
        info_heavy = vowel_analysis.get('best_info_gain', 0) > 0.25
        if spin_utility > vowel_utility and decision_score['spin'] >= decision_score['buy_vowel'] and not info_heavy:
            reasoning = f"Spin EV ${spin_ev:.0f} vs vowel utility ${vowel_utility:.0f}; " \
                        f"confidence {solution_confidence:.1%}"
            return 'spin', reasoning
        else:
            info_text = f", info gain {vowel_analysis.get('best_info_gain',0):.2f}" if info_heavy else ""
            reasoning = f"Buy vowel: utility ${vowel_utility:.0f} vs spin EV ${spin_ev:.0f}; " \
                        f"confidence {solution_confidence:.1%}{info_text}"
            return 'buy_vowel', reasoning
    else:
        # Fallback to earlier scoring
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


def analyze_vowel_value(
    game_state: Dict,
    previous_guesses: List[str],
    letter_model: Dict = None
) -> Dict:
    """Analyze the expected value of buying a vowel.

    If a letter probability model is available, use it to estimate the
    best vowel and how many letters it is expected to reveal. Otherwise
    fall back to a frequency-based heuristic.
    """
    if letter_model and (letter_model.get('best_vowel') or letter_model.get('best_info_vowel')):
        best_vowel = letter_model.get('best_vowel') or letter_model.get('best_info_vowel')
        expected_letters = letter_model['expected_reveals'].get(best_vowel, 0.0)
        probability_of_hit = letter_model['prob_any'].get(best_vowel, 0.0)
        info_gain = letter_model.get('info_gain', {}).get(best_vowel, 0.0)
        return {
            'expected_letters': expected_letters,
            'probability_of_hit': probability_of_hit,
            'available_vowels': letter_model.get('available_vowels', 0),
            'best_vowel_frequency': probability_of_hit,
            'best_info_gain': info_gain,
            'best_vowel': best_vowel
        }
    
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


def _load_matching_puzzles(showing: str) -> tuple:
    """Return the normalized showing pattern and matching puzzles from the corpus."""
    norm_showing = re.sub(r'[^A-Z_ ]', '', showing.upper())
    if not norm_showing.strip():
        return norm_showing, []

    pattern = '^' + re.escape(norm_showing).replace('_', '[A-Z]') + '$'
    prog = re.compile(pattern)

    # Resolve the puzzle list relative to the repo root to work in both CLI and IDE
    base = Path(__file__).resolve().parents[2] / "data" / "puzzles"
    puzzle_files = ["valid.csv", "train.csv", "test.csv", "years_1_25.csv"]
    # Deduplicate by normalized puzzle text so the same puzzle appearing in
    # multiple corpus files doesn't artificially dilute the confidence score.
    matches = []
    seen_norm = set()
    for fname in puzzle_files:
        p = base / fname
        if not p.exists():
            continue
        try:
            with p.open('r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    puzzle = line.split(',')[0].strip().upper()
                    puzzle_norm = re.sub(r'[^A-Z ]', '', puzzle)
                    puzzle_norm = re.sub(r'\s+', ' ', puzzle_norm).strip()
                    if prog.match(puzzle_norm) and puzzle_norm not in seen_norm:
                        matches.append((puzzle, puzzle_norm))
                        seen_norm.add(puzzle_norm)
        except FileNotFoundError:
            continue

    return norm_showing, matches


def estimate_solution_distribution(
    showing: str,
    previous_guesses: List[str],
    top_k: int = 10,
    letter_model: Dict = None,
    allow_corpus_lookup: bool = False
) -> Dict:
    """Estimate a probability distribution over possible solutions from the corpus.

    This is a lightweight pattern matcher: it normalizes the showing and each
    puzzle in `data/puzzles/valid.csv`, matches patterns, and scores candidates
    by how well they fit the revealed letters and how many blanks they fill.
    Returns a small distribution with top candidates and a `top_probability`.
    """
    norm_showing, matches = _load_matching_puzzles(showing)
    # To avoid "cheating" by memorizing the dataset, skip direct lookups unless explicitly allowed.
    if not allow_corpus_lookup:
        matches = []

    if not matches:
        # Try to build a plausible full candidate from the system dictionary.
        dict_candidate, dict_conf = _synthesize_from_dictionary(showing, previous_guesses, letter_model)
        if dict_candidate:
            return {
                'candidates': [(dict_candidate, dict_conf)],
                'top_probability': dict_conf,
                'candidate_count': 0,
                'synthesized': True
            }
        # Fallback: synthesize a best-guess candidate using the letter model or
        # default English frequencies so we still have a solve target.
        fallback_candidate = synthesize_candidate(showing, previous_guesses, letter_model)
        if not fallback_candidate.strip('_ '):
            return {'candidates': [], 'top_probability': 0.0}
        # Give a modest pseudo-confidence; higher if almost solved
        blank_ratio = norm_showing.count('_') / max(1, len(norm_showing.replace(' ','')))
        pseudo_conf = max(0.35, 0.85 - blank_ratio)
        return {
            'candidates': [(fallback_candidate, pseudo_conf)],
            'top_probability': pseudo_conf,
            'candidate_count': 0,
            'synthesized': True
        }

    candidates = []
    for puzzle, puzzle_norm in matches:
        revealed = sum(1 for a, b in zip(norm_showing, puzzle_norm) if a != '_' and a == b)
        blanks = norm_showing.count('_')
        score = 1 + revealed + (blanks - puzzle_norm.count(' ')) * 0.1
        candidates.append((puzzle, score))

    if not candidates:
        return {'candidates': [], 'top_probability': 0.0}

    # Normalize scores to probabilities
    total = sum(s for _, s in candidates)
    dist = sorted(((p, s / total) for p, s in candidates), key=lambda x: -x[1])
    top = dist[:top_k]
    top_probability = top[0][1] if top else 0.0
    return {
        'candidates': top,
        'top_probability': top_probability,
        'candidate_count': len(matches),
        'synthesized': False
    }


def _synthesize_from_dictionary(showing: str, previous_guesses: List[str], letter_model: Dict = None) -> Tuple[str, float]:
    """Build a candidate solution using dictionary matches for each word.

    Returns (candidate, confidence) or ('', 0.0) if not enough evidence.
    Confidence is modest and scales with how much of the board is revealed.
    """
    if not showing:
        return "", 0.0

    words = showing.split(' ')
    if not words:
        return "", 0.0

    letter_model = letter_model or build_letter_probability_model(showing, previous_guesses)
    filled_words = []
    any_blank = False

    for word in words:
        if '_' not in word:
            filled_words.append(word)
            continue
        any_blank = True
        dict_word = _best_word_match(word, previous_guesses, letter_model)
        if not dict_word:
            # If any blank word cannot be matched, abort dictionary synthesis
            return "", 0.0
        filled_words.append(dict_word)

    if not any_blank:
        # Already solved
        return showing, 0.9

    candidate = ' '.join(filled_words)
    # Confidence: start modestly and increase as blanks shrink
    norm_show = re.sub(r'[^A-Z_]', '', showing.upper())
    blank_ratio = norm_show.count('_') / max(1, len(norm_show))
    revealed_ratio = 1 - blank_ratio
    confidence = min(0.85, 0.4 + 0.5 * revealed_ratio)
    return candidate, confidence


def build_letter_probability_model(
    showing: str,
    previous_guesses: List[str],
    max_candidates: int = 400
) -> Dict:
    """Create a positional letter probability model from matching corpus entries.

    It looks at all candidate solutions that fit the current pattern and
    computes the probability of each letter appearing in any blank plus the
    expected number of letters that would be revealed by guessing it.
    """
    norm_showing, matches = _load_matching_puzzles(showing)
    matches = matches[:max_candidates]
    if not matches:
        # Use a simple English frequency fallback so we still produce useful guesses
        base_freq = {
            **{c: f for c, f in zip("ETAOINSHRDLU", [0.127,0.091,0.081,0.075,0.07,0.069,0.067,0.063,0.061,0.060,0.043,0.040])},
            **{c: f for c, f in zip("CMFWYGPBVKQJXZ", [0.028,0.024,0.024,0.024,0.02,0.02,0.02,0.019,0.013,0.01,0.008,0.001,0.001,0.001])}
        }
        available = {k:v for k,v in base_freq.items() if k not in previous_guesses}
        expected_reveals = {k: v for k, v in available.items()}
        vowels = {l: v for l, v in expected_reveals.items() if l in 'AEIOU'}
        consonants = {l: v for l, v in expected_reveals.items() if l not in 'AEIOU'}
        best_vowel = max(vowels, key=vowels.get) if vowels else None
        best_consonant = max(consonants, key=consonants.get) if consonants else None
        info_gain = {letter: 2 * p * (1 - p) for letter, p in available.items()}
        info_vowels = {l: info_gain.get(l, 0) for l in info_gain if l in 'AEIOU'}
        info_consonants = {l: info_gain.get(l, 0) for l in info_gain if l not in 'AEIOU'}
        return {
            'prob_any': available,
            'expected_reveals': expected_reveals,
            'best_vowel': best_vowel,
            'best_consonant': best_consonant,
            'available_vowels': len(vowels),
            'info_gain': info_gain,
            'best_info_vowel': max(info_vowels, key=info_vowels.get) if info_vowels else best_vowel,
            'best_info_consonant': max(info_consonants, key=info_consonants.get) if info_consonants else best_consonant,
            'candidate_count': 0,
        }

    blank_positions = [i for i, c in enumerate(norm_showing) if c == '_']
    if not blank_positions:
        return {
            'prob_any': {},
            'expected_reveals': {},
            'best_vowel': None,
            'best_consonant': None,
            'available_vowels': 0,
        }

    candidate_hits = Counter()
    reveal_counts = Counter()
    total_candidates = len(matches)

    for _, puzzle_norm in matches:
        seen_in_candidate = set()
        for pos in blank_positions:
            if pos >= len(puzzle_norm):
                continue
            letter = puzzle_norm[pos]
            if letter == ' ' or letter in previous_guesses:
                continue
            reveal_counts[letter] += 1
            seen_in_candidate.add(letter)
        for letter in seen_in_candidate:
            candidate_hits[letter] += 1

    prob_any = {letter: candidate_hits[letter] / total_candidates for letter in candidate_hits}
    expected_reveals = {letter: reveal_counts[letter] / total_candidates for letter in reveal_counts}
    info_gain = {letter: 2 * p * (1 - p) for letter, p in prob_any.items()}

    # Split vowels and consonants for quick lookup
    vowels = {l: expected_reveals[l] for l in expected_reveals if l in 'AEIOU'}
    consonants = {l: expected_reveals[l] for l in expected_reveals if l not in 'AEIOU'}
    info_vowels = {l: info_gain.get(l, 0) for l in info_gain if l in 'AEIOU'}
    info_consonants = {l: info_gain.get(l, 0) for l in info_gain if l not in 'AEIOU'}

    best_vowel = max(vowels, key=vowels.get) if vowels else None
    best_consonant = max(consonants, key=consonants.get) if consonants else None
    best_info_vowel = max(info_vowels, key=info_vowels.get) if info_vowels else None
    best_info_consonant = max(info_consonants, key=info_consonants.get) if info_consonants else None

    return {
        'prob_any': prob_any,
        'expected_reveals': expected_reveals,
        'best_vowel': best_vowel,
        'best_consonant': best_consonant,
        'available_vowels': len(vowels),
        'info_gain': info_gain,
        'best_info_vowel': best_info_vowel,
        'best_info_consonant': best_info_consonant,
        'candidate_count': total_candidates,
    }


def _load_dictionary() -> List[str]:
    """Load system dictionary words once, uppercase."""
    global _DICT_CACHE
    if _DICT_CACHE:
        return _DICT_CACHE
    dict_path = Path("/usr/share/dict/words")
    if not dict_path.exists():
        return []
    try:
        with dict_path.open('r') as f:
            _DICT_CACHE = [w.strip().upper() for w in f if w.strip() and w[0].isalpha()]
    except Exception:
        _DICT_CACHE = []
    return _DICT_CACHE


def _best_word_match(pattern: str, previous_guesses: List[str], letter_model: Dict) -> str:
    """Pick the best dictionary word matching the underscore pattern."""
    words = _load_dictionary()
    if not words:
        return ""
    regex = '^' + re.escape(pattern).replace('_', '[A-Z]') + '$'
    prog = re.compile(regex)
    candidates = [w for w in words if len(w) == len(pattern) and prog.match(w)]
    if not candidates:
        return ""

    # Score by sum of letter probabilities (fallback to frequency if missing)
    prob_any = letter_model.get('prob_any', {})
    base_freq = {
        **{c: f for c, f in zip("ETAOINSHRDLU", [0.127,0.091,0.081,0.075,0.07,0.069,0.067,0.063,0.061,0.060,0.043,0.040])},
        **{c: f for c, f in zip("CMFWYGPBVKQJXZ", [0.028,0.024,0.024,0.024,0.02,0.02,0.02,0.019,0.013,0.01,0.008,0.001,0.001,0.001])}
    }
    def score(word: str) -> float:
        base = sum(prob_any.get(c, base_freq.get(c, 0.001)) for c in word)
        # Heuristic: after QU, prefer I (e.g., QUICK) and penalize other vowels
        bonus = 0.0
        for i in range(len(word) - 2):
            if word[i] == 'Q' and word[i+1] == 'U':
                next_c = word[i+2]
                if next_c == 'I':
                    bonus += 0.5
                elif next_c in 'AOEY':
                    bonus -= 0.2
        return base + bonus

    best = max(candidates, key=score)
    return best


def synthesize_candidate(showing: str, previous_guesses: List[str], letter_model: Dict = None) -> str:
    """Fill blanks with most probable letters to form a plausible candidate."""
    if not showing:
        return ""
    if not letter_model:
        letter_model = build_letter_probability_model(showing, previous_guesses)

    ranking = sorted(
        letter_model.get('expected_reveals', {}).items(),
        key=lambda kv: (-kv[1], -letter_model.get('prob_any', {}).get(kv[0], 0))
    )
    rank_letters = [l for l, _ in ranking]
    fallback_cycle = rank_letters or list("ETAOINSHRDLU")

    # Try to fill word-by-word using a dictionary; fall back to simple fill
    words = showing.split(' ')
    filled_words = []
    for word in words:
        if '_' not in word:
            filled_words.append(word)
            continue
        dict_word = _best_word_match(word, previous_guesses, letter_model)
        if dict_word:
            filled_words.append(dict_word)
        else:
            filled_words.append(_fill_blanks_simple(word, fallback_cycle))

    return ' '.join(filled_words)


def _fill_blanks_simple(word: str, fallback_cycle: List[str]) -> str:
    """Fill blanks sequentially, enforcing simple patterns like QU."""
    filled = []
    cycle_idx = 0
    for i, ch in enumerate(word):
        if ch == '_':
            if i > 0 and filled[i-1] == 'Q':
                filled.append('U')
                continue
            if i > 1 and filled[i-1] == 'U' and filled[i-2] == 'Q':
                # After QU_, prefer I before other vowels
                filled.append('I')
                continue
            if cycle_idx >= len(fallback_cycle):
                cycle_idx = 0
            filled.append(fallback_cycle[cycle_idx])
            cycle_idx += 1
        else:
            filled.append(ch)
    return ''.join(filled)


def compute_spin_expected_cash(
    game_state: Dict,
    spin_analysis: Dict,
    letter_model: Dict = None
) -> float:
    """Estimate cash EV for a spin given game state and wheel analysis.

    This multiplies the average positive wedge by the probability of hitting a
    positive wedge, the expected number of consonants revealed (approx), and
    probability that a guessed consonant appears in the blanks.
    """
    avg_value = spin_analysis.get('average_positive_value', 0)
    success_prob = spin_analysis.get('success_probability', 0)
    if letter_model and (letter_model.get('best_consonant') or letter_model.get('best_info_consonant')):
        best_consonant = letter_model.get('best_consonant') or letter_model.get('best_info_consonant')
        expected_consonants = max(0.5, letter_model['expected_reveals'].get(best_consonant, 0.5))
        consonant_prob = letter_model['prob_any'].get(best_consonant, 0.2)
        consonant_prob = max(0.05, min(1.0, consonant_prob))
    else:
        # Expected consonants remaining (bounded)
        expected_consonants = max(0.5, min(3, game_state.get('estimated_remaining_consonants', 1)))
        # Probability a random blank is a consonant
        blank_count = game_state.get('blank_count', 1)
        consonant_prob = (game_state.get('estimated_remaining_consonants', 0) / blank_count) if blank_count > 0 else 0.5
        consonant_prob = min(1.0, max(0.05, consonant_prob))

    # EV per spin (dollars expected if we choose optimal consonant)
    ev = avg_value * success_prob * expected_consonants * consonant_prob
    return ev


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
    buy_vowel_score += vowel_analysis.get('best_info_gain', 0) * 300  # reward information gain
    
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
    info_gain = vowel_analysis.get('best_info_gain', 0)
    if buy_vowel_score > spin_score:
        reasoning = f"Buy vowel: High vowel density ({game_state['vowel_density']:.2f}), " \
                   f"expected {vowel_analysis['expected_letters']:.1f} letters revealed"
        if info_gain > 0.15:
            reasoning += f", info gain {info_gain:.2f}"
    else:
        reasoning = f"Spin wheel: Expected value ${spin_expected:.0f}, " \
                   f"{spin_analysis['success_probability']:.1%} success rate"
    
    return {
        'spin': spin_score,
        'buy_vowel': buy_vowel_score,
        'reasoning': reasoning
    }


def get_best_vowel_guess(showing: str, previous_guesses: List[str]) -> str:
    """Determine the best vowel to guess based on the candidate set."""

    letter_model = build_letter_probability_model(showing, previous_guesses)
    if letter_model.get('best_vowel') or letter_model.get('best_info_vowel'):
        return letter_model.get('best_vowel') or letter_model.get('best_info_vowel')
    
    vowel_frequencies = {'E': 0.127, 'A': 0.082, 'O': 0.075, 'I': 0.070, 'U': 0.028}
    
    # Filter available vowels
    available_vowels = {v: f for v, f in vowel_frequencies.items() 
                       if v not in previous_guesses}
    
    if not available_vowels:
        return 'E'  # Fallback
    
    # Return most frequent available vowel
    return max(available_vowels.keys(), key=lambda x: available_vowels[x])


def get_best_consonant_guess(showing: str, previous_guesses: List[str]) -> str:
    """Determine the best consonant to guess using the candidate set."""

    letter_model = build_letter_probability_model(showing, previous_guesses)
    if letter_model.get('best_consonant') or letter_model.get('best_info_consonant'):
        return letter_model.get('best_consonant') or letter_model.get('best_info_consonant')
    
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
