import argparse
import time
import re


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


cache = {}


def move(currPlayerPos, otherPlayerPos, currPlayerScore, otherPlayerScore):
  if currPlayerScore >= 21:
    return [1, 0]
  if otherPlayerScore >= 21:
    return [0, 1]

  win = [0, 0]

  for die1 in range(1, 4):
    for die2 in range(1, 4):
      for die3 in range(1, 4):
        newPos = ((currPlayerPos + die1 + die2 + die3 - 1) % 10) + 1
        newScore = currPlayerScore + newPos
        # flip which player is which
        recurse = cache.get(
            (otherPlayerPos, newPos, otherPlayerScore, newScore), None)
        if not recurse:
          recurse = move(otherPlayerPos, newPos, otherPlayerScore, newScore)
          cache[(otherPlayerPos, newPos, otherPlayerScore, newScore)] = recurse
        win = [win[0] + recurse[1], win[1] + recurse[0]]
  return win


pattern = re.compile("Player (\d) starting position: (\d+)")


def puzzle(filename):
  startPos = {}

  for line in open(filename, 'r'):
    m = re.match(pattern, line)
    if m:
      startPos[int(m.group(1))] = int(m.group(2))

  return max(move(startPos[1], startPos[2], 0, 0))


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")