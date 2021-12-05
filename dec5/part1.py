import argparse
import re

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

    if startX > endX:
      (startX, endX) = (endX, startX)
    if startY > endY:
      (startY, endY) = (endY, startY)

    if (startX != endX) and (startY != endY):  # if not horiz or vert, bail
      return

    for x in range(startX, endX + 1):
      for y in range(startY, endY + 1):
        self.floor[(x, y)] = self.floor.get((x, y), 0) + 1

  def atLeast(self, number):
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