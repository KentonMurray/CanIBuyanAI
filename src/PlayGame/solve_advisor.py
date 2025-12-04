"""
Solve Advisor for Wheel of Fortune
Analyzes puzzle state and user's guess to determine probability of being correct.
Uses Google Gemini API for intelligent category-aware analysis.
"""

import re
from typing import Tuple, Dict, List, Optional
from config import get_api_key, set_api_key, GEMINI_MODEL, CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, CONFIDENCE_LOW

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Run: pip install google-generativeai")


class SolveAdvisor:
    """Analyzes puzzle solutions and provides probability estimates."""
    
    def __init__(self, api_key: str = None):
        """Initialize the advisor with optional API key."""
        self.api_key = api_key or get_api_key()
        self.model = None
        
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(GEMINI_MODEL)
            except Exception as e:
                print(f"Warning: Could not initialize Gemini: {e}")
    
    def validate_pattern_match(self, showing: str, guess: str) -> Tuple[bool, float, str]:
        """
        Check if the guess matches the revealed pattern.
        
        Returns:
            Tuple of (is_valid, match_score, explanation)
        """
        # Normalize both strings
        showing_clean = showing.upper().strip()
        guess_clean = guess.upper().strip()
        
        # Check length match
        if len(showing_clean) != len(guess_clean):
            return False, 0.0, f"Length mismatch: pattern has {len(showing_clean)} chars, guess has {len(guess_clean)}"
        
        # Check each position
        mismatches = []
        matches = 0
        total_letters = 0
        
        for i, (pattern_char, guess_char) in enumerate(zip(showing_clean, guess_clean)):
            if pattern_char == '_':
                # Blank position - any letter is potentially valid
                total_letters += 1
                if guess_char.isalpha():
                    matches += 1
                else:
                    mismatches.append(f"Position {i+1}: expected letter, got '{guess_char}'")
            elif pattern_char == ' ':
                # Space must match space
                if guess_char != ' ':
                    mismatches.append(f"Position {i+1}: expected space, got '{guess_char}'")
            elif pattern_char.isalpha():
                # Revealed letter must match exactly
                total_letters += 1
                if pattern_char == guess_char:
                    matches += 1
                else:
                    return False, 0.0, f"Letter mismatch at position {i+1}: pattern shows '{pattern_char}', guess has '{guess_char}'"
            else:
                # Other characters (punctuation) must match
                if pattern_char != guess_char:
                    mismatches.append(f"Position {i+1}: expected '{pattern_char}', got '{guess_char}'")
        
        if mismatches:
            return False, 0.0, "; ".join(mismatches)
        
        match_score = 100.0
        return True, match_score, "Pattern match: Perfect fit!"
    
    def check_letter_consistency(self, showing: str, guess: str, previous_guesses: List[str]) -> Tuple[bool, str]:
        """
        Check if the guess is consistent with previously guessed letters.
        If a letter was guessed and isn't in the puzzle, it shouldn't be in the guess.
        """
        showing_clean = showing.upper()
        guess_clean = guess.upper()
        
        # Find letters that were guessed but aren't showing (meaning they're not in the puzzle)
        letters_not_in_puzzle = []
        for letter in previous_guesses:
            if letter.upper() not in showing_clean.replace('_', ''):
                letters_not_in_puzzle.append(letter.upper())
        
        # Check if guess contains any of these letters
        violations = []
        for letter in letters_not_in_puzzle:
            if letter in guess_clean:
                violations.append(letter)
        
        if violations:
            return False, f"Guess contains letters already confirmed NOT in puzzle: {', '.join(violations)}"
        
        return True, "Letter consistency: OK"
    
    def analyze_with_gemini(self, showing: str, guess: str, category: str, previous_guesses: List[str]) -> Tuple[float, str]:
        """
        Use Gemini to analyze how well the guess fits the category.
        
        Returns:
            Tuple of (confidence_score 0-100, explanation)
        """
        if not self.model:
            return 50.0, "Gemini not available - using pattern match only"
        
        # Count blanks to help AI understand uncertainty
        blank_count = showing.count('_')
        
        # Simplified prompt - just ask about how famous/common the answer is
        prompt = f"""Rate how likely this Wheel of Fortune answer is correct.

Category: {category}
Answer: "{guess}"
Hidden letters remaining: {blank_count}

IMPORTANT: The answer already matches all revealed letters perfectly. DO NOT check pattern matching.

Your task: Rate how famous/common "{guess}" is as a {category}.

- "THE QUICK BROWN FOX" as a PHRASE = 95% (extremely famous)
- "HAPPY BIRTHDAY" as a PHRASE = 95% (extremely common)
- "MICHAEL JORDAN" as a PERSON = 95% (world famous)
- "EIFFEL TOWER" as a PLACE = 95% (iconic landmark)
- Some obscure phrase = 50-70%
- Nonsense or gibberish = 10-30%

How famous/recognizable is "{guess}" as a {category}?

Reply with ONLY:
CONFIDENCE: [number 0-100]
REASONING: [one short sentence]"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse the response
            confidence = 70.0  # Default to reasonable confidence
            reasoning = "Analysis complete"
            
            for line in response_text.split('\n'):
                if 'CONFIDENCE' in line.upper():
                    try:
                        # Extract just the number from anywhere in the line
                        conf_num = re.search(r'(\d+)', line)
                        if conf_num:
                            confidence = min(100, max(0, float(conf_num.group(1))))
                    except:
                        pass
                elif 'REASONING' in line.upper():
                    reasoning = re.sub(r'^REASONING[:\s]*', '', line, flags=re.IGNORECASE).strip()
            
            return confidence, reasoning
            
        except Exception as e:
            return 70.0, f"Gemini analysis error: {str(e)}"
    
    def calculate_remaining_possibilities(self, showing: str, previous_guesses: List[str]) -> Dict:
        """
        Estimate how many possible solutions could fit the pattern.
        This is a heuristic based on blank positions and unused letters.
        """
        blank_count = showing.count('_')
        
        # Letters not yet guessed
        all_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        guessed = set(l.upper() for l in previous_guesses)
        remaining_letters = all_letters - guessed
        
        # Rough estimate of possibilities
        # Each blank could be any of the remaining letters
        # This is a vast overestimate but gives a sense of uncertainty
        if blank_count == 0:
            possibilities = 1
        elif blank_count <= 3:
            possibilities = len(remaining_letters) ** blank_count
        else:
            # For many blanks, cap the estimate
            possibilities = min(len(remaining_letters) ** blank_count, 1000000)
        
        return {
            'blank_count': blank_count,
            'remaining_letters': len(remaining_letters),
            'estimated_possibilities': possibilities,
            'uncertainty_level': 'LOW' if blank_count <= 2 else 'MEDIUM' if blank_count <= 5 else 'HIGH'
        }
    
    def get_recommendation(self, confidence: float, blank_count: int) -> Tuple[str, str]:
        """
        Generate a recommendation based on confidence and puzzle state.
        
        Returns:
            Tuple of (recommendation, color_hint for display)
        """
        if confidence >= CONFIDENCE_HIGH:
            if blank_count <= 3:
                return "SOLVE NOW - High confidence!", "green"
            else:
                return "SOLVE - Good chance of success!", "green"
        elif confidence >= CONFIDENCE_MEDIUM:
            if blank_count <= 2:
                return "Consider solving - Decent odds", "yellow"
            else:
                return "Risky - Maybe guess more letters first", "yellow"
        else:
            return "WAIT - Keep guessing letters to be sure", "red"
    
    def analyze(self, showing: str, guess: str, category: str, previous_guesses: List[str] = None) -> Dict:
        """
        Complete analysis of a solve attempt.
        
        Args:
            showing: Current puzzle state with blanks as underscores
            guess: User's proposed solution
            category: Puzzle category (e.g., "PHRASE", "PERSON", "PLACE")
            previous_guesses: List of letters already guessed
        
        Returns:
            Dictionary with complete analysis results
        """
        if previous_guesses is None:
            previous_guesses = []
        
        results = {
            'guess': guess.upper(),
            'category': category.upper(),
            'pattern': showing,
        }
        
        # Step 1: Validate pattern match
        is_valid, pattern_score, pattern_msg = self.validate_pattern_match(showing, guess)
        results['pattern_match'] = {
            'valid': is_valid,
            'score': pattern_score,
            'message': pattern_msg
        }
        
        if not is_valid:
            results['overall_confidence'] = 0.0
            results['recommendation'] = "INVALID - Guess doesn't match the pattern"
            results['recommendation_color'] = "red"
            return results
        
        # Step 2: Check letter consistency
        is_consistent, consistency_msg = self.check_letter_consistency(showing, guess, previous_guesses)
        results['letter_consistency'] = {
            'valid': is_consistent,
            'message': consistency_msg
        }
        
        if not is_consistent:
            results['overall_confidence'] = 0.0
            results['recommendation'] = f"INVALID - {consistency_msg}"
            results['recommendation_color'] = "red"
            return results
        
        # Step 3: Calculate remaining possibilities
        possibilities = self.calculate_remaining_possibilities(showing, previous_guesses)
        results['possibilities'] = possibilities
        
        # Step 4: Gemini analysis (if available)
        gemini_confidence, gemini_reasoning = self.analyze_with_gemini(
            showing, guess, category, previous_guesses
        )
        results['gemini_analysis'] = {
            'confidence': gemini_confidence,
            'reasoning': gemini_reasoning
        }
        
        # Step 5: Calculate overall confidence
        # Weight Gemini analysis heavily since it understands context
        overall_confidence = gemini_confidence
        
        # Only apply blank penalty if Gemini isn't already highly confident
        # If AI says it's a famous phrase (>85%), trust it regardless of blanks
        if gemini_confidence < 85:
            # Small penalty for uncertainty when many blanks remain
            blank_factor = max(0.85, 1.0 - (possibilities['blank_count'] * 0.02))
            overall_confidence *= blank_factor
        # If very few blanks and high confidence, boost slightly
        elif possibilities['blank_count'] <= 3 and gemini_confidence >= 90:
            overall_confidence = min(99, overall_confidence + 3)
        
        results['overall_confidence'] = round(overall_confidence, 1)
        
        # Step 6: Generate recommendation
        recommendation, color = self.get_recommendation(
            overall_confidence, 
            possibilities['blank_count']
        )
        results['recommendation'] = recommendation
        results['recommendation_color'] = color
        
        return results
    
    def print_analysis(self, results: Dict):
        """Pretty print the analysis results."""
        print("\n" + "=" * 60)
        print("           SOLVE ADVISOR ANALYSIS")
        print("=" * 60)
        
        print(f"\n  Your Guess: \"{results['guess']}\"")
        print(f"  Category:   {results['category']}")
        print(f"  Pattern:    {results['pattern']}")
        
        print("\n" + "-" * 60)
        print("  ANALYSIS BREAKDOWN")
        print("-" * 60)
        
        # Pattern match
        pm = results['pattern_match']
        status = "✓" if pm['valid'] else "✗"
        print(f"\n  {status} Pattern Match: {pm['message']}")
        
        # Letter consistency
        if 'letter_consistency' in results:
            lc = results['letter_consistency']
            status = "✓" if lc['valid'] else "✗"
            print(f"  {status} {lc['message']}")
        
        # Possibilities
        if 'possibilities' in results:
            poss = results['possibilities']
            print(f"\n  Blanks remaining: {poss['blank_count']}")
            print(f"  Uncertainty level: {poss['uncertainty_level']}")
        
        # Gemini analysis
        if 'gemini_analysis' in results:
            ga = results['gemini_analysis']
            print(f"\n  AI Category Analysis:")
            print(f"    Confidence: {ga['confidence']}%")
            print(f"    Reasoning: {ga['reasoning']}")
        
        print("\n" + "-" * 60)
        print("  FINAL VERDICT")
        print("-" * 60)
        
        conf = results['overall_confidence']
        conf_bar = "█" * int(conf / 5) + "░" * (20 - int(conf / 5))
        print(f"\n  Overall Confidence: {conf}%")
        print(f"  [{conf_bar}]")
        
        print(f"\n  → {results['recommendation']}")
        print("\n" + "=" * 60)


def interactive_advisor():
    """Run the solve advisor in interactive mode."""
    print("\n" + "=" * 60)
    print("     WHEEL OF FORTUNE - SOLVE ADVISOR")
    print("=" * 60)
    
    # Check for API key
    api_key = get_api_key()
    if not api_key:
        print("\nNo Gemini API key found!")
        print("Get one free at: https://makersuite.google.com/app/apikey")
        api_key = input("\nEnter your Gemini API key (or press Enter to skip): ").strip()
        if api_key:
            save = input("Save this key for future use? (y/n): ").lower()
            if save == 'y':
                set_api_key(api_key)
    
    advisor = SolveAdvisor(api_key)
    
    while True:
        print("\n" + "-" * 40)
        print("Enter puzzle details (or 'quit' to exit)")
        print("-" * 40)
        
        showing = input("\nCurrent puzzle (use _ for blanks): ").strip()
        if showing.lower() == 'quit':
            break
        
        category = input("Category (e.g., PHRASE, PERSON, PLACE): ").strip()
        if not category:
            category = "PHRASE"
        
        guess = input("Your proposed solution: ").strip()
        
        guesses_input = input("Letters already guessed (space-separated, or Enter for none): ").strip()
        previous_guesses = guesses_input.upper().split() if guesses_input else []
        
        # Run analysis
        results = advisor.analyze(showing, guess, category, previous_guesses)
        advisor.print_analysis(results)
        
        another = input("\nAnalyze another guess? (y/n): ").lower()
        if another != 'y':
            break
    
    print("\nThanks for using the Solve Advisor! Good luck!")


if __name__ == "__main__":
    interactive_advisor()

