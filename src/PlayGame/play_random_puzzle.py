import random
import re

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

# Play the game
while showing != puzzle:
  guess = input().upper()
  # TODO: Assert it is one character and A-Z
  correct_places = []
  for pos,char in enumerate(puzzle):
    if(char == guess):
        correct_places.append(pos)
  #print(correct_places)
  for correct_letter in correct_places:
    showing = showing[:correct_letter] + guess + showing[correct_letter + 1:]
  print_board(showing)
