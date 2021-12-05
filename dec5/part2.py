import argparse
import re
from typing import SupportsComplex

pattern = re.compile('(\d+),(\d+) -> (\d+),(\d+)')


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class MapFloor():

  def __init__(self):
    self.floor = {}

  def addLine(self, line):
    m = re.match(pattern, line)
    startX = int(m.group(1))
    startY = int(m.group(2))
    endX = int(m.group(3))
    endY = int(m.group(4))

    if (startX != endX) and (startY != endY):  # if not horiz or vert,
      if abs(endX - startX) != abs(endY - startY):  # not 45 degrees, bail
        return

    if startX == endX:
      xStep = 0
    elif startX > endX:
      xStep = -1
    else:
      xStep = 1

    if startY == endY:
      yStep = 0
    elif startY > endY:
      yStep = -1
    else:
      yStep = 1

    x = startX
    y = startY
    self.floor[(x, y)] = self.floor.get((x, y), 0) + 1
    while not ((x == endX) and (y == endY)):
      x += xStep
      y += yStep
      self.floor[(x, y)] = self.floor.get((x, y), 0) + 1

  def display(self):
    for y in range(10):
      line = ''
      for x in range(10):
        num = self.floor.get((x, y), 0)
        line += str(num) if num > 0 else '.'
      print(line)

  def atLeast(self, number):
    #    self.display()
    sum = 0
    for val in self.floor.values():
      if val >= number:
        sum += 1
    return sum


def puzzle(filename):
  mapFloor = MapFloor()
  for line in open(filename, 'r'):
    mapFloor.addLine(line.strip())
  return mapFloor.atLeast(2)


if __name__ == "__main__":
  args = parseArgs()

  print(f"Answer: {puzzle(args.infile)}")