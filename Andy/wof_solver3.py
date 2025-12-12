import re
import string
from collections import Counter
import os

# -------------------------------------------------------------
# LOADING DATA
# -------------------------------------------------------------

#current wof solver as of 12/3/25
#uses 
#    data/words.txt
#    data/phrases.txt
"""
main function

def wof_solver(pattern, attempted_letters=None,
               words_path="data/words.txt",
               phrases_path="data/phrases.txt"):
    Returns dict:
        {
            "solutions": [string, string, string],
            "ranked": [string#1, string#2, string#3],
            "next_letter": [(letter1, count), (letter2, count)]
        }
"""
#see also wof_solver3_test.py

def load_list(path):
    """Return list of uppercase lines from file if it exists."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().upper() for line in f if line.strip()]

# -------------------------------------------------------------
# PATTERN UTILITIES
# -------------------------------------------------------------

def extract_attempted_letters(pattern, attempted):
    """Infer attempted letters from pattern if list is not provided."""
    given_attempted = {}
    if attempted:
        given_attempted = set(x.upper() for x in attempted)
    pattern_attempted = {c for c in pattern.upper() if c in string.ascii_uppercase}
    return pattern_attempted.union(given_attempted)

def pattern_to_regex(pattern, forbidden_letters=None):
    """
    Convert WOF pattern like TH_ QU_CK _RO_N _O_ into a regex.
    Underscores become [A-Z] except letters in forbidden_letters.
    """
    if forbidden_letters is None:
        forbidden_letters = set()
    forbidden_letters = "".join(forbidden_letters)
    rx = []
    for ch in pattern:
        if ch == "_":
            if forbidden_letters:
                # any uppercase letter except forbidden ones
                rx.append(f"[A-Z^{forbidden_letters}]")  # standard Python regex
            else:
                rx.append("[A-Z]")
        elif ch in string.ascii_uppercase:
            rx.append(ch)
        else:
            rx.append(ch)
    return "^" + "".join(rx) + "$"

# -------------------------------------------------------------
# DICTIONARY MATCHING
# -------------------------------------------------------------

def phrase_matches(pattern, phrases, forbidden_letters):
    """Match phrases, excluding forbidden letters in missing positions."""
    # compile basic regex: underscores → [A-Z]
    rx = re.compile(pattern_to_regex(pattern))
    results = []
    for p in phrases:
        if not rx.match(p):
            continue
        # now check forbidden letters only in positions that were underscores
        ok = True
        for pat_char, ph_char in zip(pattern, p):
            if pat_char == "_" and ph_char in forbidden_letters:
                ok = False
                break
        if ok:
            results.append(p)
    return results

# -------------------------------------------------------------
# MULTI-WORD SOLVER (words.txt)
# -------------------------------------------------------------

from itertools import product

def match_words(words, pattern_word, forbidden_letters):
    """Same logic for individual words."""
    rx = re.compile(pattern_to_regex(pattern_word))
    results = []
    for w in words:
        if len(w) != len(pattern_word):
            continue
        if not rx.match(w):
            continue
        # check forbidden letters in underscores
        ok = True
        for pc, wc in zip(pattern_word, w):
            if pc == "_" and wc in forbidden_letters:
                ok = False
                break
        if ok:
            results.append(w)
    return results

def solve_pattern(pattern, words, forbidden_letters):
    """
    Solve a multi-word pattern using words.txt.
    Returns all combined results (list of strings).
    """
    parts = pattern.split()
    candidate_lists = []

    for part in parts:
        matches = match_words(words, part, forbidden_letters)
        if not matches:
            return []  # no possible fill
        candidate_lists.append(matches)

    # Cartesian product to join words
    solutions = [" ".join(words) for words in product(*candidate_lists)]
    return solutions

# -------------------------------------------------------------
# RANKING & NEXT-GUESS
# -------------------------------------------------------------

def rank_solutions(solutions, phrase_set=None):
    """
    Rank solutions by:
      - if phrase is in phrases.txt → +100 bonus
      - sum of ETAOINSHRDLU letter frequency
    """
    freq = Counter("ETAOINSHRDLU")
    ranked = []
    for s in solutions:
        score = sum(freq.get(ch, 0) for ch in s)
        if phrase_set and s in phrase_set:
            score += 100  # boost phrases from phrases.txt
        ranked.append((s, score))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in ranked]

def recommend_next_letter(solutions, attempted, weights=None, phrase_set = {}):
    """
    Weighted letter frequency across candidate solutions.
    solutions: list of strings
    weights: optional list of floats same length as solutions
    """
    attempted = set(attempted)
    counts = Counter()

    if weights is None:
        weights = [1.0] * len(solutions)

    for s, w in zip(solutions, weights):
        for ch in s:
            if ch in string.ascii_uppercase and ch not in attempted:
                counts[ch] += int(w)
                if s in phrase_set:
                    counts[ch] += int(w) * 10

    #add -1 to each letter if they are not in counts and are possible
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if ch not in attempted and ch not in counts:
            counts[ch] += -1

    return counts.most_common()

# -------------------------------------------------------------
# MAIN SOLVER FUNCTION
# -------------------------------------------------------------

def wof_solver(pattern, attempted_letters=None,
               words_path="/home/li126/CanIBuyanAI/Andy/data/words.txt",
               phrases_path="/home/li126/CanIBuyanAI/Andy/data/phrases.txt"):
    """
    Main solver.
    Returns dict:
        {
            "solutions": [...],
            "ranked": [...],
            "next_letter": "E"
        }
    """
    pattern = pattern.upper()
    attempted = extract_attempted_letters(pattern, attempted_letters)

    words = load_list(words_path)
    phrases = load_list(phrases_path)
    phrase_set = set(phrases)

    # forbidden letters = letters already in pattern or attempted
    forbidden = set(c for c in pattern if c in string.ascii_uppercase).union(attempted)

    # 1) phrase matches first (give bonus in ranking)
    all_solutions = set(phrase_matches(pattern, phrases, forbidden))

    # 2) word-based solutions
    word_based = solve_pattern(pattern, words, forbidden)
    all_solutions.update(word_based)

    all_solutions = sorted(all_solutions)

    if not all_solutions:
        return {"solutions": [], "ranked": [], "next_letter": recommend_next_letter([], attempted, None, phrase_set)}

    # rank, giving bonus to phrases in phrases.txt
    ranked = rank_solutions(all_solutions, phrase_set)

    next_letter = recommend_next_letter(ranked, attempted, None, phrase_set)

    return {"solutions": list(all_solutions), "ranked": ranked, "next_letter": next_letter}