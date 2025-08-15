import random
import re
import sys
import time
import ascii_wheel

def computer_turn(showing, winnings, previous_guesses, turn):
  # Guess in the order of the alphabet
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  dollar = 0
  for character in alphabet:
    if character in previous_guesses:
      continue
    if is_vowel(character):
      if winnings[(turn % 3)] < 250:
        continue
      else:
        print("Computer bought:", character)
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        break
    # Want to choose a consonant ... so spins wheel
    dollar = spin_wheel()
    if dollar == 0:
      print("Computer lost a turn")
      character = "_"
      break
    elif dollar == -1:
      print("Computer went backrupt")
      winnings[(turn % 3)] = 0
      character = "_"
      break
    else:
      print("Computer guessed:", character)
      break
  return character, dollar

def computer_turn_morse(showing, winnings, previous_guesses, turn):
  # Guess in the order that Samuel Morse identified for his code
  alphabet = "ETAINOSHRDLUCMFWYGPBVKQJXZ"
  dollar = 0
  for character in alphabet:
    if character in previous_guesses:
      continue
    if is_vowel(character):
      if winnings[(turn % 3)] < 250:
        continue
      else:
        print("Computer bought:", character)
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        break
    # Want to choose a consonant ... so spins wheel
    dollar = spin_wheel()
    if dollar == 0:
      print("Computer lost a turn")
      character = "_"
      break
    elif dollar == -1:
      print("Computer went backrupt")
      winnings[(turn % 3)] = 0
      character = "_"
      break
    else:
      print("Computer guessed:", character)
      break
  return character, dollar

def computer_turn_oxford(showing, winnings, previous_guesses, turn):
  # From dictionary ... that's game optimized word not occurance of words
  # Concise Oxford Dictionary (9th edition, 1995) 
  # https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html

  alphabet = "EARIOTNSLCUDPMHGBFYWKVXZJQ"
  dollar = 0
  for character in alphabet:
    if character in previous_guesses:
      continue
    if is_vowel(character):
      if winnings[(turn % 3)] < 250:
        continue
      else:
        print("Computer bought:", character)
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        break
    # Want to choose a consonant ... so spins wheel
    dollar = spin_wheel()
    if dollar == 0:
      print("Computer lost a turn")
      character = "_"
      break
    elif dollar == -1:
      print("Computer went backrupt")
      winnings[(turn % 3)] = 0
      character = "_"
      break
    else:
      print("Computer guessed:", character)
      break
  return character, dollar

