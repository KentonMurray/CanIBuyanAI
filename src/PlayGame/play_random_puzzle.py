import random
import re
import time

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
  return random.choice(wheel_values)


# Play the game
puzzle, clue, date, game_type = get_random_puzzle()
print("Welcome to Wheel of Fortune")
print("You are playing a game of type:", game_type)
print("The clue is:", clue)

# Mask out word
showing = puzzle
#print(showing)
showing = re.sub(r"[A-Z]","_",showing)
#print(showing)
print_board(showing)

#showing = ""
#for character in puzzle:
#  if character != " ":
#    showing = showing + "_ "
#  else:
#    showing = showing + "\n"
#print(showing)

consonants = "BCDFGHJKLMNPQRSTVWXYZ"
vowels = "AEIOU"

# Play the game
guess = ""
previous_guesses = []
turn = 0

winnings = [0,0,0]

while showing != puzzle:

  print("It is player", turn % 3, "'s turn")

  # Player decisions
  decision = input("1: Spin, 2: Buy Vowel, 3: Solve ....  ")
  if decision == "3":
    solve = input("Your guess to solve: ...... ").upper() # TODO: clean
    if solve == puzzle:
      print("YOU WIN!")
      print("Player", turn % 3, "won!")
      exit()
    else:
      print("Wrong ... next player")
      turn = turn + 1
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
      elif vowel not in vowels:
        print("Not a vowel")
      else:
        is_one_vowel = True
    # Subtract winnings
    guess = vowel
  elif decision == "1":
    print("Wheel is spinning ....")
    print("It landed on ....")
    time.sleep(2) # Drama!
    # Spin wheel
    dollar = spin_wheel()
    print("....", dollar, "dollars")
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
      elif guess not in consonants:
        print("Not a consonant")
      else:
        is_one_consonant = True
  else:
    print("Please choose 1, 2, or 3")

  # Update board
  previous_guesses.append(guess)
  correct_places = []
  for pos,char in enumerate(puzzle):
    if(char == guess):
        correct_places.append(pos)
  #print(correct_places)
  if len(correct_places) < 1:
    print("Sorry, not in the puzzle ... next player")
    turn = turn + 1
  winnings[(turn % 3)] = winnings[(turn % 3)] + (dollar * len(correct_places))
  for correct_letter in correct_places:
    showing = showing[:correct_letter] + guess + showing[correct_letter + 1:]
  print("Winnings:", winnings)
  print_board(showing)
