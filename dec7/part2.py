import argparse
import re
import time
import statistics
import math


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Crabs():

  def __init__(self, line):
    self.fuelCosts = {0: 0, 1: 1}
    self.crabs = {}
    positions = [int(num) for num in line.split(',')]
    self.median = int(statistics.median(positions))
    self.maxPosition = 0
    for position in positions:
      self.crabs[position] = 1 + self.crabs.get(position, 0)
      if position > self.maxPosition:
        self.maxPosition = position

  def fuel(self, diffPos):
    try:
      return self.fuelCosts[diffPos]
    except KeyError:
      cost = 0
      for x in range(diffPos + 1):
        cost += x
      self.fuelCosts[diffPos] = cost
      return cost

  def findFuel(self, newPosition):
    amountFuel = 0
    for position, crabs in self.crabs.items():
      fuelPerCrab = self.fuel(abs(position - newPosition))
      amountFuel += fuelPerCrab * crabs
    return amountFuel

  def findMinFuel(self):
    minFuel = math.inf

    for newPos in range(self.maxPosition):
      fuel = self.findFuel(newPos)
      if fuel < minFuel:
        #        print("Smaller found at: ", newPos, fuel)
        minFuel = fuel
    return minFuel


def puzzle(filename):
  for line in open(filename, 'r'):
    c = Crabs(line)

  minFuel = c.findMinFuel()

  return minFuel


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")