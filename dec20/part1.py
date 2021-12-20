import argparse
import time
import re
import sys
from collections import defaultdict


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Image:

  def __init__(self):
    self.pixels = defaultdict(bool)
    self.minX = 0
    self.minY = 0
    self.maxX = 0
    self.maxY = 0
    self.outside = False

  def addRow(self, line, lineNum):
    if lineNum > self.maxY:
      self.maxY = lineNum
    for i, ch in enumerate(line):
      if ch == '#':
        self.pixels[(i, lineNum)] = True
        if i > self.maxX:
          self.maxX = i

  def getPixel(self, x, y):
    if x < self.minX or x > self.maxX:
      return self.outside
    if y < self.minY or y > self.maxY:
      return self.outside
    return self.pixels[(x, y)]

  def getValue(self, x, y):
    value = ""
    for yi in range(y - 1, y + 2):
      for xi in range(x - 1, x + 2):
        value += "1" if self.getPixel(xi, yi) else "0"

    return int(value, 2)

  def enhance(self, enhancementAlgorithm):
    newImage = defaultdict(bool)

    # enhancing causes to grow
    self.minX, self.minY = self.minX - 1, self.minY - 1
    self.maxX, self.maxY = self.maxX + 1, self.maxY + 1

    for x in range(self.minX, self.maxX + 1):
      self.pixels[(x, self.minY)] = self.outside
      self.pixels[(x, self.maxY)] = self.outside
    for y in range(self.minY, self.maxY + 1):
      self.pixels[(self.minX, y)] = self.outside
      self.pixels[(self.maxX, y)] = self.outside

    for x in range(self.minX, self.maxX + 1):
      for y in range(self.minY, self.maxY + 1):
        newImage[(x, y)] = enhancementAlgorithm[self.getValue(x, y)]
    self.pixels = newImage
    if self.outside:
      self.outside = enhancementAlgorithm[511]
    else:
      self.outside = enhancementAlgorithm[0]

  def numPixels(self):
    numPixels = 0
    for value in self.pixels.values():
      if value:
        numPixels += 1
    return numPixels

  def __repr__(self):
    result = ""
    for y in range(self.minY, self.maxY + 1):
      for x in range(self.minX, self.maxX + 1):
        result += "#" if self.pixels[(x, y)] else "."
      result += "\n"
    return result


def puzzle(filename):
  enhancementAlgorithm = None
  image = Image()
  lineNum = 0
  for line in open(filename, 'r'):
    line = line.strip()
    if not enhancementAlgorithm:
      enhancementAlgorithm = [(ch == '#') for ch in line]
    elif line:
      image.addRow(line, lineNum)
      lineNum += 1

  for _ in range(2):
    image.enhance(enhancementAlgorithm)

  return image.numPixels()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")