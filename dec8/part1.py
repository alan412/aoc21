import argparse
import time


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class LEDs():

  def __init__(self, line):
    (i, o) = line.split('|')
    self.signals = i.split()
    self.output = o.split()

  def countEasy(self):
    # 2 segments = 1
    # 3 segments = 7
    # 4 segments = 4
    # 8 segmenets = 8
    easy = [2, 3, 4, 7]

    easyCount = 0
    for digit in self.output:
      if len(digit) in easy:
        easyCount += 1
    return easyCount


def puzzle(filename):
  totalEasy = 0
  for line in open(filename, 'r'):
    leds = LEDs(line)
    totalEasy += leds.countEasy()

  return totalEasy


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")