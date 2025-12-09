import os
import sys
import pytest
import math

# Make src/PlayGame importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'PlayGame'))

from solve_decision import estimate_entropy, estimate_solve_probability, should_solve_now


class TestEstimateEntropy:
    """Test the estimate_entropy function."""
    
    def test_estimate_entropy_fully_revealed(self):
        """Test entropy of fully revealed puzzle."""
        showing = "HELLO WORLD"
        entropy = estimate_entropy(showing)
        assert entropy == 0.0
    
    def test_estimate_entropy_fully_blank(self):
        """Test entropy of completely blank puzzle."""
        showing = "_____"
        entropy = estimate_entropy(showing)
        # Should be maximum entropy (log2(26))
        assert entropy == math.log2(26)
    
    def test_estimate_entropy_partially_revealed(self):
        """Test entropy of partially revealed puzzle."""
        showing = "HE__O"
        entropy = estimate_entropy(showing)
        # Should be between 0 and max entropy
        assert 0 < entropy < math.log2(26)
    
    def test_estimate_entropy_with_spaces(self):
        """Test entropy calculation ignores spaces."""
        showing = "HE_ _O W_RLD"
        entropy = estimate_entropy(showing)
        assert isinstance(entropy, float)
        assert entropy >= 0
    
    def test_estimate_entropy_empty_string(self):
        """Test entropy of empty string."""
        showing = ""
        entropy = estimate_entropy(showing)
        assert entropy == 0.0
    
    def test_estimate_entropy_only_spaces(self):
        """Test entropy of string with only spaces."""
        showing = "   "
        entropy = estimate_entropy(showing)
        assert entropy == 0.0
    
    def test_estimate_entropy_with_category(self):
        """Test entropy calculation with category context."""
        showing = "HE__O"
        entropy = estimate_entropy(showing, category="PHRASE")
        assert isinstance(entropy, float)
        assert entropy >= 0


class TestEstimateSolveProbability:
    """Test the estimate_solve_probability function."""
    
    def test_estimate_solve_probability_high_confidence(self):
        """Test solve probability with high confidence scenario."""
        showing = "HELLO WOR_D"  # Only one letter missing
        prob = estimate_solve_probability(showing)
        # Should be high probability
        assert 0.7 <= prob <= 1.0
    
    def test_estimate_solve_probability_low_confidence(self):
        """Test solve probability with low confidence scenario."""
        showing = "_____ _____"  # Many letters missing
        prob = estimate_solve_probability(showing)
        # Should be low probability
        assert 0.0 <= prob <= 0.3
    
    def test_estimate_solve_probability_medium_confidence(self):
        """Test solve probability with medium confidence scenario."""
        showing = "HE__O W_R_D"  # Some letters missing
        prob = estimate_solve_probability(showing)
        # Should be medium probability
        assert 0.2 <= prob <= 0.8
    
    def test_estimate_solve_probability_fully_revealed(self):
        """Test solve probability when fully revealed."""
        showing = "HELLO WORLD"
        prob = estimate_solve_probability(showing)
        # Should be maximum probability
        assert prob == 1.0
    
    def test_estimate_solve_probability_with_category(self):
        """Test solve probability with category context."""
        showing = "HE__O W_R_D"
        prob = estimate_solve_probability(showing, category="PHRASE")
        # Should return a valid probability
        assert 0.0 <= prob <= 1.0


class TestShouldSolveNow:
    """Test the should_solve_now function."""
    
    def test_should_solve_now_high_confidence(self):
        """Test decision with high confidence puzzle."""
        showing = "HELLO WOR_D"
        should_solve = should_solve_now(showing, current_money=1000)
        # Should recommend solving with high confidence
        assert should_solve is True
    
    def test_should_solve_now_low_confidence(self):
        """Test decision with low confidence puzzle."""
        showing = "_____ _____"
        should_solve = should_solve_now(showing, current_money=1000)
        # Should recommend not solving with low confidence
        assert should_solve is False
    
    def test_should_solve_now_high_money(self):
        """Test decision with high money amount."""
        showing = "HE__O W_R_D"
        should_solve = should_solve_now(showing, current_money=50000)
        # High money should encourage solving
        assert isinstance(should_solve, bool)
    
    def test_should_solve_now_low_money(self):
        """Test decision with low money amount."""
        showing = "HE__O W_R_D"
        should_solve = should_solve_now(showing, current_money=100)
        # Low money should be more conservative
        assert isinstance(should_solve, bool)
    
    def test_should_solve_now_with_category(self):
        """Test decision with category context."""
        showing = "HE__O W_R_D"
        should_solve = should_solve_now(showing, current_money=1000, category="PHRASE")
        assert isinstance(should_solve, bool)
    
    def test_should_solve_now_edge_cases(self):
        """Test decision with edge cases."""
        # Empty puzzle
        should_solve_empty = should_solve_now("", current_money=1000)
        assert should_solve_empty is True  # Nothing to lose
        
        # Fully revealed
        should_solve_full = should_solve_now("HELLO WORLD", current_money=1000)
        assert should_solve_full is True  # Guaranteed win