import os
import sys
import pytest

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import apply_free_letters, apply_player_letters, FREE_LETTERS


class TestApplyFreeLetters:
    """Test the apply_free_letters function."""
    
    def test_apply_free_letters_basic(self):
        """Test basic functionality with RSTLNE letters."""
        solution = "HELLO WORLD"
        result = apply_free_letters(solution)
        expected = ["_", "E", "L", "L", "_", " ", "_", "_", "R", "L", "_"]
        assert result == expected
    
    def test_apply_free_letters_all_free(self):
        """Test with solution containing only free letters."""
        solution = "RSTLNE"
        result = apply_free_letters(solution)
        expected = ["R", "S", "T", "L", "N", "E"]
        assert result == expected
    
    def test_apply_free_letters_no_free(self):
        """Test with solution containing no free letters."""
        solution = "QUIZ"
        result = apply_free_letters(solution)
        expected = ["_", "_", "_", "_"]
        assert result == expected
    
    def test_apply_free_letters_with_spaces(self):
        """Test with multiple words and spaces."""
        solution = "THE BEST"
        result = apply_free_letters(solution)
        expected = ["T", "_", "E", " ", "_", "E", "S", "T"]
        assert result == expected
    
    def test_apply_free_letters_empty_string(self):
        """Test with empty string."""
        solution = ""
        result = apply_free_letters(solution)
        expected = []
        assert result == expected
    
    def test_apply_free_letters_only_spaces(self):
        """Test with only spaces."""
        solution = "   "
        result = apply_free_letters(solution)
        expected = [" ", " ", " "]
        assert result == expected


class TestApplyPlayerLetters:
    """Test the apply_player_letters function."""
    
    def test_apply_player_letters_basic(self):
        """Test basic functionality with player picks."""
        solution = "HELLO WORLD"
        pattern = ["_", "E", "L", "L", "_", " ", "_", "_", "R", "L", "_"]
        picks = "HO"
        result = apply_player_letters(solution, pattern, picks)
        expected = ["H", "E", "L", "L", "O", " ", "_", "O", "R", "L", "_"]
        assert result == expected
    
    def test_apply_player_letters_no_matches(self):
        """Test when player picks don't match any letters."""
        solution = "HELLO"
        pattern = ["_", "E", "L", "L", "_"]
        picks = "XYZ"
        result = apply_player_letters(solution, pattern, picks)
        expected = ["_", "E", "L", "L", "_"]
        assert result == expected
    
    def test_apply_player_letters_all_matches(self):
        """Test when all player picks match."""
        solution = "ABC"
        pattern = ["_", "_", "_"]
        picks = "ABC"
        result = apply_player_letters(solution, pattern, picks)
        expected = ["A", "B", "C"]
        assert result == expected
    
    def test_apply_player_letters_preserve_existing(self):
        """Test that existing revealed letters are preserved."""
        solution = "HELLO"
        pattern = ["H", "E", "_", "_", "O"]
        picks = "L"
        result = apply_player_letters(solution, pattern, picks)
        expected = ["H", "E", "L", "L", "O"]
        assert result == expected
    
    def test_apply_player_letters_case_insensitive(self):
        """Test that picks are case insensitive."""
        solution = "HELLO"
        pattern = ["_", "E", "L", "L", "_"]
        picks = "ho"  # lowercase
        result = apply_player_letters(solution, pattern, picks)
        expected = ["H", "E", "L", "L", "O"]
        assert result == expected
    
    def test_apply_player_letters_with_spaces(self):
        """Test with spaces in solution."""
        solution = "HI THERE"
        pattern = ["_", "_", " ", "T", "_", "E", "R", "E"]
        picks = "IH"
        result = apply_player_letters(solution, pattern, picks)
        expected = ["H", "I", " ", "T", "H", "E", "R", "E"]
        assert result == expected
    
    def test_apply_player_letters_duplicate_picks(self):
        """Test with duplicate letters in picks."""
        solution = "HELLO"
        pattern = ["_", "E", "L", "L", "_"]
        picks = "HHO"  # duplicate H
        result = apply_player_letters(solution, pattern, picks)
        expected = ["H", "E", "L", "L", "O"]
        assert result == expected
    
    def test_apply_player_letters_empty_picks(self):
        """Test with empty picks string."""
        solution = "HELLO"
        pattern = ["_", "E", "L", "L", "_"]
        picks = ""
        result = apply_player_letters(solution, pattern, picks)
        expected = ["_", "E", "L", "L", "_"]
        assert result == expected


class TestFreeLetters:
    """Test the FREE_LETTERS constant."""
    
    def test_free_letters_content(self):
        """Test that FREE_LETTERS contains the correct letters."""
        expected = {"R", "S", "T", "L", "N", "E"}
        assert FREE_LETTERS == expected
    
    def test_free_letters_count(self):
        """Test that FREE_LETTERS has the correct count."""
        assert len(FREE_LETTERS) == 6