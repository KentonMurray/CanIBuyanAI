import os
import sys
import pytest

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from bonus_round import BonusRoundGame


class TestBonusRoundGame:
    """Test the BonusRoundGame class."""
    
    def test_init_basic(self):
        """Test basic initialization."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        assert game.solution == "HELLO WORLD"
        # Pattern should have free letters (RSTLNE) revealed
        expected_pattern = ["_", "E", "L", "L", "_", " ", "_", "_", "R", "L", "_"]
        assert game.pattern == expected_pattern
    
    def test_init_lowercase_solution(self):
        """Test initialization with lowercase solution."""
        solution = "hello world"
        game = BonusRoundGame(solution)
        
        assert game.solution == "HELLO WORLD"
        expected_pattern = ["_", "E", "L", "L", "_", " ", "_", "_", "R", "L", "_"]
        assert game.pattern == expected_pattern
    
    def test_init_mixed_case_solution(self):
        """Test initialization with mixed case solution."""
        solution = "Hello World"
        game = BonusRoundGame(solution)
        
        assert game.solution == "HELLO WORLD"
        expected_pattern = ["_", "E", "L", "L", "_", " ", "_", "_", "R", "L", "_"]
        assert game.pattern == expected_pattern
    
    def test_init_solution_with_free_letters_only(self):
        """Test initialization with solution containing only free letters."""
        solution = "RSTLNE"
        game = BonusRoundGame(solution)
        
        assert game.solution == "RSTLNE"
        expected_pattern = ["R", "S", "T", "L", "N", "E"]
        assert game.pattern == expected_pattern
    
    def test_init_solution_with_no_free_letters(self):
        """Test initialization with solution containing no free letters."""
        solution = "QUIZ"
        game = BonusRoundGame(solution)
        
        assert game.solution == "QUIZ"
        expected_pattern = ["_", "_", "_", "_"]
        assert game.pattern == expected_pattern
    
    def test_get_pattern(self):
        """Test getting the current pattern."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        pattern = game.get_pattern()
        expected_pattern = ["_", "E", "L", "L", "_", " ", "_", "_", "R", "L", "_"]
        assert pattern == expected_pattern
    
    def test_apply_player_letters_basic(self):
        """Test applying player letter choices."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        # Apply player picks
        game.apply_player_letters("HO")
        
        expected_pattern = ["H", "E", "L", "L", "O", " ", "_", "O", "R", "L", "_"]
        assert game.pattern == expected_pattern
    
    def test_apply_player_letters_no_matches(self):
        """Test applying player letters that don't match."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        original_pattern = game.pattern.copy()
        game.apply_player_letters("XYZ")
        
        # Pattern should remain unchanged
        assert game.pattern == original_pattern
    
    def test_apply_player_letters_case_insensitive(self):
        """Test that player letters are case insensitive."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        game.apply_player_letters("ho")  # lowercase
        
        expected_pattern = ["H", "E", "L", "L", "O", " ", "_", "O", "R", "L", "_"]
        assert game.pattern == expected_pattern
    
    def test_guess_correct(self):
        """Test making a correct guess."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        assert game.guess("HELLO WORLD") is True
        assert game.guess("hello world") is True  # case insensitive
        assert game.guess("Hello World") is True  # mixed case
    
    def test_guess_incorrect(self):
        """Test making an incorrect guess."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        assert game.guess("GOODBYE WORLD") is False
        assert game.guess("HELLO") is False
        assert game.guess("") is False
    
    def test_is_solved_initially_false(self):
        """Test that puzzle is not initially solved."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        assert game.is_solved() is False
    
    def test_is_solved_after_revealing_all_letters(self):
        """Test that puzzle is solved after revealing all letters."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        # Reveal all remaining letters
        game.apply_player_letters("HOWDZ")  # H, O, W, D should complete it
        
        assert game.is_solved() is True
    
    def test_is_solved_solution_with_only_free_letters(self):
        """Test solving puzzle with only free letters."""
        solution = "RSTLNE"
        game = BonusRoundGame(solution)
        
        # Should be solved immediately since all letters are free
        assert game.is_solved() is True
    
    def test_workflow_complete_game(self):
        """Test a complete game workflow."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        # Initial state
        assert not game.is_solved()
        assert game.guess("HELLO WORLD") is True  # Can guess even without revealing
        
        # Apply some letters
        game.apply_player_letters("HO")
        pattern = game.get_pattern()
        assert "H" in pattern
        assert "O" in pattern
        
        # Still not fully solved
        assert not game.is_solved()
        
        # Apply remaining letters
        game.apply_player_letters("WD")
        
        # Now should be solved
        assert game.is_solved()
        assert game.guess("HELLO WORLD") is True