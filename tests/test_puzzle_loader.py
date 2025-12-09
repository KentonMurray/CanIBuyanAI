import os
import sys
import pytest
import tempfile
from pathlib import Path

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from puzzle_loader import PuzzleLoader


class TestPuzzleLoader:
    """Test the PuzzleLoader class."""
    
    def test_init_with_existing_file(self):
        """Test initialization with an existing file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("TEST PUZZLE\nANOTHER PUZZLE\n")
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            assert loader.puzzle_file == Path(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_init_with_nonexistent_file(self):
        """Test initialization with a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Puzzle file not found"):
            PuzzleLoader("nonexistent_file.txt")
    
    def test_load_random_puzzle_basic(self):
        """Test loading a random puzzle from a file with multiple puzzles."""
        puzzles = ["HELLO WORLD", "WHEEL OF FORTUNE", "PYTHON PROGRAMMING"]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write('\n'.join(puzzles))
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            puzzle = loader.load_random_puzzle()
            
            # Should return one of the puzzles in uppercase
            assert puzzle in [p.upper() for p in puzzles]
            assert isinstance(puzzle, str)
        finally:
            os.unlink(temp_file)
    
    def test_load_random_puzzle_single_puzzle(self):
        """Test loading from a file with a single puzzle."""
        puzzle_text = "SINGLE PUZZLE"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(puzzle_text)
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            puzzle = loader.load_random_puzzle()
            
            assert puzzle == puzzle_text.upper()
        finally:
            os.unlink(temp_file)
    
    def test_load_random_puzzle_with_empty_lines(self):
        """Test loading puzzles while ignoring empty lines."""
        content = """
FIRST PUZZLE

SECOND PUZZLE


THIRD PUZZLE

"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            puzzle = loader.load_random_puzzle()
            
            expected_puzzles = ["FIRST PUZZLE", "SECOND PUZZLE", "THIRD PUZZLE"]
            assert puzzle in expected_puzzles
        finally:
            os.unlink(temp_file)
    
    def test_load_random_puzzle_with_whitespace(self):
        """Test loading puzzles with leading/trailing whitespace."""
        content = "  PUZZLE WITH SPACES  \n\t\tTABBED PUZZLE\t\t\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            puzzle = loader.load_random_puzzle()
            
            expected_puzzles = ["PUZZLE WITH SPACES", "TABBED PUZZLE"]
            assert puzzle in expected_puzzles
        finally:
            os.unlink(temp_file)
    
    def test_load_random_puzzle_case_conversion(self):
        """Test that puzzles are converted to uppercase."""
        content = "lowercase puzzle\nMiXeD cAsE pUzZlE\nUPPERCASE PUZZLE"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            puzzle = loader.load_random_puzzle()
            
            expected_puzzles = ["LOWERCASE PUZZLE", "MIXED CASE PUZZLE", "UPPERCASE PUZZLE"]
            assert puzzle in expected_puzzles
            # Ensure it's actually uppercase
            assert puzzle == puzzle.upper()
        finally:
            os.unlink(temp_file)
    
    def test_load_random_puzzle_empty_file(self):
        """Test loading from an empty file raises IndexError."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("")  # Empty file
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            with pytest.raises(IndexError):
                loader.load_random_puzzle()
        finally:
            os.unlink(temp_file)
    
    def test_load_random_puzzle_only_empty_lines(self):
        """Test loading from a file with only empty lines raises IndexError."""
        content = "\n\n   \n\t\t\n\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            with pytest.raises(IndexError):
                loader.load_random_puzzle()
        finally:
            os.unlink(temp_file)
    
    def test_load_random_puzzle_deterministic_with_seed(self):
        """Test that random selection can be made deterministic for testing."""
        import random
        
        puzzles = ["PUZZLE ONE", "PUZZLE TWO", "PUZZLE THREE"]
        content = '\n'.join(puzzles)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            loader = PuzzleLoader(temp_file)
            
            # Set seed for reproducible results
            random.seed(42)
            puzzle1 = loader.load_random_puzzle()
            
            random.seed(42)
            puzzle2 = loader.load_random_puzzle()
            
            # Should get the same puzzle with the same seed
            assert puzzle1 == puzzle2
        finally:
            os.unlink(temp_file)