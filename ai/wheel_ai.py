import re
import collections
import os

class WheelAI:
    """
    Wheel of Fortune Vowel Purchasing AI.
    Uses pattern matching + vowel probability estimation + expected value logic.
    """

    def __init__(self, dictionary_path="words_alpha.txt", vowel_cost=250):
        self.vowel_cost = vowel_cost
        self.vowels = set("AEIOU")
        self.corpus = self._load_dictionary(dictionary_path)

        # Fallback English vowel frequencies
        self.general_vowel_freq = {
            "A": 0.082, "E": 0.127, "I": 0.070,
            "O": 0.075, "U": 0.028
        }

    # -------------------------------------------------------------------------
    # DATA LOADING
    # -------------------------------------------------------------------------

    def _load_dictionary(self, path):
        """Loads dictionary or uses fallback list."""
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return [
                        w.strip().upper()
                        for w in f
                        if w.strip().isalpha()
                    ]
            except:
                pass

        print("[AI WARNING] Using fallback dictionary.")
        return [
            "APPLE", "BANANA", "PYTHON", "COMPUTER", "ALGORITHM",
            "ORANGE", "GRAPE", "CHERRY", "STRAWBERRY", "MOONLIGHT",
            "SUNSHINE", "TELEPHONE", "JOURNEY", "DATABASE", "KEYBOARD"
        ]

    # -------------------------------------------------------------------------
    # PATTERN MATCHING ENGINE
    # -------------------------------------------------------------------------

    def _generate_regex(self, board_pattern, used_letters):
        """Builds a regex to filter candidate words."""
        clean = board_pattern.replace(" ", "").upper()

        revealed = set(c for c in clean if c.isalpha())
        dead = used_letters - revealed
        excluded = revealed.union(dead)

        # Characters that blanks CANNOT be
        if excluded:
            exclusion = f"[^{''.join(sorted(excluded))}]"
        else:
            exclusion = "."

        regex = "^"
        for c in clean:
            if c == "_":
                regex += exclusion
            elif c.isalpha():
                regex += c
            else:
                regex += re.escape(c)
        regex += "$"

        return regex

    def _get_candidates(self, board_pattern, used_letters):
        """Returns all dictionary words matching the board."""
        regex = re.compile(self._generate_regex(board_pattern, used_letters))
        return [w for w in self.corpus if regex.match(w)]

    # -------------------------------------------------------------------------
    # PROBABILITY CALCULATIONS
    # -------------------------------------------------------------------------

    def _vowel_probabilities(self, candidates, used_letters):
        """Returns probability of each vowel appearing in remaining candidates."""
        if not candidates:
            return {}

        counts = collections.Counter()
        total = len(candidates)

        for w in candidates:
            for v in self.vowels:
                if v not in used_letters and v in w:
                    counts[v] += 1

        return {v: counts[v] / total for v in counts}

    def _fallback_stats(self, board_pattern, used_letters):
        """Statistical expected-value fallback when no pattern-matching possible."""
        clean = board_pattern.replace(" ", "")
        blanks = clean.count("_")
        total = len(clean)

        if total == 0:
            return {}

        density = (total - blanks) / total  # Filled-in fraction
        info_need = 1 - density              # How much more info is needed

        scores = {}

        for v in self.vowels:
            if v in used_letters:
                continue

            freq = self.general_vowel_freq.get(v, 0.05)
            # Basic EV model: likelihood × info value × assumed 1–2 occurrences
            score = freq * info_need * 2.0
            scores[v] = score

        return scores

    # -------------------------------------------------------------------------
    # DECISION ENGINE
    # -------------------------------------------------------------------------

    def should_buy_vowel(self, board_pattern, used_letters, current_money):
        """
        Master decision function.

        Returns:
            {
                "decision": bool,
                "suggested_vowel": str or None,
                "reason": str,
                "strategy": str,
                "confidence": float
            }
        """

        # 0. Financial constraint
        if current_money < self.vowel_cost:
            return {
                "decision": False,
                "suggested_vowel": None,
                "reason": "Insufficient money to buy a vowel.",
                "strategy": "Finance",
                "confidence": 1.0
            }

        # 1. Primary strategy: pattern matching
        candidates = self._get_candidates(board_pattern, used_letters)

        if candidates:
            probs = self._vowel_probabilities(candidates, used_letters)

            if not probs:
                return {
                    "decision": False,
                    "suggested_vowel": None,
                    "reason": "Pattern match: No vowels appear in candidates.",
                    "strategy": "Pattern Matching",
                    "confidence": 0.9
                }

            best_vowel = max(probs, key=probs.get)
            confidence = probs[best_vowel]

            # Decision thresholds
            if confidence >= 0.70:
                return {
                    "decision": True,
                    "suggested_vowel": best_vowel,
                    "reason": f"High probability {confidence:.1%} from pattern matching.",
                    "strategy": "Pattern Matching",
                    "confidence": confidence
                }

            if current_money > 2000 and confidence > 0.40:
                return {
                    "decision": True,
                    "suggested_vowel": best_vowel,
                    "reason": "Aggressive strategy enabled by high money and decent odds.",
                    "strategy": "Pattern Matching (Aggressive)",
                    "confidence": confidence
                }

            return {
                "decision": False,
                "suggested_vowel": best_vowel,
                "reason": f"Low probability ({confidence:.1%}). Better to spin.",
                "strategy": "Pattern Matching",
                "confidence": confidence
            }

        # 2. Fallback strategy (no candidate words)
        fallback = self._fallback_stats(board_pattern, used_letters)

        if not fallback:
            return {
                "decision": False,
                "suggested_vowel": None,
                "reason": "No valid vowels remaining.",
                "strategy": "Fallback",
                "confidence": 1.0
            }

        best_vowel = max(fallback, key=fallback.get)
        score = fallback[best_vowel]

        if score > 0.15:
            return {
                "decision": True,
                "suggested_vowel": best_vowel,
                "reason": "Statistical fallback: vowel likely & puzzle is sparse.",
                "strategy": "Fallback",
                "confidence": score
            }

        return {
            "decision": False,
            "suggested_vowel": best_vowel,
            "reason": "Statistical fallback indicates low value.",
            "strategy": "Fallback",
            "confidence": score
        }
