import argparse
import time
import re
import sys
from collections import defaultdict


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Die():

  def __init__(self):
    self.numSides = 100
    self.nextRoll = 1
    self.numRolls = 0

  def roll(self):
    thisRoll = self.nextRoll
    self.nextRoll = (self.nextRoll % self.numSides) + 1
    self.numRolls += 1
    return thisRoll


class Game():

  def __init__(self, p1Start, p2Start):
    self.playerPos = [p1Start, p2Start]
    self.playerScores = [0, 0]
    self.die = Die()

  def move(self, pos):
    dieRolls = self.die.roll() + self.die.roll() + self.die.roll()
    pos = pos + dieRolls
    while pos > 10:
      pos -= 10
    return pos

  def play(self):
    done = False
    print(f"Scores: {self.playerScores} Positions {self.playerPos}")
    while not done:
      self.playerPos[0] = self.move(self.playerPos[0])
      self.playerScores[0] += self.playerPos[0]
      if self.playerScores[0] >= 1_000:
        done = True
      else:
        self.playerPos[1] = self.move(self.playerPos[1])
        self.playerScores[1] += self.playerPos[1]
        if self.playerScores[1] >= 1_000:
          done = True
      print(f"Scores: {self.playerScores} Positions {self.playerPos}")
    return min(self.playerScores) * self.die.numRolls


pattern = re.compile("Player (\d) starting position: (\d+)")


def puzzle(filename):
  startPos = {}

  for line in open(filename, 'r'):
    m = re.match(pattern, line)
    if m:
      startPos[int(m.group(1))] = int(m.group(2))

  game = Game(startPos[1], startPos[2])
  return game.play()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")