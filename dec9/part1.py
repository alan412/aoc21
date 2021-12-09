import argparse
import time
import math


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class HeightMap():

  def __init__(self):
    self.heightMap = []

  def addLine(self, line):
    self.heightMap.append([int(ch) for ch in line.strip()])

  def findLow(self):
    sumRisk = 0
    numRows = len(self.heightMap)
    for row, line in enumerate(self.heightMap):
      numCols = len(line)
      for col, value in enumerate(line):
        if col != 0:
          if line[col - 1] <= value:
            continue
        if col + 1 != numCols:
          if line[col + 1] <= value:
            continue
        if row != 0:
          if self.heightMap[row - 1][col] <= value:
            continue
        if row + 1 != numRows:
          if self.heightMap[row + 1][col] <= value:
            continue
        print(f"Found low point: {value} at {row}{col}")
        sumRisk += (1 + value)
    return sumRisk


def puzzle(filename):
  hm = HeightMap()

  for line in open(filename, 'r'):
    hm.addLine(line)

  return hm.findLow()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")