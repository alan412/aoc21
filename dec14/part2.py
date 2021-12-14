import argparse
import time
import re
from collections import Counter

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

  def polymerize(self, numSteps):
    pair_frequencies = Counter()
    char_frequencies = Counter(self.polymer)

    for pos in range(1, len(self.polymer)):
      pair = self.polymer[pos - 1:pos + 1]
      pair_frequencies[pair] += 1

    for step in range(numSteps):
      pair_frequencies_step = Counter()
      for pair, frequency in pair_frequencies.items():
        if pair in self.insertionRules:
          insertChar = self.insertionRules[pair]
          pair_frequencies_step[pair[0] + insertChar] += frequency
          pair_frequencies_step[insertChar + pair[1]] += frequency
          char_frequencies[insertChar] += frequency
      pair_frequencies = pair_frequencies_step

    print(char_frequencies)
    return max(char_frequencies.values()) - min(char_frequencies.values())

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

  return poly.polymerize(40)


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")