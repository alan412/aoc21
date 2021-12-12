import argparse
import time
import math


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Octopi:

  def __init__(self):
    self.lines = []
    self.flashes = set()

  def readLine(self, line):
    digits = [int(ch) for ch in line.strip()]
    self.lines.append(digits)

  def increase(self, x, y):
    if (x >= 0 and x <= 9) and (y >= 0 and y <= 9):
      self.lines[y][x] += 1

  def flash(self, x, y):
    if (x, y) not in self.flashes:
      self.flashes.add((x, y))
      self.increase(x - 1, y - 1)
      self.increase(x - 1, y)
      self.increase(x - 1, y + 1)
      self.increase(x, y - 1)
      self.increase(x, y + 1)
      self.increase(x + 1, y - 1)
      self.increase(x + 1, y)
      self.increase(x + 1, y + 1)
      return True
    return False

  def step(self):
    for y in range(10):
      for x in range(10):
        self.lines[y][x] += 1
    self.flashes = set()
    oldFlashes = self.flashes.copy()
    done = False

    while not done:
      for y in range(10):
        for x in range(10):
          if self.lines[y][x] > 9:
            self.flash(x, y)
      if self.flashes.issubset(oldFlashes):
        done = True
      else:
        oldFlashes = self.flashes.copy()

    numFlashes = 0
    for y in range(10):
      for x in range(10):
        if self.lines[y][x] > 9:
          self.lines[y][x] = 0
          numFlashes += 1
    return numFlashes

  def __repr__(self):
    result = ''
    for y in range(10):
      for x in range(10):
        result += str(self.lines[y][x]) + ' '
      result += '\n'
    return result


def puzzle(filename):
  octopi = Octopi()
  for line in open(filename, 'r'):
    octopi.readLine(line)
  print(octopi)

  totalFlashes = 0
  for day in range(100):
    totalFlashes += octopi.step()


#    print('after step', day + 1, '\n', octopi)

  return totalFlashes

if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")