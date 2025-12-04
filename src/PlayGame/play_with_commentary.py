#!/usr/bin/env python3
"""
Enhanced Wheel of Fortune Game with Interactive Host Commentary
Integrates Pat Sajak commentary and player personalities into the game
"""

import random
import re
import sys
import time
import ascii_wheel
from smart_player import computer_turn_smart, computer_turn_smart_conservative, computer_turn_smart_aggressive
from interactive_host import InteractiveHost

# Global interactive host instance
interactive_host = InteractiveHost()

def computer_turn(showing, winnings, previous_guesses, turn):
    """Basic computer turn with commentary integration"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dollar = 0
    for character in alphabet:
        if character in previous_guesses:
            continue
        if is_vowel(character):
            if winnings[(turn % 3)] < 250:
                continue
            else:
                interactive_host.log_game_action('buy_vowel', turn % 3, f'letter: {character}, cost: $250')
                print("Computer bought:", character)
                winnings[(turn % 3)] = winnings[(turn % 3)] - 250
                break
        # Want to choose a consonant ... so spins wheel
        interactive_host.log_game_action('spin', turn % 3, f'spun wheel')
        dollar = spin_wheel()
        if dollar == 0:
            interactive_host.log_game_action('lose_turn', turn % 3, f'landed on Lose a Turn')
            print("Computer lost a turn")
            character = "_"
            break
        elif dollar == -1:
            interactive_host.log_game_action('bankrupt', turn % 3, f'landed on BANKRUPT')
            print("Computer went bankrupt")
            winnings[(turn % 3)] = 0
            character = "_"
            break
        else:
            interactive_host.log_game_action('guess_consonant', turn % 3, f'letter: {character}, value: ${dollar}')
            print("Computer guessed:", character)
            break
    return character, dollar

def computer_turn_morse(showing, winnings, previous_guesses, turn):
    """Morse code strategy with commentary integration"""
    alphabet = "ETAINOSHRDLUCMFWYGPBVKQJXZ"
    dollar = 0
    for character in alphabet:
        if character in previous_guesses:
            continue
        if is_vowel(character):
            if winnings[(turn % 3)] < 250:
                continue
            else:
                interactive_host.log_game_action('buy_vowel', turn % 3, f'letter: {character}, cost: $250')
                print("Computer bought:", character)
                winnings[(turn % 3)] = winnings[(turn % 3)] - 250
                break
        # Want to choose a consonant ... so spins wheel
        interactive_host.log_game_action('spin', turn % 3, f'spun wheel')
        dollar = spin_wheel()
        if dollar == 0:
            interactive_host.log_game_action('lose_turn', turn % 3, f'landed on Lose a Turn')
            print("Computer lost a turn")
            character = "_"
            break
        elif dollar == -1:
            interactive_host.log_game_action('bankrupt', turn % 3, f'landed on BANKRUPT')
            print("Computer went bankrupt")
            winnings[(turn % 3)] = 0
            character = "_"
            break
        else:
            interactive_host.log_game_action('guess_consonant', turn % 3, f'letter: {character}, value: ${dollar}')
            print("Computer guessed:", character)
            break
    return character, dollar

def computer_turn_oxford(showing, winnings, previous_guesses, turn):
    """Oxford dictionary strategy with commentary integration"""
    alphabet = "EARIOTNSLCUDPMHGBFYWKVXZJQ"
    dollar = 0
    for character in alphabet:
        if character in previous_guesses:
            continue
        if is_vowel(character):
            if winnings[(turn % 3)] < 250:
                continue
            else:
                interactive_host.log_game_action('buy_vowel', turn % 3, f'letter: {character}, cost: $250')
                print("Computer bought:", character)
                winnings[(turn % 3)] = winnings[(turn % 3)] - 250
                break
        # Want to choose a consonant ... so spins wheel
        interactive_host.log_game_action('spin', turn % 3, f'spun wheel')
        dollar = spin_wheel()
        if dollar == 0:
            interactive_host.log_game_action('lose_turn', turn % 3, f'landed on Lose a Turn')
            print("Computer lost a turn")
            character = "_"
            break
        elif dollar == -1:
            interactive_host.log_game_action('bankrupt', turn % 3, f'landed on BANKRUPT')
            print("Computer went bankrupt")
            winnings[(turn % 3)] = 0
            character = "_"
            break
        else:
            interactive_host.log_game_action('guess_consonant', turn % 3, f'letter: {character}, value: ${dollar}')
            print("Computer guessed:", character)
            break
    return character, dollar

def computer_turn_trigrams_bigrams(showing, winnings, previous_guesses, turn):
    """Trigrams/bigrams strategy with commentary integration"""
    allow_vowels = False
    if winnings[(turn % 3)] >= 250:
        allow_vowels = True

    candidate_trigrams = [] 
    showing_words = showing.split(' ')
    for word in showing_words:
        index = 0
        while index < (len(word) - 2):
            trigram = word[index:index+3]
            if trigram[2] == "_" and "_" != trigram[0] and "_" != trigram[1]:
                candidate_trigrams.append(trigram)
            index = index + 1

    candidate_bigrams = [] 
    for word in showing_words:
        index = 0
        while index < (len(word) - 1):
            bigram = word[index:index+2]
            if "_" != bigram[0] and bigram[1] == "_":
                candidate_bigrams.append(bigram)
            index = index + 1

    dollar = 0
    guess = "_"

    # Trigrams processing
    trigrams = ["THE", "AND", "THA", "ENT", "ING", "ION", "TIO", "FOR", "NDE", "HAS", "NCE", "EDT", "TIS", "OFT", "STH", "MEN"]
    for trigram in trigrams:
        to_match = trigram[0:2] + "_"
        if to_match in candidate_trigrams:
            candidate = trigram[2]
            if is_vowel(candidate) and allow_vowels == False:
                continue
            elif candidate in previous_guesses:
                continue
            else:
                guess = candidate
                break
    
    if guess != "_":
        if is_vowel(guess):
            interactive_host.log_game_action('buy_vowel', turn % 3, f'letter: {guess}, cost: $250')
            print("Computer bought:", guess)
            winnings[(turn % 3)] = winnings[(turn % 3)] - 250
            return guess, dollar
        else:
            interactive_host.log_game_action('spin', turn % 3, f'spun wheel')
            dollar = spin_wheel()
            if dollar == 0:
                interactive_host.log_game_action('lose_turn', turn % 3, f'landed on Lose a Turn')
                print("Computer lost a turn")
                guess = "_"
            elif dollar == -1:
                interactive_host.log_game_action('bankrupt', turn % 3, f'landed on BANKRUPT')
                print("Computer went bankrupt")
                winnings[(turn % 3)] = 0
                guess = "_"
            else:
                interactive_host.log_game_action('guess_consonant', turn % 3, f'letter: {guess}, value: ${dollar}')
                print("Computer guessed:", guess)
            return guess, dollar

    # Bigrams processing
    bigrams = []
    with open("bigrams.txt") as g:
        for line in g:
            line = line.rstrip('\n')
            bigram = line.split(' ')[0].upper()
            bigrams.append(bigram)
            if len(bigrams) == 128:
                break
    
    for bigram in bigrams:
        to_match = bigram[0] + "_"
        if to_match in candidate_bigrams:
            candidate = bigram[1]
            if is_vowel(candidate) and allow_vowels == False:
                continue
            elif candidate in previous_guesses:
                continue
            else:
                guess = candidate
                break
    
    if guess != "_":
        if is_vowel(guess):
            interactive_host.log_game_action('buy_vowel', turn % 3, f'letter: {guess}, cost: $250')
            print("Computer bought:", guess)
            winnings[(turn % 3)] = winnings[(turn % 3)] - 250
            return guess, dollar
        else:
            interactive_host.log_game_action('spin', turn % 3, f'spun wheel')
            dollar = spin_wheel()
            if dollar == 0:
                interactive_host.log_game_action('lose_turn', turn % 3, f'landed on Lose a Turn')
                print("Computer lost a turn")
                guess = "_"
            elif dollar == -1:
                interactive_host.log_game_action('bankrupt', turn % 3, f'landed on BANKRUPT')
                print("Computer went bankrupt")
                winnings[(turn % 3)] = 0
                guess = "_"
            else:
                interactive_host.log_game_action('guess_consonant', turn % 3, f'letter: {guess}, value: ${dollar}')
                print("Computer guessed:", guess)
            return guess, dollar

    # Fallback to unigrams
    alphabet = "EARIOTNSLCUDPMHGBFYWKVXZJQ"
    for character in alphabet:
        if character in previous_guesses:
            continue
        if is_vowel(character):
            if winnings[(turn % 3)] < 250:
                continue
            else:
                interactive_host.log_game_action('buy_vowel', turn % 3, f'letter: {character}, cost: $250')
                print("Computer bought:", character)
                winnings[(turn % 3)] = winnings[(turn % 3)] - 250
                break
        # Want to choose a consonant ... so spins wheel
        interactive_host.log_game_action('spin', turn % 3, f'spun wheel')
        dollar = spin_wheel()
        if dollar == 0:
            interactive_host.log_game_action('lose_turn', turn % 3, f'landed on Lose a Turn')
            print("Computer lost a turn")
            character = "_"
            break
        elif dollar == -1:
            interactive_host.log_game_action('bankrupt', turn % 3, f'landed on BANKRUPT')
            print("Computer went bankrupt")
            winnings[(turn % 3)] = 0
            character = "_"
            break
        else:
            interactive_host.log_game_action('guess_consonant', turn % 3, f'letter: {character}, value: ${dollar}')
            print("Computer guessed:", character)
            break
    return character, dollar

def get_random_puzzle():
    """Get a random puzzle from the database"""
    random_int = random.randint(0,900)
    number = 0
    with open("../../data/puzzles/valid.csv") as f:
        for line in f:
            line = line.rstrip('\n')
            puzzle, clue, date, game_type = line.split(',')
            if number == random_int:
                clue = clue.replace("&amp;", "&")
                puzzle = puzzle.replace("&amp;", "&")
                return(puzzle, clue, date, game_type)
            number = number + 1

def human_turn(showing, winnings, previous_guesses, turn, puzzle):
    """Human turn with commentary integration"""
    # Make sure human chooses a valid action
    deciding = False
    while not deciding:
        decision = input("1: Spin, 2: Buy Vowel, 3: Solve ....  ")
        if decision == "1" or decision == "2" or decision == "3":
            deciding = True
            if decision == "2" and winnings[(turn % 3)] < 250:
                print("Sorry .... you don't have enough money. Select 1 or 3")
                deciding = False
        else:
            print("Please choose 1, 2, or 3")

    # Player decisions
    if decision == "3":
        solve = input("Your guess to solve: ...... ").upper()
        interactive_host.log_game_action('solve_attempt', turn % 3, f'attempted solve: {solve}')
        if solve == puzzle:
            print("YOU WIN!")
            print("Player", turn % 3, "won!")
            print("Winnings:", winnings)
            interactive_host.generate_victory_speech(turn % 3, winnings[turn % 3])
            exit()
        else:
            print("Wrong ... next player")
            guess = "_"
            dollar = 0
    elif decision == "2":
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        is_one_vowel = False
        while is_one_vowel != True:
            vowel = input("Guess a vowel: ").upper()
            if len(vowel) != 1:
                print("Guess only one letter")
            else:
                is_one_vowel = is_vowel(vowel)
            if not is_one_vowel:
                print("Not a vowel")
        interactive_host.log_game_action('buy_vowel', turn % 3, f'letter: {vowel}, cost: $250')
        guess = vowel
        dollar = 0
    elif decision == "1":
        # Spin wheel
        interactive_host.log_game_action('spin', turn % 3, f'spun wheel')
        dollar = spin_wheel()
        guess = ""
        if dollar == 0:
            interactive_host.log_game_action('lose_turn', turn % 3, f'landed on Lose a Turn')
            print("Sorry! Lose a turn. Next player")
            guess = "_"
        elif dollar == -1:
            interactive_host.log_game_action('bankrupt', turn % 3, f'landed on BANKRUPT')
            print("Oh No! Bankrupt!")
            winnings[(turn % 3)] = 0
            guess = "_"
        
        is_one_consonant = False
        if guess == "_":
            is_one_consonant = True  # Hacky way
        while is_one_consonant != True:
            guess = input("Name a consonant .... ").upper()
            if len(guess) != 1: 
                print("Guess only one letter")
            else:
                is_one_consonant = is_consonant(guess)
            if not is_one_consonant:
                print("Not a consonant")
        
        if guess != "_":
            interactive_host.log_game_action('guess_consonant', turn % 3, f'letter: {guess}, value: ${dollar}')
    
    return guess, dollar

def is_consonant(guess):
    """Check if guess is a consonant"""
    consonants = "BCDFGHJKLMNPQRSTVWXYZ"
    if guess in consonants:
        return True
    else:
        return False

def is_vowel(guess):
    """Check if guess is a vowel"""
    vowels = "AEIOU"
    if guess in vowels:
        return True
    else:
        return False

def print_board(showing):
    """Print the game board"""
    words = showing.split(" ")
    to_print = ""
    for word in words:
        for character in word:
            to_print = to_print + character + " "
        to_print = to_print + "\n"
    print(to_print)

def spin_wheel():
    """Spin the wheel and return the value"""
    wheel_values = [0,-1,500,550,600,650,700,750,800,850,900,-1,500,550,600,650,700,750,800,850,900,500,550,600]
    print("Wheel is spinning ....")
    print("It landed on ....")
    time.sleep(2)
    ascii_wheel.draw_ascii_wheel(wheel_values, radius=18, label_style="long")
    dollar = random.choice(wheel_values)
    print("....", dollar, "dollars")
    return dollar

def play_random_game(type_of_players, enable_commentary=True):
    """Play a random game with optional commentary"""
    
    # Enable interactive host mode if requested
    if enable_commentary:
        interactive_host.enable_interactive_mode()
    
    # Play the game
    puzzle, clue, date, game_type = get_random_puzzle()
    print("Welcome to Wheel of Fortune")
    print("You are playing a game of type:", game_type)
    print("The clue is:", clue)

    # Mask out word
    showing = puzzle
    showing = re.sub(r"[A-Z]","_",showing)
    print_board(showing)

    # Play the game
    guess = ""
    previous_guesses = []
    turn = 0

    winnings = [0,0,0]
    dollar = 0
    is_solved = False

    while showing != puzzle:
        time.sleep(2)
        print("It is player", turn % 3, "'s turn")

        # Type of player
        type_of_player = type_of_players[turn % 3]
        print("This player is:", type_of_player)

        if type_of_player == "human":
            guess, dollar = human_turn(showing, winnings, previous_guesses, turn, puzzle)
        elif type_of_player == "morse":
            guess, dollar = computer_turn_morse(showing, winnings, previous_guesses, turn)
        elif type_of_player == "oxford":
            guess, dollar = computer_turn_oxford(showing, winnings, previous_guesses, turn)
        elif type_of_player == "trigram":
            guess, dollar = computer_turn_trigrams_bigrams(showing, winnings, previous_guesses, turn)
        elif type_of_player == "smart":
            guess, dollar = computer_turn_smart(showing, winnings, previous_guesses, turn)
        elif type_of_player == "conservative":
            guess, dollar = computer_turn_smart_conservative(showing, winnings, previous_guesses, turn)
        elif type_of_player == "aggressive":
            guess, dollar = computer_turn_smart_aggressive(showing, winnings, previous_guesses, turn)

        # Double check that guess has not already been said
        if guess in previous_guesses and guess != "_":
            print("Sorry, that's already been guessed .... next player")
            turn = turn + 1
        else:
            # Update board
            previous_guesses.append(guess)
            correct_places = []
            for pos,char in enumerate(puzzle):
                if(char == guess):
                    correct_places.append(pos)
            
            if guess == "_":  # Hacky way to say the comp got it wrong or bankrupt, etc.
                turn = turn + 1
            elif len(correct_places) < 1:
                if enable_commentary:
                    interactive_host.log_game_action('wrong_guess', turn % 3, f'letter: {guess}, count: 0')
                print("Sorry, not in the puzzle ... next player")
                turn = turn + 1
            else:
                if enable_commentary:
                    interactive_host.log_game_action('correct_guess', turn % 3, f'letter: {guess}, count: {len(correct_places)}')
        
        winnings[(turn % 3)] = winnings[(turn % 3)] + (dollar * len(correct_places))
        for correct_letter in correct_places:
            showing = showing[:correct_letter] + guess + showing[correct_letter + 1:]
        print("Winnings:", winnings)
        print("Previous guesses:", previous_guesses)
        print("The clue is:", clue)
        print_board(showing)

    while not is_solved:
        print("Player", turn % 3, "has a chance to solve")
        type_of_player = type_of_players[turn % 3]
        # If human, let them guess, otherwise let computer guess
        if type_of_player == "human":
            solve = input("Your guess to solve: ...... ").upper()
        else:
            solve = showing
      
        if solve == puzzle:
            print("Player", turn % 3, "won!")
            print("Winnings:", winnings)
            if enable_commentary:
                interactive_host.generate_victory_speech(turn % 3, winnings[turn % 3])
            is_solved = True
        else:
            print("Wrong ... next player")
            turn = turn + 1
            print("The clue is:", clue)
            print_board(showing)

if __name__ == '__main__':
    # Parse command line arguments
    args = sys.argv[1:]
    
    # Check for commentary flag
    enable_commentary = True
    if "--no-commentary" in args:
        enable_commentary = False
        args.remove("--no-commentary")
    elif "--commentary" in args:
        enable_commentary = True
        args.remove("--commentary")
    
    type_of_players = args
    print(type_of_players)
    
    if len(type_of_players) != 3:
        print("There should be 3 players ... creating a default game with smart AI players")
        print("Available player types: human, morse, oxford, trigram, smart, conservative, aggressive")
        print("Use --commentary or --no-commentary to control interactive host mode")
        type_of_players = ["human", "smart", "conservative"]
        time.sleep(3)

    print(f"\n🎮 Interactive Host Mode: {'ENABLED' if enable_commentary else 'DISABLED'}")
    if enable_commentary:
        print("🎪 Get ready for Pat Sajak commentary and player personalities!")
    print()
    
    play_random_game(type_of_players, enable_commentary)