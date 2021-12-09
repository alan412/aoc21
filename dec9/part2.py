import argparse
import time


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
    self.lowPoints = []
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
        self.lowPoints.append((row, col))
        sumRisk += (1 + value)
    return sumRisk

  def getValue(self, row, col):
    if row < 0 or col < 0:
      return 9
    if row >= len(self.heightMap):
      return 9
    if col >= len(self.heightMap[0]):
      return 9
    try:
      return self.heightMap[row][col]
    except IndexError:
      return 9

  def getBasins(self):
    basins = []
    self.findLow()
    for pt in self.lowPoints:
      (row, col) = pt
      basins.append(self.getBasinSize(row, col))
    basins.sort(reverse=True)
    answer = basins[0] * basins[1] * basins[2]
    return answer

  def getBasinSize(self, row, col):
    basinPoints = set()
    basinPoints.add((row, col))
    oldSize = len(basinPoints)
    done = False
    while not done:
      basinPoints = self.growBasin(basinPoints)
      newSize = len(basinPoints)
      if newSize == oldSize:
        done = True
      oldSize = newSize
    return newSize

  def growBasin(self, basinPoints):
    newBasinPoints = basinPoints.copy()
    for point in basinPoints:
      (row, col) = point
      if self.getValue(row - 1, col) != 9:
        newBasinPoints.add((row - 1, col))
      if self.getValue(row + 1, col) != 9:
        newBasinPoints.add((row + 1, col))
      if self.getValue(row, col - 1) != 9:
        newBasinPoints.add((row, col - 1))
      if self.getValue(row, col + 1) != 9:
        newBasinPoints.add((row, col + 1))
    return newBasinPoints


def puzzle(filename):
  hm = HeightMap()

  for line in open(filename, 'r'):
    hm.addLine(line)

  return hm.getBasins()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")