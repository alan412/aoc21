import argparse


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def readData(filename):
  data = []
  for line in open(filename, 'r'):
    data.append(int(line))
  return data


def part2(data):
  numElements = len(data)
  oldData = data[0] + data[1] + data[2]
  numIncreased = 0
  start = 0
  for i in range(numElements - 2):
    value = data[i] + data[i + 1] + data[i + 2]
    if value > oldData:
      numIncreased = numIncreased + 1
    oldData = value

  return numIncreased


if __name__ == "__main__":
  args = parseArgs()
  data = readData(args.infile)
  numIncreased = part2(data)
  print(f"{numIncreased}")