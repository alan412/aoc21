import argparse
import time
import re
import sys
import heapq


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Maze:

  def __init__(self):
    self.costs = []

  def addRow(self, line):
    row = len(self.costs)
    self.costs.append([int(cost) for cost in line])

  def enlarge(self):
    newCosts = {}
    size = len(self.costs)
    for row in range(size):
      for col in range(size):
        for rowOffset in range(5):
          for colOffset in range(5):
            newCost = (self.getCost(col, row) + rowOffset + colOffset)
            while newCost > 9:
              newCost -= 9
            newCosts[(row + (rowOffset * size),
                      col + (colOffset * size))] = newCost
    self.costs = []
    for row in range(5 * size):
      newRow = []
      for col in range(5 * size):
        newRow.append(newCosts[(row, col)])
      self.costs.append(newRow)

  def getCost(self, x, y):
    return self.costs[y][x]

  def getNeighbors(self, node):
    neighbors = []
    (x, y) = node
    if x > 0:
      neighbors.append((x - 1, y))
    if y > 0:
      neighbors.append((x, y - 1))
    newX = x + 1
    if newX < len(self.costs):
      neighbors.append((newX, y))
    newY = y + 1
    if newY < len(self.costs):
      neighbors.append((x, newY))
    return neighbors

  def getLowestRisk(self):
    size = len(self.costs)

    shortestPath = [[sys.maxsize] * size for row in self.costs]
    shortestPath[0][0] = 0
    queue = []
    heapq.heappush(queue, (0, 0, 0))

    while True:
      _, x, y = heapq.heappop(queue)
      c = shortestPath[y][x]
      if y == (size - 1) and x == (size - 1):
        return c
      for (newX, newY) in self.getNeighbors((x, y)):
        d = c + self.costs[newY][newX]
        if d < shortestPath[newY][newX]:
          shortestPath[newY][newX] = d
          heapq.heappush(queue, (d, newX, newY))

  def __repr__(self):
    result = ''
    for row in self.costs:
      for col in row:
        result += str(col)
      result += '\n'
    return result


def puzzle(filename):
  maze = Maze()

  for line in open(filename, 'r'):
    maze.addRow(line.strip())

  maze.enlarge()
  #  print(maze)
  return maze.getLowestRisk()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")