def computer_turn_trigrams_bigrams(showing, winnings, previous_guesses, turn):

  allow_vowels = False
  if winnings[(turn % 3)] >= 250:
    allow_vowels = True

  candidate_trigrams = [] 
  showing_words = showing.split(' ')
  for word in showing_words:
    index = 0
    while index < (len(word) - 2):
      trigram = word[index:index+3]
      #print(trigram)
      if trigram[2] == "_" and "_" != trigram[0] and "_" != trigram[1]:
        candidate_trigrams.append(trigram)
      index = index + 1

  candidate_bigrams = [] 
  for word in showing_words:
    index = 0
    while index < (len(word) - 1):
      bigram = word[index:index+2]
      #print(bigram)
      if "_" != bigram[0] and bigram[1] == "_":
        candidate_bigrams.append(bigram)
      index = index + 1

  #print(candidate_trigrams)
  #print(candidate_bigrams)

  dollar = 0
  guess = "_"

  # Frewquencies from: http://mathcenter.oxford.emory.edu/site/math125/englishLetterFreqs/#:~:text=Most%20common%20bigrams%20(in%20order,%2C%20sa%2C%20em%2C%20ro.

  #Most common trigrams (in order)
  trigrams = ["THE", "AND", "THA", "ENT", "ING", "ION", "TIO", "FOR", "NDE", "HAS", "NCE", "EDT", "TIS", "OFT", "STH", "MEN"]
  for trigram in trigrams:
    to_match = trigram[0:2] + "_"
    #print("TOMatch", to_match)
    if to_match in candidate_trigrams:
      candidate = trigram[2]
      #print("CANDIDATE", candidate)
      if is_vowel(candidate) and allow_vowels == False:
        #print("can't vowel")
        continue
      elif candidate in previous_guesses:
        #print("already guessed")
        continue
      else:
        guess = candidate
        #print("Actual CANDIDATE", candidate)
        break
  if guess != "_":
    if is_vowel(guess):
      print("Computer bought:", guess)
      winnings[(turn % 3)] = winnings[(turn % 3)] - 250
      return guess, dollar # Should be a vowel and 0 since we've already subtraced
    else:
      dollar = spin_wheel()
      if dollar == 0:
        print("Computer lost a turn")
        guess = "_"
      elif dollar == -1:
        print("Computer went backrupt")
        winnings[(turn % 3)] = 0
        guess = "_"
      else:
        print("Computer guessed:", guess)
      return guess, dollar

  #print("No trigrams ... backing off to bigrams")

  #Most common bigrams (in order)
  #frequent bigrams from a file ... http://practicalcryptography.com/media/cryptanalysis/files/english_bigrams_1.txt Only want first 128
  #bigrams = ["TH", "HE", "IN", "EN", "NT", "RE", "ER", "AN", "TI", "ES", "ON", "AT", "SE", "ND", "OR", "AR", "AL", "TE", "CO", "DE", "TO", "RA", "ET", "ED", "IT", "SA", "EM", "RO"]
  bigrams = []
  with open("bigrams.txt") as g:
    for line in g:
      line = line.rstrip('\n')
      bigram = line.split(' ')[0].upper()
      bigrams.append(bigram)
      if len(bigrams) == 128:
        break # Arbitrary threshold to use
  #print(bigrams)
  for bigram in bigrams:
    to_match = bigram[0] + "_"
    #print(to_match)
    if to_match in candidate_bigrams:
      candidate = bigram[1]
      #print("CANDIDATE", candidate)
      if is_vowel(candidate) and allow_vowels == False:
        #print("can't vowel")
        continue
      elif candidate in previous_guesses:
        #print("already guessed")
        continue
      else:
        guess = candidate
        #print("Actual CANDIDATE", candidate)
        break
  if guess != "_":
    if is_vowel(guess):
      print("Computer bought:", guess)
      winnings[(turn % 3)] = winnings[(turn % 3)] - 250
      return guess, dollar # Should be a vowel and 0 since we've already subtraced
    else:
      dollar = spin_wheel()
      if dollar == 0:
        print("Computer lost a turn")
        guess = "_"
      elif dollar == -1:
        print("Computer went backrupt")
        winnings[(turn % 3)] = 0
        guess = "_"
      else:
        print("Computer guessed:", guess)
      return guess, dollar

  #print("No bigrams ... backing off to unigrams")

  # Unigrams are from the oxford strategy above
  alphabet = "EARIOTNSLCUDPMHGBFYWKVXZJQ"


  for character in alphabet:
    if character in previous_guesses:
      continue
    if is_vowel(character):
      if winnings[(turn % 3)] < 250:
        continue
      else:
        print("Computer bought:", character)
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        break
    # Want to choose a consonant ... so spins wheel
    dollar = spin_wheel()
    if dollar == 0:
      print("Computer lost a turn")
      character = "_"
      break
    elif dollar == -1:
      print("Computer went backrupt")
      winnings[(turn % 3)] = 0
      character = "_"
      break
    else:
      print("Computer guessed:", character)
      break
  return character, dollar

def get_random_puzzle():
  random_int = random.randint(0,900) # Roughly size of num puzzles in valid
  number = 0
  with open("../../data/puzzles/valid.csv") as f:
    for line in f:
      line = line.rstrip('\n')
      puzzle, clue, date, game_type = line.split(',')
      if number == random_int:
        #print(line)
        clue = clue.replace("&amp;", "&") # HTML Code
        puzzle = puzzle.replace("&amp;", "&") # HTML Code
        return(puzzle, clue, date, game_type)
      number = number + 1

def human_turn(showing, winnings, previous_guesses, turn, puzzle):

  # Make sure human chooses a valid action
  deciding = False
  while not deciding:
    decision = input("1: Spin, 2: Buy Vowel, 3: Solve ....  ")
    if decision == "1" or decision == "2" or decision == "3":
      deciding = True
      if decision == "2" and winnings[(turn % 3)] < 250: # Minimum cost of a vowel
        print("Sorry .... you don't have enough money. Select 1 or 3")
        deciding = False
    else:
      print("Please choose 1, 2, or 3")

  # Player decisions
  if decision == "3":
    deciding = True
    solve = input("Your guess to solve: ...... ").upper() # TODO: clean
    if solve == puzzle:
      print("YOU WIN!")
      print("Player", turn % 3, "won!")
      print("Winnings:", winnings)
      is_solved = True
      exit()
      #break #TODO: not just exit here
    else:
      print("Wrong ... next player")
      #turn = turn + 1
      #print("The clue is:", clue)
      #print_board(showing)
      #continue
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
    guess = vowel
    dollar = 0
  elif decision == "1":
    # Spin wheel
    dollar = spin_wheel()
    guess = ""
    if dollar == 0:
      print("Sorry! Lose a turn. Next player")
      #turn = turn + 1
      #continue
      guess = "_"
    elif dollar == -1:
      print("Oh No! Bankrupt!")
      winnings[(turn % 3)] = 0
      #turn = turn + 1
      #continue
      guess = "_"
    is_one_consonant = False
    if guess == "_":
      is_one_consonant = True # Hacky way
    while is_one_consonant != True:
      guess = input("Name a consonant .... ").upper()
      if len(guess) != 1: 
        print("Guess only one letter")
      else:
        is_one_consonant = is_consonant(guess)

      if not is_one_consonant:
        print("Not a consonant")
  return guess, dollar

