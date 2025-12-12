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
        clue = clue.replace("&amp;", "&") # HTML Code
        puzzle = puzzle.replace("&amp;", "&") # HTML Code
        return(puzzle, clue, date, game_type)
      number = number + 1

def get_only_puzzle(file):
  puzzles = ""
  with open(f"{file}.csv") as f:
    for line in f:
      line = line.rstrip('\n')

      line = re.sub("\<br.*\</i", "", line)
      line = re.sub("(\d),(\d)", r"\1.\2", line)
      line = re.sub(",/td><td.*>", "", line)

      puzzle, clue, date, game_type = line.split(',')
      clue = clue.replace("&amp;", "&") # HTML Code
      puzzle = puzzle.replace("&amp;", "&") # HTML Code
      puzzles += puzzle + "\n"
  with open(f"{file}.txt", "x") as f:
    f.write(puzzles)

if __name__ == "__main__":
  get_only_puzzle("years_1_25")

    