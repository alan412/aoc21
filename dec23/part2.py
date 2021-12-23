import argparse
import time
import re
import sys
from collections import defaultdict
from functools import cache


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


class Burrow:

  def __init__(self):
    self.cavern = ['.'] * 11
    self.roomSize = 4
    self.goal = [
        '.', '.', 'A' * self.roomSize, '.', 'B' * self.roomSize, '.',
        'C' * self.roomSize, '.', 'D' * self.roomSize, '.', '.'
    ]
    self.dest = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
    self.destSet = set(self.dest.values())
    self.hallwaySet = set({0, 1, 3, 5, 7, 9, 10})

  def addLine(self, line, y):
    rooms = {3: 0, 5: 1, 7: 2, 9: 3}
    for x, ch in enumerate(line):
      if ch in ['A', 'B', 'C', 'D']:
        if self.cavern[x - 1] != '.':
          self.cavern[x - 1] += ch
        else:
          self.cavern[x - 1] = ch

  def canReach(self, cavern, pos, dest):
    a = min(pos, dest)
    b = max(pos, dest)
    for i in range(a, b + 1):
      if i == pos:
        continue
      if i in self.destSet:
        continue
      if cavern[i] != '.':
        return False
    return True

  def roomOk(self, cavern, piece, dest):
    inRoom = cavern[dest]
    return len(inRoom) == inRoom.count('.') + inRoom.count(piece)

  def possibleMoves(self, cavern, pos):
    piece = cavern[pos]
    if pos not in self.destSet:
      dest = self.dest[piece]
      if self.canReach(cavern, pos, dest) and self.roomOk(cavern, piece, dest):
        return [dest]
      return []
    movingLetter = self.getPieceFromRoom(piece)
    if pos == self.dest[movingLetter] and self.roomOk(cavern, movingLetter,
                                                      pos):
      return []

    possible = []
    for dest in range(len(cavern)):
      if dest == pos:
        continue
      if dest in self.destSet and self.dest[movingLetter] != dest:
        continue
      if self.dest[movingLetter] == dest:
        if not self.roomOk(cavern, movingLetter, dest):
          continue
      if self.canReach(cavern, pos, dest):
        possible.append(dest)
    return possible

  def addToRoom(self, letter, room):
    room = list(room)
    dist = room.count('.')
    room[dist - 1] = letter
    return ''.join(room), dist

  def getPieceFromRoom(self, room):
    for c in room:
      if c != '.':
        return c

  def move(self, cavern, pos, dest):
    newCavern = cavern[:]
    dist = 0
    movingLetter = self.getPieceFromRoom(cavern[pos])
    if len(cavern[pos]) == 1:
      newCavern[pos] = '.'
    else:
      newRoom = ''
      found = False
      for c in cavern[pos]:
        if c == '.':
          dist += 1
          newRoom += c
        elif not found:
          newRoom += '.'
          dist += 1
          found = True
        else:
          newRoom += c
      newCavern[pos] = newRoom
    dist += abs(pos - dest)

    if len(cavern[dest]) == 1:
      newCavern[dest] = movingLetter
      return newCavern, dist * COSTS[movingLetter]
    else:
      newCavern[dest], addl_dist = self.addToRoom(movingLetter, cavern[dest])
      dist += addl_dist
      return newCavern, dist * COSTS[movingLetter]

  def solve(self):
    states = {tuple(self.cavern): 0}
    queue = [self.cavern]
    while queue:
      cavern = queue.pop()
      for pos, piece in enumerate(cavern):
        if self.getPieceFromRoom(piece) is None:
          continue
        dests = self.possibleMoves(cavern, pos)
        for dest in dests:
          newCavern, addlCost = self.move(cavern, pos, dest)
          newCost = states[tuple(cavern)] + addlCost
          newCavernTuple = tuple(newCavern)
          cost = states.get(newCavernTuple, sys.maxsize)
          if newCost < cost:
            states[newCavernTuple] = newCost
            queue.append(newCavern)
    return states[tuple(self.goal)]

  def __repr__(self):
    return f'{self.cavern}'


def puzzle(filename):
  burrow = Burrow()

  for i, line in enumerate(open(filename, 'r')):
    burrow.addLine(line, i)

  print(burrow)
  return burrow.solve()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")