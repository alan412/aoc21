import argparse
import time
import re

pattern = re.compile('fold along (x|y)=(\d+)')


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Paper:

  def __init__(self):
    self.dots = set()
    self.folds = []

  def addDot(self, line):
    (x, y) = line.split(',')
    self.dots.add((int(x), int(y)))

  def addFolds(self, line):
    m = re.match(pattern, line)
    if m:
      self.folds.append((m.group(1), int(m.group(2))))

  def fold(self):
    (foldDirection, pos) = self.folds[0]
    newDots = set()

    for dot in self.dots:
      (x, y) = dot
      (newX, newY) = (x, y)
      if foldDirection == 'x':
        if x > pos:
          newX = pos - (x - pos)
      else:
        if y > pos:
          newY = pos - (y - pos)
      newDots.add((newX, newY))

    self.dots = newDots
    self.folds = self.folds[1:]

    return len(self.dots)

  def __repr__(self):
    result = ''
    for dot in self.dots:
      result += f'({dot[0]}, {dot[1]}) '
    result += '\n'
    for fold in self.folds:
      result += f'fold: ({fold[0]}, {fold[1]})\n'
    return result

  def printDots(self):
    maxX = 0
    maxY = 0
    for dot in self.dots:
      (x, y) = dot
      if x > maxX:
        maxX = x
      if y > maxY:
        maxY = y
    for y in range(maxY + 1):
      line = ''
      for x in range(maxX + 1):
        line += '#' if (x, y) in self.dots else '.'
      print(line)


def puzzle(filename):
  paper = Paper()

  doneDots = False
  for line in open(filename, 'r'):
    line = line.strip()
    if not line:
      doneDots = True
    else:
      if doneDots:
        paper.addFolds(line)
      else:
        paper.addDot(line)
  while paper.folds:
    answer = paper.fold()
  print(paper)
  paper.printDots()
  return answer


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")