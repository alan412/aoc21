import argparse
import time
import math


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


matchChars = {'(': ')', '[': ']', '{': '}', '<': '>'}


class Syntax:

  def __init__(self, line):
    self.line = line.strip()
    self.complete = ''

    opening = ''
    for index, ch in enumerate(self.line):
      if ch in matchChars.keys():
        opening += ch
      elif ch in matchChars.values():
        if matchChars[opening[-1]] == ch:
          opening = opening[:-1]
        else:
          # print(f'{self.line} - Expected close of {matchChars[opening[-1]]}, but found {ch} instead')
          return
      else:
        print(f"None??? {ch}")

    for ch in reversed(opening):
      self.complete += matchChars[ch]

  def getScore(self):
    scores = {')': 1, ']': 2, '}': 3, '>': 4}
    total = 0
    for ch in self.complete:
      total = (total * 5) + scores[ch]
    if total:
      print(f'{self.complete} - {total}')
    return total


def puzzle(filename):
  scores = []
  for line in open(filename, 'r'):
    sl = Syntax(line)
    score = sl.getScore()
    if score:
      scores.append(score)

  scores.sort()
  print(scores)
  middleScore = scores[int((len(scores) - 1) / 2)]

  return middleScore


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")