import argparse
import time
import re
import sys
from collections import defaultdict


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def intersectRange(x, y):
  return range(max(x[0], y[0]), min(x[-1], y[-1]) + 1)


class Reactor():

  def __init__(self):
    self.cubes = defaultdict(bool)

  def step(self, instr, coords):
    cubeRange = range(-50, 50 + 1)
    xRange = range(coords[0], coords[1] + 1)
    yRange = range(coords[2], coords[3] + 1)
    zRange = range(coords[4], coords[5] + 1)

    for x in intersectRange(cubeRange, xRange):
      for y in intersectRange(cubeRange, yRange):
        for z in intersectRange(cubeRange, zRange):
          self.cubes[(x, y, z)] = (instr == 'on')

  def numCubesOn(self):
    numCubes = 0
    for value in self.cubes.values():
      if value:
        numCubes += 1
    return numCubes


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