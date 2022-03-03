import random
import re
import time

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

def get_random_puzzle():
  random_int = random.randint(0,900) # Roughly size of num puzzles in valid
  number = 0
  with open("../../data/puzzles/valid.csv") as f:
    for line in f:
      line = line.rstrip('\n')
      puzzle, clue, date, game_type = line.split(',')
      if number == random_int:
        #print(line)
        return(puzzle, clue, date, game_type)
      number = number + 1

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
  dollar = random.choice(wheel_values)
  print("....", dollar, "dollars")
  return dollar


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

while showing != puzzle:
  # Ends wierd if last letter is guessed and not solved.# TODO
  print("It is player", turn % 3, "'s turn")

  ## Computer playing
  #if turn % 3 == 1:
  #  #showing, winnings, previous_guesses = computer_turn(showing, winnings, previous_guesses, turn)
  #  #turn = turn + 1
  #  #print("Winnings:", winnings)
  #  #print_board(showing)
  #  #continue

  # Player decisions
  if turn % 3 == 0:
    decision = input("1: Spin, 2: Buy Vowel, 3: Solve ....  ")
    if decision == "3":
      solve = input("Your guess to solve: ...... ").upper() # TODO: clean
      if solve == puzzle:
        print("YOU WIN!")
        print("Player", turn % 3, "won!")
        print("Winnings:", winnings)
        exit()
      else:
        print("Wrong ... next player")
        turn = turn + 1
        print("The clue is:", clue)
        print_board(showing)
        continue
    elif decision == "2":
      if winnings[(turn % 3)] < 250: # Minimum cost of a vowel
        print("Sorry .... you don't have enough money. Select 1 or 3")
        continue
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
      if dollar == 0:
        print("Sorry! Lose a turn. Next player")
        turn = turn + 1
        continue
      elif dollar == -1:
        print("Oh No! Bankrupt!")
        winnings[(turn % 3)] = 0
        turn = turn + 1
        continue
      is_one_consonant = False
      while is_one_consonant != True:
        guess = input("Name a consonant .... ").upper()
        if len(guess) != 1: 
          print("Guess only one letter")
        else:
          is_one_consonant = is_consonant(guess)

        if not is_one_consonant:
          print("Not a consonant")
    else:
      print("Please choose 1, 2, or 3")

  # Computer playing
  elif turn % 3 == 1:
    guess, dollar = computer_turn_oxford(showing, winnings, previous_guesses, turn)
  elif turn % 3 == 2:
    guess, dollar = computer_turn_morse(showing, winnings, previous_guesses, turn)


  # Double check that guess has not already been said (I've seen it on TV before)
  if guess in previous_guesses:
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
    if guess == "_": # Hacky way to say the comp got it wrong
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
