import os
import sys
import pytest
import tempfile
from pathlib import Path

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from letter_chooser import (
    _normalize_pattern, _load_candidates, _pattern_to_regex_str,
    LetterChooserAI, FREE_LETTERS, VOWELS, CONSONANTS
)


class TestNormalizePatternLetterChooser:
    """Test the _normalize_pattern function in letter_chooser."""
    
    def test_normalize_pattern_list_input(self):
        """Test normalizing a list pattern."""
        pattern = ['H', 'E', '_', '_', 'O']
        result = _normalize_pattern(pattern)
        assert result == "HE__O"
    
    def test_normalize_pattern_string_input(self):
        """Test normalizing a string pattern."""
        pattern = "HE__O"
        result = _normalize_pattern(pattern)
        assert result == "HE__O"
    
    def test_normalize_pattern_with_spaces(self):
        """Test normalizing pattern with spaces."""
        pattern = "HE_ _O W_RLD"
        result = _normalize_pattern(pattern)
        assert result == "HE_ _O W_RLD"
    
    def test_normalize_pattern_lowercase(self):
        """Test that lowercase is converted to uppercase."""
        pattern = "he__o"
        result = _normalize_pattern(pattern)
        assert result == "HE__O"


class TestLoadCandidatesLetterChooser:
    """Test the _load_candidates function in letter_chooser."""
    
    def test_load_candidates_existing_file(self):
        """Test loading candidates from an existing file."""
        content = "HELLO WORLD\nWHEEL OF FORTUNE\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            candidates = _load_candidates(temp_file)
            expected = ["HELLO WORLD", "WHEEL OF FORTUNE"]
            assert candidates == expected
        finally:
            os.unlink(temp_file)
    
    def test_load_candidates_nonexistent_file(self):
        """Test loading candidates from non-existent file returns empty list."""
        candidates = _load_candidates("nonexistent_file.txt")
        assert candidates == []


class TestPatternToRegexStr:
    """Test the _pattern_to_regex_str function."""
    
    def test_pattern_to_regex_str_basic(self):
        """Test basic pattern to regex string conversion."""
        pattern = "HE__O"
        regex_str = _pattern_to_regex_str(pattern)
        expected = "^HE..O$"
        assert regex_str == expected
    
    def test_pattern_to_regex_str_with_spaces(self):
        """Test pattern with spaces."""
        pattern = "HE_ _O W_RLD"
        regex_str = _pattern_to_regex_str(pattern)
        expected = "^HE. .O W.RLD$"
        assert regex_str == expected
    
    def test_pattern_to_regex_str_special_chars(self):
        """Test pattern with special regex characters."""
        pattern = "A.B+C*"
        regex_str = _pattern_to_regex_str(pattern)
        # Special chars should be escaped
        assert "\\." in regex_str
        assert "\\+" in regex_str
        assert "\\*" in regex_str


class TestConstants:
    """Test the constants used in letter_chooser."""
    
    def test_free_letters(self):
        """Test FREE_LETTERS constant."""
        expected = {"R", "S", "T", "L", "N", "E"}
        assert FREE_LETTERS == expected
    
    def test_vowels(self):
        """Test VOWELS constant."""
        expected = {"A", "E", "I", "O", "U"}
        assert VOWELS == expected
    
    def test_consonants(self):
        """Test CONSONANTS constant."""
        # Should be all letters minus vowels
        expected = set("BCDFGHJKLMNPQRSTVWXYZ")
        assert CONSONANTS == expected
    
    def test_vowels_consonants_disjoint(self):
        """Test that vowels and consonants don't overlap."""
        assert VOWELS.isdisjoint(CONSONANTS)
    
    def test_vowels_consonants_complete(self):
        """Test that vowels and consonants cover all letters."""
        all_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        assert VOWELS | CONSONANTS == all_letters


