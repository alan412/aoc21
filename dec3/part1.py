import argparse
import re


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def calcGamma(numOnes, numZeros):
  gamma = 0
  for i in range(len(numOnes)):
    gamma = (gamma << 1) | (1 if numOnes[i] > numZeros[i] else 0)
  return gamma


def readData(filename):
  numOnes = []
  numZeros = []
  numValues = 0
  for line in open(filename, 'r'):
    if numValues == 0:
      numValues = len(line) - 1
      numOnes = [0] * numValues
      numZeros = [0] * numValues
    for i in range(numValues):
      if line[i] == '1':
        numOnes[i] += 1
      else:
        numZeros[i] += 1

  gamma = calcGamma(numOnes, numZeros)
  epsilon = ((2**numValues) - 1) - gamma
  print(f'{gamma} {epsilon}')
  return gamma * epsilon


if __name__ == "__main__":
  args = parseArgs()

  print(f"Answer: {readData(args.infile)}")