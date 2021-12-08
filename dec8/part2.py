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
    self.wiringMap = {}
    self.digitMap = {}
    self.deduce()

  def deduce(self):
    unknown = []
    # Take care of easy ones first
    for digit in self.signals:
      wiring = frozenset(digit)
      if len(wiring) == 2:
        self.wiringMap[wiring] = 1
        self.digitMap[1] = wiring
      elif len(wiring) == 3:
        self.wiringMap[wiring] = 7
        self.digitMap[7] = wiring
      elif len(wiring) == 4:
        self.wiringMap[wiring] = 4
        self.digitMap[4] = wiring
      elif len(wiring) == 7:
        self.wiringMap[wiring] = 8
        self.digitMap[8] = wiring
      else:
        unknown.append(wiring)

    # We know that 3 is equal to 7 plus d and g
    for wiring in unknown:
      if self.digitMap[7].issubset(wiring):
        if len(wiring) == 5:
          self.wiringMap[wiring] = 3
          self.digitMap[3] = wiring
        if len(wiring) == 6 and self.digitMap[4].issubset(wiring):
          self.wiringMap[wiring] = 9
          self.digitMap[9] = wiring
    unknown.remove(self.digitMap[3])
    unknown.remove(self.digitMap[9])

    # We know that 0 is equal to 1 plus digits
    # We know the other 6 wires left is 6
    for wiring in unknown:
      if len(wiring) == 6:
        if self.digitMap[1].issubset(wiring):
          self.wiringMap[wiring] = 0
          self.digitMap[0] = wiring
        else:
          self.wiringMap[wiring] = 6
          self.digitMap[6] = wiring
    unknown.remove(self.digitMap[0])
    unknown.remove(self.digitMap[6])

    # We know that 5 is a proper subset of 6
    for wiring in unknown:
      if wiring.issubset(self.digitMap[6]):
        self.wiringMap[wiring] = 5
        self.digitMap[5] = wiring
      else:
        self.wiringMap[wiring] = 2
        self.digitMap[2] = wiring

  def getOutputValue(self):
    result = 0
    for digit in self.output:
      wiring = frozenset(digit)
      result = (result * 10) + self.wiringMap[wiring]
    return result


def puzzle(filename):
  answer = 0
  for line in open(filename, 'r'):
    leds = LEDs(line)
    result = leds.getOutputValue()
    answer += result

  return answer


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")