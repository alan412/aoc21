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
    self.cachedRules = {}
    self.rulesAfter = {}
    self.numAfter = 0

  def replacePoly(self, line):
    self.polymer = line

  def addRule(self, line):
    m = re.match(pattern, line)
    if m:
      self.insertionRules[m.group(1)] = m.group(2)

  def generateRules(self, numSteps):
    self.numHits = 0
    self.numTotal = 0
    for rule in self.insertionRules:
      endPoly = rule
      for step in range(numSteps):
        endPoly = self.insert(endPoly)
      self.rulesAfter[rule] = endPoly
    self.numAfter = numSteps

  def insert(self, polymer):
    if len(polymer) < 2:
      return polymer
    #    print(f'insert {polymer}')
    newPoly = self.cachedRules.get(polymer, '')
    self.numTotal += 1
    if newPoly:
      self.numHits += 1
      return newPoly
    if len(polymer) == 2:
      newPoly = polymer[0] + self.insertionRules[polymer] + polymer[1]
    else:
      mid = len(polymer) // 2
      left = self.insert(polymer[:mid])
      right = self.insert(polymer[mid:])
      middle = self.insertionRules[polymer[mid - 1:mid + 1]]
      newPoly = left + middle + right

    self.cachedRules[polymer] = newPoly
    return newPoly

  def step(self):
    self.numHits = 0
    self.numTotal = 0
    self.polymer = self.insert(self.polymer)
    print(f"Cache: {self.numHits/self.numTotal}")

  def stepAfter(self):
    print(f"Len: {len(self.polymer)}")
    newPoly = self.polymer[:1]
    for index in range(len(self.polymer) - 1):
      if not (index % 10_000):
        print(index)
      newPoly += self.rulesAfter[self.polymer[index:index + 2]][1:]
    self.polymer = newPoly

  def addLetters(self, letterDicts, letters):
    for letter, value in letters.items():
      letterDicts[letter] = letterDicts.get(letter, 0) + value
    return letterDicts

  def scoreAfter(self):
    letterDicts = {}
    totalLetters = {}
    for k, v in self.rulesAfter.items():
      letterDicts[k] = self.getLetterDict(v)

    for index in range(len(self.polymer) - 1):
      if not (index % 10_000):
        print(index)
      totalLetters = self.addLetters(totalLetters,
                                     letterDicts[self.polymer[index:index + 2]])
      lastLetter = self.polymer[index + 1]
      totalLetters[lastLetter] = totalLetters[lastLetter] - 1
    totalLetters[lastLetter] = totalLetters[lastLetter] + 1

    leastCommon = totalLetters[lastLetter]
    mostCommon = 0
    print(totalLetters)
    for value in totalLetters.values():
      if value > mostCommon:
        mostCommon = value
      if value < leastCommon:
        leastCommon = value
    return mostCommon - leastCommon

  def getLetterDict(self, polymer):
    letters = {}
    for letter in polymer:
      letters[letter] = 1 + letters.get(letter, 0)
    return letters

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

  startTime = time.time()

  print('Generating Rules')
  poly.generateRules(20)
  print('Done:', time.time() - startTime)

  poly.stepAfter()
  #print("Step", step, '-', time.time() - startTime, len(poly.cachedRules))

  #  for step in range(40):
  #    poly.step()
  #    print("Step", step, '-', time.time() - startTime, len(poly.cachedRules))

  return poly.scoreAfter()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")