import os
import sys
import pytest
from io import StringIO

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from display import Display


class TestDisplay:
    """Test the Display class."""
    
    def test_show_header(self, capsys):
        """Test showing the header."""
        Display.show_header()
        captured = capsys.readouterr()
        
        assert "WHEEL OF FORTUNE" in captured.out
        assert "BONUS ROUND" in captured.out
        assert "=====" in captured.out
    
    def test_show_pattern_basic(self, capsys):
        """Test showing a basic pattern."""
        pattern = ["H", "E", "_", "_", "O"]
        Display.show_pattern(pattern)
        captured = capsys.readouterr()
        
        assert "Puzzle:" in captured.out
        assert "H E _ _ O" in captured.out
    
    def test_show_pattern_with_spaces(self, capsys):
        """Test showing pattern with spaces."""
        pattern = ["H", "E", "_", "_", "O", " ", "W", "_", "R", "_", "D"]
        Display.show_pattern(pattern)
        captured = capsys.readouterr()
        
        assert "Puzzle:" in captured.out
        assert "H E _ _ O   W _ R _ D" in captured.out
    
    def test_show_pattern_empty(self, capsys):
        """Test showing empty pattern."""
        pattern = []
        Display.show_pattern(pattern)
        captured = capsys.readouterr()
        
        assert "Puzzle:" in captured.out
        # Should handle empty pattern gracefully
    
    def test_show_pattern_single_character(self, capsys):
        """Test showing single character pattern."""
        pattern = ["A"]
        Display.show_pattern(pattern)
        captured = capsys.readouterr()
        
        assert "Puzzle:" in captured.out
        assert "A" in captured.out
    
    def test_msg_basic(self, capsys):
        """Test basic message display."""
        message = "Hello, World!"
        Display.msg(message)
        captured = capsys.readouterr()
        
        assert message in captured.out
    
    def test_msg_empty(self, capsys):
        """Test empty message display."""
        message = ""
        Display.msg(message)
        captured = capsys.readouterr()
        
        # Should handle empty message gracefully
        assert captured.out == "\n"
    
    def test_msg_multiline(self, capsys):
        """Test multiline message display."""
        message = "Line 1\nLine 2\nLine 3"
        Display.msg(message)
        captured = capsys.readouterr()
        
        assert "Line 1" in captured.out
        assert "Line 2" in captured.out
        assert "Line 3" in captured.out
    
    def test_msg_special_characters(self, capsys):
        """Test message with special characters."""
        message = "Special chars: !@#$%^&*()"
        Display.msg(message)
        captured = capsys.readouterr()
        
        assert message in captured.out
    
    def test_static_methods(self):
        """Test that all methods are static and can be called without instance."""
        # Should be able to call without creating instance
        Display.show_header()
        Display.show_pattern(["A", "B", "C"])
        Display.msg("Test message")
        
        # No exceptions should be raised