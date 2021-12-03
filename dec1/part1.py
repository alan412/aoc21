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


def part1(data):
  oldData = data[0]
  numIncreased = 0
  for datum in data:
    if datum > oldData:
      numIncreased = numIncreased + 1
    oldData = datum
  return numIncreased


if __name__ == "__main__":
  args = parseArgs()
  data = readData(args.infile)
  numIncreased = part1(data)
  print(f"{numIncreased}")