class TestLetterChooserAI:
    """Test the LetterChooserAI class."""
    
    def setup_method(self):
        """Set up test data for each test."""
        # Create a temporary puzzle file
        self.test_puzzles = [
            "HELLO WORLD",
            "WHEEL OF FORTUNE", 
            "PYTHON PROGRAMMING",
            "ARTIFICIAL INTELLIGENCE",
            "MACHINE LEARNING",
            "COMPUTER SCIENCE"
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write('\n'.join(self.test_puzzles))
            self.temp_file = f.name
    
    def teardown_method(self):
        """Clean up after each test."""
        if hasattr(self, 'temp_file'):
            os.unlink(self.temp_file)
    
    def test_init_with_existing_file(self):
        """Test initialization with existing puzzle file."""
        chooser = LetterChooserAI(self.temp_file)
        assert chooser.puzzles_file == self.temp_file
    
    def test_init_with_default_file(self):
        """Test initialization with default file."""
        chooser = LetterChooserAI()
        assert chooser.puzzles_file == "data/bonus_puzzles.txt"
    
    def test_choose_letters_basic(self):
        """Test basic letter choosing functionality."""
        chooser = LetterChooserAI(self.temp_file)
        
        # Pattern for "HELLO WORLD" with free letters revealed
        pattern = "_E__O WOR_D"  # R, S, T, L, N, E are free
        picks = chooser.choose_letters(pattern)
        
        # Should return 4 letters: 3 consonants + 1 vowel
        assert len(picks) == 4
        assert isinstance(picks, str)
        
        # Last letter should be a vowel
        assert picks[-1] in VOWELS
        
        # First 3 should be consonants
        for i in range(3):
            assert picks[i] in CONSONANTS
    
    def test_choose_letters_with_custom_candidates(self):
        """Test choosing letters with custom candidate list."""
        chooser = LetterChooserAI(self.temp_file)
        
        custom_candidates = ["HELLO WORLD", "HELLO THERE"]
        pattern = "_E__O W____"
        picks = chooser.choose_letters(pattern, candidates=custom_candidates)
        
        assert len(picks) == 4
        assert picks[-1] in VOWELS
    
    def test_choose_letters_no_matching_candidates(self):
        """Test choosing letters when no candidates match pattern."""
        chooser = LetterChooserAI(self.temp_file)
        
        # Pattern that won't match any puzzles
        pattern = "ZZZZZ ZZZZZ"
        picks = chooser.choose_letters(pattern)
        
        # Should still return 4 letters using fallback logic
        assert len(picks) == 4
        assert picks[-1] in VOWELS
    
    def test_choose_letters_excludes_free_letters(self):
        """Test that chosen letters don't include free letters."""
        chooser = LetterChooserAI(self.temp_file)
        
        pattern = "_____ _____"
        picks = chooser.choose_letters(pattern)
        
        # None of the picks should be free letters
        for letter in picks:
            assert letter not in FREE_LETTERS
    
    def test_choose_letters_excludes_revealed_letters(self):
        """Test that chosen letters don't include already revealed letters."""
        chooser = LetterChooserAI(self.temp_file)
        
        # Pattern with some letters already revealed
        pattern = "HE__O W_R_D"
        picks = chooser.choose_letters(pattern)
        
        # Picks shouldn't include H, E, O, W, R, D
        revealed = {"H", "E", "O", "W", "R", "D"}
        for letter in picks:
            assert letter not in revealed
    
    def test_choose_letters_list_pattern(self):
        """Test choosing letters with list pattern input."""
        chooser = LetterChooserAI(self.temp_file)
        
        pattern = ['H', 'E', '_', '_', 'O', ' ', 'W', '_', 'R', '_', 'D']
        picks = chooser.choose_letters(pattern)
        
        assert len(picks) == 4
        assert picks[-1] in VOWELS
    
    def test_choose_letters_fallback_vowel(self):
        """Test vowel fallback when no vowels have frequency."""
        chooser = LetterChooserAI(self.temp_file)
        
        # Create a scenario where vowels might not appear in unrevealed positions
        # by using a pattern that reveals most vowels
        pattern = "A E I O U"  # All vowels revealed
        picks = chooser.choose_letters(pattern)
        
        # Should still pick a vowel (fallback to 'A')
        assert len(picks) == 4
        assert picks[-1] in VOWELS
    
    def test_choose_letters_fallback_consonants(self):
        """Test consonant fallback when no consonants have frequency."""
        chooser = LetterChooserAI(self.temp_file)
        
        # Use empty candidates to trigger fallback
        picks = chooser.choose_letters("_____ _____", candidates=[])
        
        assert len(picks) == 4
        assert picks[-1] in VOWELS
        
        # First 3 should be consonants from fallback order
        for i in range(3):
            assert picks[i] in CONSONANTS
    
    def test_choose_letters_length_mismatch_handling(self):
        """Test handling of candidates with different lengths than pattern."""
        chooser = LetterChooserAI(self.temp_file)
        
        # Pattern length that doesn't match any puzzle exactly
        pattern = "___"  # 3 letters, but our puzzles are longer
        picks = chooser.choose_letters(pattern)
        
        # Should still work and return 4 letters
        assert len(picks) == 4
        assert picks[-1] in VOWELS
    
    def test_choose_letters_empty_pattern(self):
        """Test choosing letters with empty pattern."""
        chooser = LetterChooserAI(self.temp_file)
        
        pattern = ""
        picks = chooser.choose_letters(pattern)
        
        # Should handle gracefully and return 4 letters
        assert len(picks) == 4
        assert picks[-1] in VOWELS
    
    def test_choose_letters_frequency_based_selection(self):
        """Test that letter selection is based on frequency in candidates."""
        # Create a puzzle file where certain letters appear more frequently
        frequent_puzzles = [
            "AAAAA BBBBB",  # A and B appear frequently
            "AAAAA CCCCC",  # A and C appear frequently  
            "AAAAA DDDDD",  # A and D appear frequently
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write('\n'.join(frequent_puzzles))
            temp_file = f.name
        
        try:
            chooser = LetterChooserAI(temp_file)
            pattern = "_____ _____"
            picks = chooser.choose_letters(pattern)
            
            # A should be chosen as the vowel (most frequent)
            assert picks[-1] == 'A'
            
            # B, C, D should likely be chosen as consonants (most frequent)
            consonant_picks = picks[:3]
            frequent_consonants = {'B', 'C', 'D'}
            # At least some of the frequent consonants should be picked
            assert len(set(consonant_picks) & frequent_consonants) > 0
            
        finally:
            os.unlink(temp_file)