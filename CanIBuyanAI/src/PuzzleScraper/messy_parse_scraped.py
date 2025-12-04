import sys

with open(sys.argv[1]) as f:
  puzzle = ""
  in_row = False
  for line in f:
    line = line.rstrip('\n')
    #print(line)
    if line == "</tr>":
      puzzle = puzzle.lstrip(',')
      print(puzzle)
      in_row = False
    elif in_row:
      cleaned = line.lstrip("<td align=\"center\">")
      cleaned = cleaned.rstrip("</td>")
      puzzle = puzzle + "," + cleaned
    elif line == "<tr>":
      in_row = True
      puzzle = ""
