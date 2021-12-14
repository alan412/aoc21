import argparse
import time
import re

pattern = re.compile('(\w+) -> (\w)')


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Polymer():

  def __init__(self):
    self.polymer = ''
    self.insertionRules = {}

  def replacePoly(self, line):
    self.polymer = line

  def addRule(self, line):
    m = re.match(pattern, line)
    if m:
      self.insertionRules[m.group(1)] = m.group(2)

  def step(self):
    newPoly = self.polymer[:1]
    for index in range(len(self.polymer) - 1):
      newPoly += self.insertionRules[self.polymer[index:index +
                                                  2]] + self.polymer[index + 1]
    self.polymer = newPoly

  def getScore(self):
    letters = {}
    for letter in self.polymer:
      letters[letter] = 1 + letters.get(letter, 0)

    leastCommon = len(self.polymer)
    mostCommon = 0
    for letter in letters:
      value = letters[letter]
      if value > mostCommon:
        mostCommon = value
      if value < leastCommon:
        leastCommon = value

    return mostCommon - leastCommon

  def __repr__(self):
    return f'{self.polymer} : {self.insertionRules}'


def puzzle(filename):
  poly = Polymer()

  doneTemplate = False
  for line in open(filename, 'r'):
    line = line.strip()
    if not line:
      doneTemplate = True
    else:
      if not doneTemplate:
        poly.replacePoly(line)
      else:
        poly.addRule(line)

  for step in range(10):
    poly.step()
    print(step)

  return poly.getScore()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")