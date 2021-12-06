import argparse
import re
import time


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  parser.add_argument('num_days', type=int)
  return parser.parse_args()


class LanternFishes():

  def __init__(self, line):
    self.lanternFish = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for value in line.split(','):
      days = int(value)
      self.lanternFish[days] = 1 + self.lanternFish[days]

  def newDay(self):
    newFish = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    newFish[0:8] = self.lanternFish[1:9]
    newFish[8] = self.lanternFish[0]
    newFish[6] += self.lanternFish[0]
    self.lanternFish = newFish

  def getNumFishes(self):
    sumFish = 0
    for numFish in self.lanternFish:
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

  startTime = time.time()
  answer = puzzle(args.infile, args.num_days)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")