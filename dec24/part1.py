import argparse
import time
import re
import sys
from collections import defaultdict
from functools import cache
from enum import Enum


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class ALU():

  def __init__(self):
    self.instructions = []
    self.registers = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

  def addInstruction(self, line):
    parts = line.strip().split()
    if len(parts) == 2:
      self.instructions.append((parts[0], parts[1], None))
    else:
      self.instructions.append((parts[0], parts[1], parts[2]))

  def getNextModelNumber(self, currModelNum):
    if currModelNum == None:
      return '9' * 14

    numModel = int(currModelNum)
    while True:
      numModel -= 1
      strModel = str(numModel)
      if strModel.count('0') == 0:
        return strModel

  def solve(self):
    failed = set()

    modelNumber = None
    found = False
    while not found:
      modelNumber = self.getNextModelNumber(modelNumber)

      skip = False
      for failure in failed:
        if modelNumber.startswith(failure):  # no need to try it will fail
          skip = True
          break
      if not skip:
        print('Trying', modelNumber, 'failures so far:', failed)
        failed = self.execute(modelNumber)
        if failed:
          set.add(failed)
        elif self.registers['z'] == 0:
          found = True
          return modelNumber

  def execute(self, inputValue):
    remainingInput = inputValue
    usedInput = ''

    for inst in self.instructions:
      op = inst[0]
      param1 = self.registers[inst[1]]
      if inst[2] in self.registers:
        param2 = self.registers[inst[2]]
      elif inst[2]:
        param2 = int(inst[2])
      else:
        param2 = None

      if op == 'inp':
        self.registers[inst[1]] = int(remainingInput[0])
        usedInput += remainingInput[0]
        remainingInput = remainingInput[1:]
      elif op == 'add':
        self.registers[inst[1]] = param1 + param2
      elif op == 'mul':
        self.registers[inst[1]] = param1 * param2
      elif op == 'div':
        if param2 == 0:
          return usedInput
        self.registers[inst[1]] = param1 // param2
      elif op == 'mod':
        if param1 < 0 or param2 <= 0:
          return usedInput
        self.registers[inst[1]] = param1 % param2
      elif op == 'eql':
        self.registers[inst[1]] = 1 if (param1 == param2) else 0

    return ''

  def __repr__(self):
    result = f'{self.registers} '
    for instruction in self.instructions:
      result += f'\n{instruction}'
    return result


def puzzle(filename):
  alu = ALU()

  for i, line in enumerate(open(filename, 'r')):
    alu.addInstruction(line)

  return alu.solve()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")