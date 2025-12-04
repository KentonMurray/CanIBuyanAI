#!/usr/bin/env python3
"""
Standalone Wheel of Fortune with Built-in Commentary
Zero external dependencies - uses only Python built-ins
"""

import random
import re
import sys
import time

# Built-in Pat Sajak commentary templates
PAT_COMMENTARY = {
    'wrong_guess': [
        "Sorry, no {letter}s in the puzzle!",
        "Not today, {player}! No {letter}s!",
        "Ooh, tough break! No {letter}s there!",
        "That's not going to help you, {player}!",
        "No {letter}s... better luck next spin!"
    ],
    'correct_guess': [
        "Nice work, {player}! {count} {letter}s!",
        "There you go! {count} {letter}s!",
        "Excellent! {count} {letter}s in the puzzle!",
        "Way to go, {player}! {count} {letter}s!",
        "That's what I'm talking about! {count} {letter}s!"
    ],
    'bankrupt': [
        "Oh no! BANKRUPT! Sorry, {player}!",
        "Ouch! That's a BANKRUPT, {player}!",
        "The wheel can be cruel! BANKRUPT!",
        "Better luck next time, {player}! BANKRUPT!"
    ],
    'lose_turn': [
        "Lose a Turn! Sorry, {player}!",
        "That's a Lose a Turn! Moving on!",
        "Oops! Lose a Turn, {player}!",
        "The wheel says Lose a Turn!"
    ],
    'victory': [
        "Congratulations, {player}! You've won with ${winnings}!",
        "What a fantastic game, {player}! ${winnings} is yours!",
        "Outstanding performance, {player}! You've earned ${winnings}!",
        "Well done, {player}! ${winnings} and the victory!"
    ]
}

# Player personality traits
PERSONALITY_TRAITS = [
    "Confident", "Nervous", "Cheerful", "Analytical", "Impulsive", "Strategic",
    "Optimistic", "Cautious", "Energetic", "Thoughtful", "Bold", "Humble",
    "Witty", "Serious", "Friendly", "Competitive", "Calm", "Excitable",
    "Focused", "Dreamy", "Practical", "Creative", "Logical", "Intuitive",
    "Patient", "Eager", "Methodical", "Spontaneous", "Observant", "Talkative"
]

LOCATIONS = ["New York", "California", "Texas", "Florida", "Illinois", "Ohio", "Michigan", "Georgia"]

class StandaloneHost:
    """Built-in commentary system with zero dependencies"""
    
    def __init__(self):
        self.players = {}
        self.action_count = 0
        
    def setup_players(self, num_players):
        """Generate player personalities"""
        for i in range(num_players):
            traits = random.sample(PERSONALITY_TRAITS, 3)
            location = random.choice(LOCATIONS)
            self.players[i] = {
                'name': f"Player {i+1}",
                'traits': traits,
                'location': location
            }
        
        print("\n🎪 INTERACTIVE HOST MODE ACTIVATED! 🎪")
        print("Pat Sajak and our contestants are ready to entertain!")
        print("\nMeet our contestants:")
        for i, player in self.players.items():
            traits_str = ", ".join(player['traits'])
            print(f"🎭 Amazing {player['name']} from {player['location']}: {traits_str}")
        print()
    
    def commentary(self, action_type, player_num, **kwargs):
        """Generate Pat Sajak commentary"""
        self.action_count += 1
        
        if action_type not in PAT_COMMENTARY:
            return
            
        player_name = self.players.get(player_num, {}).get('name', f'Player {player_num+1}')
        
        template = random.choice(PAT_COMMENTARY[action_type])
        
        # Fill in template variables with safe defaults
        try:
            commentary = template.format(
                player=player_name,
                letter=kwargs.get('letter', 'X'),
                count=kwargs.get('count', 1),
                winnings=kwargs.get('winnings', 0)
            )
        except KeyError:
            # If template has missing parameters, use a safe version
            safe_template = template.replace('{letter}', kwargs.get('letter', 'that letter'))
            safe_template = safe_template.replace('{count}', str(kwargs.get('count', 'some')))
            safe_template = safe_template.replace('{winnings}', str(kwargs.get('winnings', '0')))
            commentary = safe_template.format(player=player_name)
        
        print(f"🎙️ Pat Sajak: {commentary}")
        
        # Every 3rd action, add player commentary
        if self.action_count % 3 == 0:
            self.player_commentary(player_num)
    
    def player_commentary(self, player_num):
        """Generate player commentary"""
        player = self.players.get(player_num, {})
        if not player:
            return
            
        # Simple trait-based commentary
        trait = random.choice(player['traits'])
        
        if trait == "Confident":
            comment = "I've got this! Just need to stay focused!"
        elif trait == "Nervous":
            comment = "Oh gosh, I hope I can figure this out..."
        elif trait == "Cheerful":
            comment = "This is so much fun! I love this game!"
        elif trait == "Strategic":
            comment = "Let me think about the most common letters..."
        elif trait == "Impulsive":
            comment = "I'm just going to go with my gut feeling!"
        else:
            comment = "This puzzle is really challenging!"
        
        print(f"💬 {player['name']}: {comment}")

