import argparse
import re


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  parser.add_argument('num_days', type=int)
  return parser.parse_args()


class LanternFishes():

  def __init__(self, line):
    self.lanternFish = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    #    {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    for value in line.split(','):
      days = int(value)
      self.lanternFish[days] = 1 + self.lanternFish[days]

  def newDay(self):
    newFish = {}
    for i in range(8):
      newFish[i] = self.lanternFish[i + 1]
    newFish[8] = self.lanternFish[0]
    newFish[6] += self.lanternFish[0]
    self.lanternFish = newFish

  def getNumFishes(self):
    sumFish = 0
    for numFish in self.lanternFish.values():
      sumFish += numFish
    return sumFish


def puzzle(filename, numDays):
  for line in open(filename, 'r'):
    lf = LanternFishes(line)

    for i in range(numDays):
      #      print(f"Day {i}: {lf.getNumFishes()} {lf.lanternFish}")
      lf.newDay()

  return lf.getNumFishes()


if __name__ == "__main__":
  args = parseArgs()

  print(f"Answer: {puzzle(args.infile, args.num_days)}")