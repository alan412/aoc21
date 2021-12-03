import argparse
import re
from collections import defaultdict


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def readData(filename):
  reg = re.compile('(forward|down|up) (\d+)')
  depth = 0
  hPos = 0
  aim = 0

  for line in open(filename, 'r'):
    m = reg.match(line)
    direction = m.group(1)
    amount = int(m.group(2))
    if direction == 'forward':
      hPos += amount
      depth += aim * amount
    elif direction == 'down':
      aim += amount
    elif direction == 'up':
      aim -= amount

  return hPos * depth


if __name__ == "__main__":
  args = parseArgs()
  data = readData(args.infile)
  print(f"Answer: {data}")