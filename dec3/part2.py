import argparse
import re


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def readData(filename):
  data = []
  for line in open(filename, 'r'):
    data.append(line.strip())

  oxygen = calcOxygen(data)
  scrubber = calcScrubber(data)

  return oxygen * scrubber


def calcNumbers(data):
  numOnes = []
  numZeros = []
  numValues = 0
  for datum in data:
    if numValues == 0:
      numValues = len(datum)
      numOnes = [0] * numValues
      numZeros = [0] * numValues
    for i in range(numValues):
      if datum[i] == '1':
        numOnes[i] += 1
      else:
        numZeros[i] += 1
  return (numOnes, numZeros)


def reduceList(data, value, position):
  return [x for x in data if x[position] == value]


def calcGeneral(data, greaterValue, lesserValue):
  reducedList = data.copy()
  for i in range(len(data[0])):
    (numOnes, numZeros) = calcNumbers(reducedList)
    if numOnes[i] >= numZeros[i]:
      reducedList = reduceList(reducedList, greaterValue, i)
    else:
      reducedList = reduceList(reducedList, lesserValue, i)
    if len(reducedList) == 1:
      break
  return int(reducedList[0], 2)


def calcOxygen(data):
  return calcGeneral(data, "1", "0")


def calcScrubber(data):
  return calcGeneral(data, "0", "1")


if __name__ == "__main__":
  args = parseArgs()

  print(f"Answer: {readData(args.infile)}")