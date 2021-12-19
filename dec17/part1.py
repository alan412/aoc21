import argparse
import time
import re
import sys


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Point():

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __repr__(self):
    return f"({self.x},{self.y})"


class Probe():

  def __init__(self, minTarget, maxTarget):
    self.minTarget = minTarget
    self.maxTarget = maxTarget

  def shoot(self, startVelocity):
    pos = Point(0, 0)
    done = False
    velocity = startVelocity
    highest = 0
    while not done:
      pos.x += velocity.x
      pos.y += velocity.y
      if velocity.x > 0:
        velocity.x -= 1
      elif velocity.x < 0:
        velocity.x += 1
      velocity.y -= 1
      if pos.y > highest:
        highest = pos.y
      if pos.y < self.minTarget.y:
        return -1  # won't make it
      elif self.minTarget.x <= pos.x <= self.maxTarget.x and \
           self.minTarget.y <= pos.y <= self.maxTarget.y:
        done = True
    return highest

  def solve(self):
    highest = 0
    highestStart = (1, 1)
    # lazy way to do it fast
    for y in range(1, 200):
      for x in range(1, 200):
        startVel = Point(x, y)
        height = self.shoot(startVel)
        if height > highest:
          print("New Highest", height, (x, y))
          highest = height
          highestStart = startVel
    print(highest, "at", highestStart)
    return highest


def puzzle(filename):
  pattern = re.compile('target area: x=(\d+)..(\d+), y=(-\d+)..(-\d+)')

  for line in open(filename, 'r'):
    m = re.match(pattern, line)
    minTarget = Point(int(m.group(1)), int(m.group(3)))
    maxTarget = Point(int(m.group(2)), int(m.group(4)))

    probe = Probe(minTarget, maxTarget)
    return probe.solve()
  return -1


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")