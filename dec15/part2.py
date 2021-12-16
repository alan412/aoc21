import argparse
import time
import re
import sys


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
    unvisitedNodes = []

    for row in range(size):
      for col in range(size):
        unvisitedNodes.append((row, col))
    shortestPath = {}
    previousNodes = {}

    for node in unvisitedNodes:
      shortestPath[node] = sys.maxsize
    shortestPath[(0, 0)] = 0

    while unvisitedNodes:
      currentMinNode = unvisitedNodes[0]
      for node in unvisitedNodes[1:]:
        if shortestPath[node] < shortestPath[currentMinNode]:
          currentMinNode = node
      for neighbor in self.getNeighbors(currentMinNode):
        (x, y) = neighbor
        tmpValue = shortestPath[currentMinNode] + self.getCost(x, y)
        if tmpValue < shortestPath[neighbor]:
          shortestPath[neighbor] = tmpValue
          previousNodes[neighbor] = currentMinNode
      unvisitedNodes.remove(currentMinNode)

    return shortestPath[(size - 1, size - 1)]

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