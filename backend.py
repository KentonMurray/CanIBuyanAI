#!/usr/bin/env python3
"""
Wheel of Fortune Backend Server
Serves puzzle data and handles AI player logic
"""

import csv
import json
import random
import re
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load puzzle data
def load_puzzles():
    puzzles = []
    puzzle_file = os.path.join('data', 'puzzles', 'valid.csv')
    
    if not os.path.exists(puzzle_file):
        # Fallback puzzles if CSV doesn't exist
        return [
            {"phrase": "WHEEL OF FORTUNE", "category": "TV SHOW"},
            {"phrase": "GOOD LUCK", "category": "PHRASE"},
            {"phrase": "HAPPY BIRTHDAY", "category": "EVENT"}
        ]
    
    try:
        with open(puzzle_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    phrase = row[0].strip().upper()
                    category = row[1].strip().upper()
                    # Only include puzzles with letters (no numbers/symbols)
                    if re.match(r'^[A-Z\s&\'-]+$', phrase) and len(phrase) <= 50:
                        puzzles.append({
                            "phrase": phrase,
                            "category": category
                        })
    except Exception as e:
        print(f"Error loading puzzles: {e}")
        # Return fallback puzzles
        return [
            {"phrase": "WHEEL OF FORTUNE", "category": "TV SHOW"},
            {"phrase": "GOOD LUCK", "category": "PHRASE"},
            {"phrase": "HAPPY BIRTHDAY", "category": "EVENT"}
        ]
    
    return puzzles[:500]  # Limit to first 500 puzzles for performance

# Global puzzle data
PUZZLES = load_puzzles()

# AI Player Strategies
class AIPlayer:
    def __init__(self, strategy='morse'):
        self.strategy = strategy
        self.alphabet_orders = {
            'morse': "ETAINOSHRDLUCMFWYGPBVKQJXZ",  # Morse code frequency
            'oxford': "ETAOINSHRDLCUMWFGYPBVKJXQZ",  # Oxford English frequency
            'alphabetical': "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        }
    
    def get_next_guess(self, revealed_letters, used_letters, current_money, puzzle_category):
        """Get the next letter guess from AI player"""
        alphabet = self.alphabet_orders.get(self.strategy, self.alphabet_orders['morse'])
        vowels = "AEIOU"
        
        for letter in alphabet:
            if letter in used_letters:
                continue
                
            if letter in vowels:
                # Buy vowel if we have enough money
                if current_money >= 250:
                    return {'action': 'buy_vowel', 'letter': letter}
            else:
                # Guess consonant (requires spinning first)
                return {'action': 'guess_consonant', 'letter': letter}
        
        # If no letters left, try to solve
        return {'action': 'solve', 'solution': self._attempt_solve(revealed_letters, puzzle_category)}
    
    def _attempt_solve(self, revealed_letters, category):
        """Attempt to solve the puzzle based on revealed letters"""
        # Simple pattern matching - in a real implementation, this would be more sophisticated
        pattern = ''.join(revealed_letters).replace('_', '.')
        
        # For now, return a placeholder - this would need more advanced logic
        return "PLACEHOLDER SOLUTION"

# Routes
@app.route('/')
def index():
    return send_from_directory('.', 'wheel-of-fortune.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/puzzles/random')
def get_random_puzzle():
    """Get a random puzzle"""
    puzzle = random.choice(PUZZLES)
    return jsonify(puzzle)

@app.route('/api/puzzles/count')
def get_puzzle_count():
    """Get total number of available puzzles"""
    return jsonify({'count': len(PUZZLES)})

@app.route('/api/ai/move', methods=['POST'])
def get_ai_move():
    """Get AI player's next move"""
    data = request.json
    
    strategy = data.get('strategy', 'morse')
    revealed_letters = data.get('revealed_letters', [])
    used_letters = data.get('used_letters', [])
    current_money = data.get('current_money', 0)
    puzzle_category = data.get('puzzle_category', '')
    
    ai_player = AIPlayer(strategy)
    move = ai_player.get_next_guess(revealed_letters, used_letters, current_money, puzzle_category)
    
    return jsonify(move)

@app.route('/api/wheel/spin')
def spin_wheel():
    """Simulate wheel spin"""
    # Wheel values matching original game (24 sections)
    # 0 = LOSE TURN, -1 = BANKRUPT
    wheel_values = [0, -1, 500, 550, 600, 650, 700, 750, 800, 850, 900, -1, 
                   500, 550, 600, 650, 700, 750, 800, 850, 900, 500, 550, 600]
    
    result = random.choice(wheel_values)
    
    if result == 0:
        return jsonify({'type': 'lose_turn', 'value': 0, 'message': 'Lose a Turn!'})
    elif result == -1:
        return jsonify({'type': 'bankrupt', 'value': 0, 'message': 'Bankrupt!'})
    else:
        return jsonify({'type': 'money', 'value': result, 'message': f'${result}'})

if __name__ == '__main__':
    print(f"Loaded {len(PUZZLES)} puzzles from CSV data")
    print("Starting Wheel of Fortune backend server...")
    app.run(host='0.0.0.0', port=8083, debug=True)