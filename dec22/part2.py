import argparse
import time
import re
import sys
from collections import defaultdict


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def lineIntersection(line1, line2):
  left = max(line1[0], line2[0])
  right = min(line1[1], line2[1])
  if right - left <= 0:
    return False
  return (left, right)


class CubeRange():

  def __init__(self, xRange, yRange, zRange, op='on'):
    self.xRange = xRange
    self.yRange = yRange
    self.zRange = zRange
    self.on = op == 'on'

  def __repr__(self):
    return f"{'+' if self.on else '-'} x:{self.xRange}, y:{self.yRange} z:{self.zRange}, ({self.size()})"

  def intersection(self, other):
    x = lineIntersection(self.xRange, other.xRange)
    y = lineIntersection(self.yRange, other.yRange)
    z = lineIntersection(self.zRange, other.zRange)
    if x and y and z:
      return CubeRange(x, y, z)
    return False

  def size(self):
    x = (self.xRange[1] - self.xRange[0]) + 1
    y = (self.yRange[1] - self.yRange[0]) + 1
    z = (self.zRange[1] - self.zRange[0]) + 1
    return x * y * z * (1 if self.on else -1)


class Reactor():

  def __init__(self):
    self.cubeRanges = []

  def step(self, instr, coords):
    self.cubeRanges.append(
        CubeRange((coords[0], coords[1]), (coords[2], coords[3]),
                  (coords[4], coords[5]), instr))

  def numCubesOn(self):
    listCubes = [self.cubeRanges[0]]
    # look for all intersections
    for cube in self.cubeRanges[1:]:
      for cr in listCubes.copy():
        newRange = cr.intersection(cube)
        if newRange:
          if cr.on:
            newRange.on = False
          listCubes.append(newRange)
      if cube.on:
        listCubes.append(cube)

    total = 0
    for cube in listCubes:
      total += cube.size()
    return total


pattern = re.compile(
    '(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')


def puzzle(filename):
  reactor = Reactor()

  for line in open(filename, 'r'):
    m = re.match(pattern, line)
    if m:
      reactor.step(m.group(1), [
          int(m.group(2)),
          int(m.group(3)),
          int(m.group(4)),
          int(m.group(5)),
          int(m.group(6)),
          int(m.group(7))
      ])

  return reactor.numCubesOn()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")