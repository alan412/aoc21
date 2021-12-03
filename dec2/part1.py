import argparse
import re
from collections import defaultdict


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def readData(filename):
  reg = re.compile('(forward|down|up) (\d+)')
  data = defaultdict(int)
  for line in open(filename, 'r'):
    m = reg.match(line)
    data[m.group(1)] += int(m.group(2))

  return data


def part1(data):
  return data['forward'] * (data['down'] - data['up'])


if __name__ == "__main__":
  args = parseArgs()
  data = readData(args.infile)
  print(f"Answer: {part1(data)}")