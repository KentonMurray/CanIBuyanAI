#needs phrases
"""
Wheel of Fortune Solver Module
=================================

This single-file module implements a Wheel-of-Fortune-style phrase solver and
includes utilities to load phrase/word datasets, match patterns with wildcards, and
rank candidate phrases by likelihood.

Features
--------
- Loads phrase lists from plain text files (one phrase per line) in ./data/
- Optionally uses `wordfreq` (if installed) to score phrases by frequency (recommended)
- Pure-Python fallback scoring using word counts if `wordfreq` is absent
- Fast pattern matching that preserves word boundaries and ignores punctuation
- CLI: `python wof_solver2.py "TH_ QU_CK _RO_N _O_" --top 20`
- Optional --download flag will attempt to fetch candidate sources (simple downloader)

Expected data layout (place your phrase and word files here):

  data/
    phrases.txt        # one phrase per line (common phrases)
    words.txt          # optional: one word per line (useful for ranking/backfilling)

If no data files are found, the module can still run but will return no matches.

Notes
-----
- The pattern uses underscore `_` for missing letters. Spaces separate words.
- Input pattern can be lowercase or uppercase; punctuation in patterns is ignored.
- Scoring: higher score = more likely. If wordfreq is available, it uses zipf scores;
  otherwise it uses corpus-derived frequencies.

License: MIT-style (you may reuse and modify for personal use).

"""

from __future__ import annotations
import argparse
import os
import re
import sys
import math
from collections import Counter, defaultdict
from typing import List, Tuple, Optional

# Try to import wordfreq for better scoring. It's optional.
try:
    from wordfreq import zipf_frequency
    HAS_WORDSCORE = True
except Exception:
    HAS_WORDSCORE = False


# ----------------------------- Utilities ---------------------------------

def normalize_phrase(s: str) -> str:
    """Normalize a phrase: uppercase letters and collapse whitespace; remove
    punctuation except spaces and apostrophes (apostrophes are kept).
    """
    # Keep letters, spaces, and apostrophes; convert to upper
    s = s.upper()
    s = re.sub(r"[^A-Z0-9 '\"]+", " ", s)  # turn punctuation into spaces
    s = re.sub(r"\s+", " ", s).strip()
    return s


def pattern_to_regex(pattern: str) -> str:
    """Convert a WOFD-style pattern (underscores as unknown letters) into a regex
    anchored to match the full phrase. Keeps spaces as word separators.

    Example: "TH_ QU_CK _RO_N _O_" -> r'^TH[A-Z] QU[A-Z]CK [A-Z]RO[A-Z]N [A-Z]O[A-Z]$'
    """
    # Normalize spacing and uppercase
    pattern = normalize_phrase(pattern)

    # Replace underscores: a single underscore stands for a single letter
    def repl(m):
        return "[A-Z]"

    # We must preserve letters and spaces; all digits are treated as literals
    # Escape any regex-significant characters (there shouldn't be any after normalize)
    regex_parts = []
    for ch in pattern:
        if ch == "_":
            regex_parts.append("[A-Z]")
        elif ch == " ":
            regex_parts.append("\\s+")
        else:
            # Letters or digits
            safe = re.escape(ch)
            regex_parts.append(safe)
    regex = "^" + "".join(regex_parts) + "$"
    return regex


# --------------------------- Dataset Loader -------------------------------