# Initialize the host
host = StandaloneHost()

def is_vowel(character):
    return character in "AEIOU"

def computer_turn_basic(showing, winnings, previous_guesses, turn):
    """Basic computer turn with commentary"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    for character in alphabet:
        if character in previous_guesses:
            continue
        if is_vowel(character):
            if winnings[turn % 3] < 250:
                continue
            else:
                print("Computer bought:", character)
                return character, "buy"
        else:
            print("Computer guessed:", character)
            return character, "guess"
    
    return None, "pass"

def play_simple_game():
    """Play a simple game with built-in commentary"""
    
    # Sample puzzle
    puzzle = "KITCHEN TIMER"
    clue = "In the Kitchen"
    
    # Initialize game state
    showing = ["_" if c.isalpha() else c for c in puzzle]
    winnings = [0, 0, 0]
    previous_guesses = []
    turn = 0
    
    # Setup players
    host.setup_players(3)
    
    print(f"Welcome to Wheel of Fortune")
    print(f"The clue is: {clue}")
    print(" ".join(showing))
    print()
    
    # Game loop
    while "_" in showing and turn < 20:  # Limit turns to prevent infinite loop
        print(f"It is Player {(turn % 3) + 1}'s turn")
        
        # Simple computer turn
        guess, action_type = computer_turn_basic(showing, winnings, previous_guesses, turn)
        
        if guess is None:
            print("No more letters to guess!")
            break
            
        previous_guesses.append(guess)
        
        # Check if letter is in puzzle
        if guess in puzzle:
            count = puzzle.count(guess)
            # Update showing
            for i, c in enumerate(puzzle):
                if c == guess:
                    showing[i] = c
            
            if action_type == "buy":
                winnings[turn % 3] -= 250
            else:
                winnings[turn % 3] += count * 500  # Simple scoring
            
            host.commentary('correct_guess', turn % 3, letter=guess, count=count)
            
            # Check for win
            if "_" not in showing:
                print(f"\n🎉 PUZZLE SOLVED: {puzzle}")
                host.commentary('victory', turn % 3, winnings=winnings[turn % 3])
                break
        else:
            host.commentary('wrong_guess', turn % 3, letter=guess)
            turn += 1  # Next player's turn
        
        print(f"Winnings: {winnings}")
        print(f"Puzzle: {' '.join(showing)}")
        print()
        
        time.sleep(1)  # Brief pause for readability

def main():
    print("🎮 STANDALONE WHEEL OF FORTUNE 🎮")
    print("Zero dependencies - built-in Pat Sajak commentary!")
    print("=" * 50)
    
    try:
        play_simple_game()
    except KeyboardInterrupt:
        print("\n\nThanks for playing!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()