import argparse
import time
import math


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Cave:

  def __init__(self, name):
    self.paths = set()
    self.name = name
    self.isLarge = name.isupper()

  def addPath(self, pathName):
    if self.name != 'end' and pathName != 'start':
      self.paths.add(pathName)

  def followPath(self, smallVisited, caves):
    if self.name == 'end':
      #      print(f'At end : {visited}')
      return 1

    if self.name in smallVisited:
      #      print(f'Already visited: {self.name}, {visited}')
      return 0

    newVisited = smallVisited[:]

    if not self.isLarge:
      newVisited.append(self.name)
    totalPaths = 0
    for path in self.paths:
      numPaths = caves[path].followPath(newVisited, caves)
      #        print(f"({numPaths}) Visited: {path} from {newVisited}")
      totalPaths += numPaths
    return totalPaths

  def __repr__(self):
    return f'{self.name} : {self.paths}'


class Maze:

  def __init__(self):
    self.caves = {'start': Cave('start'), 'end': Cave('end')}

  def parseLine(self, line):
    caves = line.strip().split('-')
    startCave = caves[0]
    endCave = caves[1]
    if startCave not in self.caves:
      self.caves[startCave] = Cave(startCave)
    if endCave not in self.caves:
      self.caves[endCave] = Cave(endCave)
    self.caves[startCave].addPath(endCave)
    self.caves[endCave].addPath(startCave)

  def __repr__(self):
    result = ''
    for cave in self.caves.values():
      result += str(cave) + '\n'
    return result

  def findPaths(self):
    totalPaths = self.caves['start'].followPath([], self.caves)
    return totalPaths


def puzzle(filename):
  maze = Maze()
  for line in open(filename, 'r'):
    maze.parseLine(line)

  totalPaths = maze.findPaths()

  return totalPaths


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")