def is_consonant(guess):
  consonants = "BCDFGHJKLMNPQRSTVWXYZ"
  if guess in consonants:
    return True
  else:
    return False

def is_vowel(guess):
  vowels = "AEIOU"
  if guess in vowels:
    return True
  else:
    return False

def print_board(showing):
  words = showing.split(" ")
  to_print = ""
  for word in words:
    for character in word:
      to_print = to_print + character + " "
    to_print = to_print + "\n"
  print(to_print)

def spin_wheel():
  wheel_values = [0,-1,500,550,600,650,700,750,800,850,900,-1,500,550,600,650,700,750,800,850,900,500,550,600]
  # Note that the wheel changes over time ... free play now an 850. Different rounds, etc.
  print("Wheel is spinning ....")
  print("It landed on ....")
  time.sleep(2) # Drama!
  ascii_wheel.draw_ascii_wheel(wheel_values, radius=18, label_style="long")
  dollar = random.choice(wheel_values)
  print("....", dollar, "dollars")
  return dollar


def play_random_game(type_of_players):

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
    time.sleep(2) # Let humans see what is going on
    # Ends wierd if last letter is guessed and not solved.# TODO
    print("It is player", turn % 3, "'s turn")

    # Type of player
    type_of_player = type_of_players[turn % 3]
    print("This player is:", type_of_player)

    if type_of_player == "human":
      guess, dollar = human_turn(showing, winnings, previous_guesses, turn, puzzle)
    elif type_of_player == "morse":
      guess, dollar = computer_turn_oxford(showing, winnings, previous_guesses, turn)
    elif type_of_player == "oxford":
      guess, dollar = computer_turn_oxford(showing, winnings, previous_guesses, turn)
    elif type_of_player == "trigram":
      guess, dollar = computer_turn_trigrams_bigrams(showing, winnings, previous_guesses, turn)

    ## Human playing
    #if turn % 3 == 0:
    #  guess, dollar = human_turn(showing, winnings, previous_guesses, turn, puzzle)
    #
    ## Computer playing
    #elif turn % 3 == 1:
    #  guess, dollar = computer_turn_oxford(showing, winnings, previous_guesses, turn)
    #elif turn % 3 == 2:
    #  guess, dollar = computer_turn_morse(showing, winnings, previous_guesses, turn)


    # Double check that guess has not already been said (I've seen it on TV before)
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
      #print(correct_places)
      if guess == "_": # Hacky way to say the comp got it wrong or bankrupt, etc.
        turn = turn + 1
      elif len(correct_places) < 1:
        print("Sorry, not in the puzzle ... next player")
        turn = turn + 1
    winnings[(turn % 3)] = winnings[(turn % 3)] + (dollar * len(correct_places))
    for correct_letter in correct_places:
      showing = showing[:correct_letter] + guess + showing[correct_letter + 1:]
    print("Winnings:", winnings)
    print("Previous guesses:", previous_guesses)
    print("The clue is:", clue)
    print_board(showing)

  while not is_solved:
    print("Player", turn % 3, "has a chance to solve")
    type_of_player = type_of_players[turn % 3] # wouldn't have hit this above
    # If human, let them guess, otheerwise let computer guess
    if type_of_player == "human":
      solve = input("Your guess to solve: ...... ").upper() # TODO: clean
    else:
      solve = showing
  
    if solve == puzzle:
      print("Player", turn % 3, "won!")
      print("Winnings:", winnings)
      is_solved = True
    else:
      print("Wrong ... next player")
      turn = turn + 1
      print("The clue is:", clue)
      print_board(showing)

if __name__ == '__main__':
  type_of_players = sys.argv[1:]
  print(type_of_players)
  if len(type_of_players) != 3:
    print("There should be 3 players ... creating a default game with one human for you")
    type_of_players = ["human", "morse", "oxford"] # TODO: Set with command line
    time.sleep(3)
  #type_of_players = ["morse", "morse", "oxford"] # TODO: Set with command line

  play_random_game(type_of_players)



# TODO: Somehow when the comp buys E it messes things up ... (first letter for many strategies)
