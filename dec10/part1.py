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
    self.restLine = ''

    opening = ''
    for index, ch in enumerate(self.line):
      if ch in matchChars.keys():
        opening += ch
      elif ch in matchChars.values():
        if matchChars[opening[-1]] == ch:
          opening = opening[:-1]
        else:
          print(
              f'{self.line} - Expected close of {matchChars[opening[-1]]}, but found {ch} instead'
          )
          self.restLine = self.line[index:]
          return
      else:
        print(f"None??? {ch}")

  def getScore(self):
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    try:
      return scores[self.restLine[0]]
    except IndexError:
      return 0


def puzzle(filename):
  totalScore = 0
  for line in open(filename, 'r'):
    sl = Syntax(line)
    totalScore += sl.getScore()

  return totalScore


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")