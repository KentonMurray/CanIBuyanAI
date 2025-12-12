import re

def load_wordlist(path="data/words.txt"):
    """Load words from words.txt into a set for fast lookup."""
    with open(path, "r", encoding="utf-8") as f:
        words = [line.strip().upper() for line in f if line.strip()]
    return set(words)


def guess_phrase(pattern, wordlist):
    """
    Guess possible phrases from a pattern using a wordlist.

    pattern: str, e.g., "TH_ QU_CK _RO_N _O_"
    wordlist: set of uppercase words

    Returns: list of matching phrases (strings)
    """
    pattern = pattern.upper().strip()
    # Split the pattern into words
    pattern_words = pattern.split()

    # For each pattern word, compile a regex replacing _ with [A-Z]
    regexes = [re.compile("^" + w.replace("_", "[A-Z]") + "$") for w in pattern_words]

    # Find candidate words for each pattern word
    candidate_lists = []
    for regex in regexes:
        candidates = [w for w in wordlist if regex.match(w)]
        candidate_lists.append(candidates)

    # Generate all possible phrase combinations
    # Be careful: if some lists are huge, this can explode combinatorially
    from itertools import product
    phrases = [" ".join(p) for p in product(*candidate_lists)]

    return phrases


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    words = load_wordlist("data/words.txt")
    pattern = "TH_ QU_CK _RO_N _O_"
    matches = guess_phrase(pattern, words)
    print(f"Found {len(matches)} matches:\n")
    for m in matches[:20]:  # show only top 20
        print(m)