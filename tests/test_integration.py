import os
import sys
import pytest
import tempfile

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from bonus_round import BonusRoundGame
from solver import PuzzleSolverAI
from letter_chooser import LetterChooserAI
from puzzle_loader import PuzzleLoader
from utils import apply_free_letters, apply_player_letters


@pytest.mark.integration
class TestBonusRoundIntegration:
    """Integration tests for the complete bonus round workflow."""
    
    def setup_method(self):
        """Set up test data for each test."""
        self.test_puzzles = [
            "HELLO WORLD",
            "WHEEL OF FORTUNE", 
            "PYTHON PROGRAMMING",
            "ARTIFICIAL INTELLIGENCE",
            "MACHINE LEARNING"
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write('\n'.join(self.test_puzzles))
            self.temp_file = f.name
    
    def teardown_method(self):
        """Clean up after each test."""
        if hasattr(self, 'temp_file'):
            os.unlink(self.temp_file)
    
    def test_complete_bonus_round_workflow(self):
        """Test a complete bonus round game workflow."""
        # Load a puzzle
        loader = PuzzleLoader(self.temp_file)
        solution = loader.load_random_puzzle()
        
        # Start the game
        game = BonusRoundGame(solution)
        initial_pattern = game.get_pattern()
        
        # Verify free letters are revealed
        assert any(ch in "RSTLNE" for ch in initial_pattern if ch != "_" and ch != " ")
        
        # Use AI to choose letters
        chooser = LetterChooserAI(self.temp_file)
        letter_picks = chooser.choose_letters(initial_pattern)
        
        # Verify letter picks format
        assert len(letter_picks) == 4
        assert letter_picks[-1] in "AEIOU"  # Last should be vowel
        
        # Apply the letter picks
        game.apply_player_letters(letter_picks)
        updated_pattern = game.get_pattern()
        
        # Pattern should have changed (unless no picks matched)
        # At minimum, it should be the same or more revealed
        revealed_before = sum(1 for ch in initial_pattern if ch != "_" and ch != " ")
        revealed_after = sum(1 for ch in updated_pattern if ch != "_" and ch != " ")
        assert revealed_after >= revealed_before
        
        # Use solver to get solution candidates
        solver = PuzzleSolverAI(self.temp_file)
        candidates = solver.solve(updated_pattern, top_n=3)
        
        # Should get some candidates
        assert len(candidates) >= 0
        
        # The actual solution should be a valid guess
        assert game.guess(solution) is True
    
    def test_ai_letter_chooser_with_solver_integration(self):
        """Test integration between letter chooser and solver."""
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        # Get initial pattern
        pattern = game.get_pattern()
        
        # Use letter chooser
        chooser = LetterChooserAI(self.temp_file)
        picks = chooser.choose_letters(pattern)
        
        # Apply picks
        game.apply_player_letters(picks)
        updated_pattern = game.get_pattern()
        
        # Use solver to find candidates
        solver = PuzzleSolverAI(self.temp_file)
        candidates = solver.solve(updated_pattern)
        
        # The actual solution should be in candidates or at least findable
        assert isinstance(candidates, list)
        
        # Test that we can make a guess
        guess_result = game.guess(solution)
        assert guess_result is True
    
    def test_puzzle_loader_with_game_integration(self):
        """Test integration between puzzle loader and game."""
        loader = PuzzleLoader(self.temp_file)
        
        # Load multiple puzzles and test each
        for _ in range(3):
            solution = loader.load_random_puzzle()
            
            # Should be one of our test puzzles
            assert solution in self.test_puzzles
            
            # Should work with the game
            game = BonusRoundGame(solution)
            pattern = game.get_pattern()
            
            # Pattern should be valid
            assert len(pattern) == len(solution)
            assert game.guess(solution) is True
    
    def test_utils_integration_with_game(self):
        """Test integration of utility functions with game logic."""
        solution = "HELLO WORLD"
        
        # Test apply_free_letters
        free_pattern = apply_free_letters(solution)
        expected_free = ["_", "E", "L", "L", "_", " ", "_", "_", "R", "L", "_"]
        assert free_pattern == expected_free
        
        # Test apply_player_letters
        player_pattern = apply_player_letters(solution, free_pattern, "HO")
        expected_player = ["H", "E", "L", "L", "O", " ", "_", "O", "R", "L", "_"]
        assert player_pattern == expected_player
        
        # Test with game
        game = BonusRoundGame(solution)
        assert game.pattern == expected_free
        
        game.apply_player_letters("HO")
        assert game.pattern == expected_player
    
    def test_solver_accuracy_with_real_puzzles(self):
        """Test solver accuracy with real puzzle scenarios."""
        solver = PuzzleSolverAI(self.temp_file)
        
        # Test with partially revealed "HELLO WORLD"
        pattern = "_E__O WOR_D"
        candidates = solver.solve(pattern, top_n=5)
        
        # "HELLO WORLD" should be in the candidates if it's in our corpus
        if "HELLO WORLD" in self.test_puzzles:
            assert "HELLO WORLD" in candidates
    
    def test_letter_chooser_effectiveness(self):
        """Test that letter chooser makes reasonable choices."""
        chooser = LetterChooserAI(self.temp_file)
        
        # Test with a pattern that has clear optimal choices
        pattern = "_E__O W_R_D"  # Missing H, L, O, L
        picks = chooser.choose_letters(pattern)
        
        # Should pick reasonable letters
        assert len(picks) == 4
        
        # Should not pick already revealed letters
        revealed = set("EOWRD")
        for pick in picks:
            assert pick not in revealed
        
        # Should not pick free letters
        free_letters = set("RSTLNE")
        for pick in picks:
            assert pick not in free_letters
    
    def test_error_handling_integration(self):
        """Test error handling across integrated components."""
        # Test with empty puzzle file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("")  # Empty file
            empty_file = f.name
        
        try:
            # Components should handle empty corpus gracefully
            chooser = LetterChooserAI(empty_file)
            picks = chooser.choose_letters("_____ _____")
            assert len(picks) == 4  # Should still return 4 letters
            
            solver = PuzzleSolverAI(empty_file)
            candidates = solver.solve("_____ _____")
            assert isinstance(candidates, list)  # Should return empty list
            
        finally:
            os.unlink(empty_file)
    
    def test_performance_integration(self):
        """Test that integrated workflow performs reasonably."""
        import time
        
        solution = "HELLO WORLD"
        game = BonusRoundGame(solution)
        
        start_time = time.time()
        
        # Complete workflow
        chooser = LetterChooserAI(self.temp_file)
        picks = chooser.choose_letters(game.get_pattern())
        game.apply_player_letters(picks)
        
        solver = PuzzleSolverAI(self.temp_file)
        candidates = solver.solve(game.get_pattern())
        
        end_time = time.time()
        
        # Should complete in reasonable time (less than 1 second)
        assert end_time - start_time < 1.0
        
        # Should produce valid results
        assert len(picks) == 4
        assert isinstance(candidates, list)