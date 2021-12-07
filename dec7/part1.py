import argparse
import re
import time
import statistics


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Crabs():

  def __init__(self, line):
    self.crabs = {}
    positions = [int(num) for num in line.split(',')]
    self.median = int(statistics.median(positions))
    for position in positions:
      self.crabs[position] = 1 + self.crabs.get(position, 0)

  def findFuel(self, newPosition):
    amountFuel = 0
    for position, crabs in self.crabs.items():
      amountFuel += abs(position - newPosition) * crabs
    return amountFuel


def puzzle(filename):
  for line in open(filename, 'r'):
    c = Crabs(line)

  newPos = c.median
  print("NewPos", newPos)

  return c.findFuel(newPos)


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")