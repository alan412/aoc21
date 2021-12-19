import argparse
import time
import re
import sys
import copy


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Pair:

  def __init__(self, el1, el2):
    self.el1 = el1
    self.el2 = el2

  def getMagnitude(self):
    el1Value = 0
    el2Value = 0
    if isinstance(self.el1, Pair):
      el1Value = self.el1.getMagnitude()
    else:
      el1Value = self.el1
    if isinstance(self.el2, Pair):
      el2Value = self.el2.getMagnitude()
    else:
      el2Value = self.el2

    return (el1Value * 3) + (el2Value * 2)

  def split(self):
    result = False
    if isinstance(self.el1, Pair):
      result = self.el1.split()
      if result:
        return True
    elif self.el1 >= 10:
      newLeft = self.el1 // 2
      newRight = self.el1 - newLeft
      self.el1 = Pair(newLeft, newRight)
      return True
    if isinstance(self.el2, Pair):
      result = self.el2.split()
      if result:
        return True
    elif self.el2 >= 10:
      newLeft = self.el2 // 2
      newRight = self.el2 - newLeft
      self.el2 = Pair(newLeft, newRight)
      return True
    return False

  def addLeftMost(self, number):
    if isinstance(self.el1, Pair):
      return self.el1.addLeftMost(number)
    self.el1 += number

  def addRightMost(self, number):
    if isinstance(self.el2, Pair):
      return self.el2.addRightMost(number)
    self.el2 += number

  def explode(self, depth):
    if depth == 4 and isinstance(self.el1, int) and isinstance(self.el2, int):
      return (True, True, (self.el1, self.el2))

    if isinstance(self.el1, Pair):
      (exploded, newlyExploded, (left, right)) = self.el1.explode(depth + 1)
      if newlyExploded:
        self.el1 = 0
      if right:
        if isinstance(self.el2, int):
          self.el2 += right
        else:
          self.el2.addLeftMost(right)
        return (exploded, False, (left, None))
      if exploded:
        return (exploded, False, (left, right))
    if isinstance(self.el2, Pair):
      (exploded, newlyExploded, (left, right)) = self.el2.explode(depth + 1)
      if newlyExploded:
        self.el2 = 0
      if left:
        if isinstance(self.el1, int):
          self.el1 += left
        else:
          self.el1.addRightMost(left)
        return (exploded, False, (None, right))
      if exploded:
        return (exploded, False, (left, right))

    return (False, False, (None, None))

  def reduce(self, newPair):
    (exploded, _, (left, right)) = newPair.explode(0)

    if exploded:
      # print("Ex:", newPair, left, right)
      return (True, newPair)

    didSplit = newPair.split()
    # if didSplit:
    #   print("Sp:", newPair)
    return (didSplit, newPair)

  def __add__(self, other):
    newPair = Pair(self, other)
    reduced = True
    while reduced:
      (reduced, newPair) = self.reduce(newPair)
    return newPair

  def __repr__(self):
    return f"[{self.el1}, {self.el2}]"


def parsePair(line):
  # a pair is "["."(number or pair)", "," (number or pair), "]"
  line = line[1:]  # strip off open bracket
  if line[0] == '[':
    (element1, nextIndex) = parsePair(line[0:])
  else:
    commaPos = line.find(",")
    element1 = int(line[:commaPos])
    nextIndex = commaPos

  nextIndex += 1  # Skip over comma

  if line[nextIndex] == '[':
    (element2, nextIndex2) = parsePair(line[nextIndex:])
    nextIndex += nextIndex2

  else:
    closePos = line[nextIndex:].find("]")
    closePos += nextIndex
    element2 = int(line[nextIndex:closePos])
    nextIndex = closePos
  nextIndex += 2  # One for opening bracket and one for closing

  return (Pair(element1, element2), nextIndex)


def puzzle(filename):
  listNumbers = []

  for line in open(filename, 'r'):
    (pair, _) = parsePair(line.strip())
    listNumbers.append(pair)

  largest = 0
  print(listNumbers)
  print("----")
  for num1 in listNumbers:
    for num2 in listNumbers:
      if num1 != num2:
        add1 = copy.deepcopy(num1)
        add2 = copy.deepcopy(num2)
        print(num1, "\n+", num2)
        newPair = add1 + add2
        value = newPair.getMagnitude()
        print("= ", newPair, "***", value)
        if value > largest:
          largest = value

  return largest


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")