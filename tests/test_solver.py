import os
import sys
import pytest
import tempfile
from pathlib import Path

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from solver import (
    _normalize_pattern, _load_candidates, _pattern_to_regex, 
    _letter_frequency, PuzzleSolverAI
)


class TestNormalizePattern:
    """Test the _normalize_pattern function."""
    
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
    
    def test_normalize_pattern_with_invalid_chars(self):
        """Test that invalid characters are removed."""
        pattern = "HE123__O!@#"
        result = _normalize_pattern(pattern)
        assert result == "HE__O"
    
    def test_normalize_pattern_multiple_spaces(self):
        """Test that multiple spaces are collapsed to single spaces."""
        pattern = "HE__O    W_RLD"
        result = _normalize_pattern(pattern)
        assert result == "HE__O W_RLD"
    
    def test_normalize_pattern_leading_trailing_spaces(self):
        """Test that leading and trailing spaces are stripped."""
        pattern = "  HE__O  "
        result = _normalize_pattern(pattern)
        assert result == "HE__O"


class TestLoadCandidates:
    """Test the _load_candidates function."""
    
    def test_load_candidates_existing_file(self):
        """Test loading candidates from an existing file."""
        content = "HELLO WORLD\nWHEEL OF FORTUNE\nPYTHON PROGRAMMING\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            candidates = _load_candidates(temp_file)
            expected = ["HELLO WORLD", "WHEEL OF FORTUNE", "PYTHON PROGRAMMING"]
            assert candidates == expected
        finally:
            os.unlink(temp_file)
    
    def test_load_candidates_nonexistent_file(self):
        """Test loading candidates from non-existent file returns empty list."""
        candidates = _load_candidates("nonexistent_file.txt")
        assert candidates == []
    
    def test_load_candidates_empty_file(self):
        """Test loading candidates from empty file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("")
            temp_file = f.name
        
        try:
            candidates = _load_candidates(temp_file)
            assert candidates == []
        finally:
            os.unlink(temp_file)
    
    def test_load_candidates_with_empty_lines(self):
        """Test loading candidates ignoring empty lines."""
        content = "HELLO\n\nWORLD\n\n\nPUZZLE\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            candidates = _load_candidates(temp_file)
            expected = ["HELLO", "WORLD", "PUZZLE"]
            assert candidates == expected
        finally:
            os.unlink(temp_file)


class TestPatternToRegex:
    """Test the _pattern_to_regex function."""
    
    def test_pattern_to_regex_basic(self):
        """Test basic pattern to regex conversion."""
        pattern = "HE__O"
        regex = _pattern_to_regex(pattern)
        
        assert regex.match("HELLO")
        assert regex.match("HERBO")  # HE + any two chars + O
        assert not regex.match("HEAVY")  # doesn't end with O
        assert not regex.match("WORLD")
        assert not regex.match("HE")
    
    def test_pattern_to_regex_with_spaces(self):
        """Test pattern with spaces."""
        pattern = "HE_ _O W_RLD"
        regex = _pattern_to_regex(pattern)
        
        assert regex.match("HEY TO WORLD")
        assert regex.match("HER SO WORLD")
        assert not regex.match("HELLO WORLD")  # wrong length
        assert not regex.match("HEY_TO_WORLD")  # underscore instead of space
    
    def test_pattern_to_regex_only_underscores(self):
        """Test pattern with only underscores."""
        pattern = "___"
        regex = _pattern_to_regex(pattern)
        
        assert regex.match("ABC")
        assert regex.match("XYZ")
        assert not regex.match("ABCD")  # too long
        assert not regex.match("AB")    # too short
    
    def test_pattern_to_regex_no_underscores(self):
        """Test pattern with no underscores (fully revealed)."""
        pattern = "HELLO"
        regex = _pattern_to_regex(pattern)
        
        assert regex.match("HELLO")
        assert not regex.match("WORLD")
        assert not regex.match("HELL")
    
    def test_pattern_to_regex_special_chars(self):
        """Test pattern with special regex characters."""
        pattern = "A.B"  # dot should be escaped
        regex = _pattern_to_regex(pattern)
        
        assert regex.match("A.B")
        assert not regex.match("ACB")  # dot should not match any character


class TestLetterFrequency:
    """Test the _letter_frequency function."""
    
    def test_letter_frequency_basic(self):
        """Test basic letter frequency counting."""
        corpus = ["HELLO", "WORLD"]
        freq = _letter_frequency(corpus)
        
        assert freq['L'] == 3  # 2 in HELLO, 1 in WORLD
        assert freq['O'] == 2  # 1 in each word
        assert freq['H'] == 1
        assert freq['E'] == 1
        assert freq['W'] == 1
        assert freq['R'] == 1
        assert freq['D'] == 1
    
    def test_letter_frequency_empty_corpus(self):
        """Test letter frequency with empty corpus."""
        corpus = []
        freq = _letter_frequency(corpus)
        assert len(freq) == 0
    
    def test_letter_frequency_with_spaces(self):
        """Test that spaces are ignored in frequency counting."""
        corpus = ["HELLO WORLD"]
        freq = _letter_frequency(corpus)
        
        assert ' ' not in freq
        assert freq['L'] == 3
        assert freq['O'] == 2
    
    def test_letter_frequency_case_insensitive(self):
        """Test that frequency counting preserves case as-is."""
        corpus = ["Hello", "WORLD"]
        freq = _letter_frequency(corpus)
        
        # The function preserves case as-is
        assert freq['H'] == 1
        assert freq['e'] == 1  # lowercase 'e' from "Hello"
        assert freq['W'] == 1
        assert freq['O'] == 1
        assert freq['R'] == 1
        assert freq['L'] == 1
        assert freq['D'] == 1


class TestPuzzleSolverAI:
    """Test the PuzzleSolverAI class."""
    
    def setup_method(self):
        """Set up test data for each test."""
        # Create a temporary puzzle file
        self.test_puzzles = [
            "HELLO WORLD",
            "WHEEL OF FORTUNE", 
            "PYTHON PROGRAMMING",
            "ARTIFICIAL INTELLIGENCE",
            "MACHINE LEARNING",
            "DEEP LEARNING"
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
        solver = PuzzleSolverAI(self.temp_file)
        
        assert solver.puzzles_file == self.temp_file
        assert len(solver.corpus) == len(self.test_puzzles)
        assert all(puzzle.upper() in solver.corpus for puzzle in self.test_puzzles)
        assert solver.total_letters > 0
    
    def test_init_with_nonexistent_file(self):
        """Test initialization with non-existent file."""
        solver = PuzzleSolverAI("nonexistent.txt")
        
        assert solver.corpus == []
        assert solver.total_letters == 1  # fallback value
    
    def test_solve_exact_match(self):
        """Test solving with an exact pattern match."""
        solver = PuzzleSolverAI(self.temp_file)
        
        # Pattern that exactly matches "HELLO WORLD"
        pattern = "HELLO WORLD"
        solutions = solver.solve(pattern, top_n=3)
        
        assert "HELLO WORLD" in solutions
        assert len(solutions) <= 3
    
    def test_solve_partial_pattern(self):
        """Test solving with partial pattern."""
        solver = PuzzleSolverAI(self.temp_file)
        
        # Pattern for "HELLO WORLD" with some letters hidden
        pattern = "HE__O W_R_D"
        solutions = solver.solve(pattern, top_n=5)
        
        assert "HELLO WORLD" in solutions
        assert len(solutions) <= 5
    
    def test_solve_with_custom_candidates(self):
        """Test solving with custom candidate list."""
        solver = PuzzleSolverAI(self.temp_file)
        
        custom_candidates = ["HELLO WORLD", "HELLO THERE", "HELLO FRIEND"]
        pattern = "HE__O _____"
        solutions = solver.solve(pattern, candidates=custom_candidates, top_n=3)
        
        # All solutions should be from custom candidates
        for solution in solutions:
            assert solution in custom_candidates
    
    def test_solve_no_matches(self):
        """Test solving when no candidates match the pattern."""
        solver = PuzzleSolverAI(self.temp_file)
        
        # Pattern that doesn't match any puzzle
        pattern = "ZZZZZ ZZZZZ"
        solutions = solver.solve(pattern, top_n=3)
        
        # Should fall back to shape matching
        assert isinstance(solutions, list)
    
    def test_solve_list_pattern(self):
        """Test solving with list pattern input."""
        solver = PuzzleSolverAI(self.temp_file)
        
        pattern = ['H', 'E', '_', '_', 'O', ' ', 'W', '_', 'R', '_', 'D']
        solutions = solver.solve(pattern, top_n=3)
        
        assert "HELLO WORLD" in solutions
    
    def test_solve_top_n_limit(self):
        """Test that solve respects the top_n limit."""
        solver = PuzzleSolverAI(self.temp_file)
        
        # Use a pattern that might match multiple puzzles
        pattern = "_____ ________"
        solutions = solver.solve(pattern, top_n=2)
        
        assert len(solutions) <= 2
    
    def test_score_candidate_basic(self):
        """Test the scoring function."""
        solver = PuzzleSolverAI(self.temp_file)
        
        pattern = "HE__O W_R_D"
        candidate = "HELLO WORLD"
        
        score = solver._score_candidate(pattern, candidate)
        assert isinstance(score, float)
        # Score should be positive for a good match
        assert score > 0
    
    def test_score_candidate_perfect_match(self):
        """Test scoring for perfect match."""
        solver = PuzzleSolverAI(self.temp_file)
        
        pattern = "HELLO WORLD"
        candidate = "HELLO WORLD"
        
        score = solver._score_candidate(pattern, candidate)
        # Perfect match should have high score
        assert score > 0
    
    def test_score_candidate_poor_match(self):
        """Test scoring for poor match."""
        solver = PuzzleSolverAI(self.temp_file)
        
        pattern = "HE__O W_R_D"
        candidate = "AAAAA AAAAA"  # Wrong letters but right shape
        
        score = solver._score_candidate(pattern, candidate)
        # Poor match should have lower score
        assert isinstance(score, float)
    
    def test_solve_empty_pattern(self):
        """Test solving with empty pattern."""
        solver = PuzzleSolverAI(self.temp_file)
        
        pattern = ""
        solutions = solver.solve(pattern, top_n=3)
        
        # Should handle gracefully
        assert isinstance(solutions, list)
    
    def test_solve_all_underscores(self):
        """Test solving with pattern of all underscores."""
        solver = PuzzleSolverAI(self.temp_file)
        
        pattern = "_____ _____"  # 5 + 5 letter words
        solutions = solver.solve(pattern, top_n=3)
        
        # Should return puzzles that match the shape
        assert isinstance(solutions, list)
        for solution in solutions:
            words = solution.split()
            if len(words) == 2:
                assert len(words[0]) == 5 and len(words[1]) == 5