class Dataset:
    """Loads phrases and words from a data directory.

    Expects:
      data/phrases.txt  (one phrase per line)
      data/words.txt    (one word per line)  -- optional

    Provides accessors and a simple frequency table for fallback scoring.
    """
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.phrases: List[str] = []
        self.words: List[str] = []
        self.word_counts: Counter = Counter()
        self._loaded = False

    def load(self) -> None:
        self._load_phrases()
        self._load_words()
        self._derive_word_counts()
        self._loaded = True

    def _load_phrases(self) -> None:
        pfile = os.path.join(self.data_dir, "phrases.txt")
        if not os.path.exists(pfile):
            # Try alternate names often used in bundles
            candidates = ["wof_phrases.txt", "phrases_common.txt", "phrases_all.txt"]
            found = False
            for c in candidates:
                path = os.path.join(self.data_dir, c)
                if os.path.exists(path):
                    pfile = path
                    found = True
                    break
            if not found:
                # No phrase file; leave phrases empty
                print(f"[Dataset] No phrases file found at {pfile}. Continue with empty list.", file=sys.stderr)
                self.phrases = []
                return

        with open(pfile, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
        cleaned = []
        for line in lines:
            if not line:
                continue
            norm = normalize_phrase(line)
            # Exclude anything that's too long or too short for WOF (heuristic)
            if len(norm) < 1:
                continue
            cleaned.append(norm)
        # Deduplicate preserving order
        seen = set()
        dedup = []
        for ph in cleaned:
            if ph not in seen:
                dedup.append(ph)
                seen.add(ph)
        self.phrases = dedup
        print(f"[Dataset] Loaded {len(self.phrases)} phrases.", file=sys.stderr)

    def _load_words(self) -> None:
        wfile = os.path.join(self.data_dir, "words.txt")
        if not os.path.exists(wfile):
            self.words = []
            return
        with open(wfile, "r", encoding="utf-8") as f:
            ws = [w.strip() for w in f if w.strip()]
        self.words = [w.upper() for w in ws]
        print(f"[Dataset] Loaded {len(self.words)} words.", file=sys.stderr)

    def _derive_word_counts(self) -> None:
        # Build counts from phrases first, then words
        counts = Counter()
        for ph in self.phrases:
            for w in ph.split():
                counts[w] += 1
        for w in self.words:
            counts[w] += 0  # ensure existence
        self.word_counts = counts


# ----------------------------- Scoring -----------------------------------

class Scorer:
    """Scoring helper. Uses wordfreq.zipf_frequency when available, else fallbacks
    to phrase-derived counts.
    """
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def word_score(self, word: str) -> float:
        w = word.lower()
        if HAS_WORDSCORE:
            try:
                # zipf_frequency returns numbers ~0..7
                return zipf_frequency(w, "en")
            except Exception:
                pass
        # Fallback: use log(count + 1)
        cnt = self.dataset.word_counts.get(word.upper(), 0)
        return math.log1p(cnt)

    def phrase_score(self, phrase: str) -> float:
        # Sum of word scores; longer phrases get more base score but that's OK.
        total = 0.0
        for w in phrase.split():
            total += self.word_score(w)
        # Small length normalization: prefer exact-length matches with more common words
        return total


# ----------------------------- Solver ------------------------------------

class WoFSolver:
    def __init__(self, dataset: Dataset):
        if not dataset._loaded:
            dataset.load()
        self.dataset = dataset
        self.scorer = Scorer(dataset)

    def find_matches(self, pattern: str, top_n: int = 20, min_score: Optional[float] = None) -> List[Tuple[str, float]]:
        """Return top_n matches as (phrase, score) sorted by score desc.

        pattern: underscores (_) mean unknown letters. Spaces separate words. Pattern
                 is matched against normalized phrase text.
        """
        regex = pattern_to_regex(pattern)
        cre = re.compile(regex)

        candidates = []
        for ph in self.dataset.phrases:
            if cre.match(ph):
                score = self.scorer.phrase_score(ph)
                if min_score is not None and score < min_score:
                    continue
                candidates.append((ph, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_n]

    def find_matches_allow_letters(self, pattern: str, allowed_letters: Optional[List[str]] = None, top_n: int = 20) -> List[Tuple[str, float]]:
        """Like find_matches but additionally requires that no letters appear that are
        known to have been guessed and excluded. `allowed_letters` is a list of letters that
        *may* appear; if provided, candidates containing letters outside this set are filtered out.
        (This is useful when you want to ensure you only consider phrases composed of allowed letters.)
        """
        matches = self.find_matches(pattern, top_n=None)
        if allowed_letters is None:
            return matches[:top_n]
        allowed_set = set(l.upper() for l in allowed_letters)
        filtered = []
        for ph, sc in matches:
            ok = True
            for ch in ph:
                if ch.isalpha() and ch not in allowed_set:
                    ok = False
                    break
            if ok:
                filtered.append((ph, sc))
            if len(filtered) >= top_n:
                break
        return filtered


# --------------------------- Downloader (optional) ------------------------

def simple_downloader(target_dir: str = "data") -> None:
    """Attempts to download a few helpful sources into target_dir. This is a
    convenience helper — it uses simple HTTP GETs and expects internet access.

    NOTE: This function is best-effort. If you're behind a firewall or offline,
    it will report failures but won't crash.
    """
    import urllib.request
    os.makedirs(target_dir, exist_ok=True)

    sources = [
        # small example sources (placeholders). For a real assembly you'd replace
        # these with links to SCOWL, OpenSubtitles, Gutenberg ngram extracts, etc.
        ("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt", "words.txt"),
        # a small common phrases repo (example)
        ("https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt", "phrases.txt"),
    ]

    for url, dest in sources:
        outpath = os.path.join(target_dir, dest)
        try:
            print(f"[Downloader] Fetching {url} -> {outpath}")
            urllib.request.urlretrieve(url, outpath)
            print(f"[Downloader] Saved {outpath}")
        except Exception as e:
            print(f"[Downloader] Failed to download {url}: {e}")


# ------------------------------- CLI ------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(prog="wof_solver.py", description="Wheel-of-Fortune phrase solver")
    parser.add_argument("pattern", help="Pattern with underscores for unknown letters, e.g. 'TH_ QU_CK _RO_N _O_'")
    parser.add_argument("--data", default="data", help="Directory with phrases.txt and words.txt")
    parser.add_argument("--top", type=int, default=20, help="Number of top matches to show")
    parser.add_argument("--download", action="store_true", help="Try to download example datasets into --data")
    parser.add_argument("--min-score", type=float, default=None, help="Filter out candidates below this score")
    args = parser.parse_args(argv)

    if args.download:
        print("[Main] Attempting to download example datasets into:", args.data)
        simple_downloader(args.data)

    ds = Dataset(args.data)
    ds.load()
    solver = WoFSolver(ds)
    matches = solver.find_matches(args.pattern, top_n=args.top, min_score=args.min_score)

    if not matches:
        print("No matches found. Consider running with --download to fetch example data or provide your own data/phrases.txt")
        return 0

    print(f"Top {len(matches)} matches for pattern: {args.pattern}\n")
    for ph, sc in matches:
        print(f"{ph}    (score={sc:.3f})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
