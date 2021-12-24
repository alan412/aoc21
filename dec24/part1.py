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
    self.registerSet = set(self.registers.keys())

  def addInstruction(self, line):
    parts = line.strip().split()
    if len(parts) == 2:
      self.instructions.append((parts[0], parts[1], None))
    else:
      print(parts)
      if parts[2] in self.registerSet:
        self.instructions.append((parts[0], parts[1], parts[2]))
      else:
        self.instructions.append((parts[0], parts[1], int(parts[2])))

  def solve(self, minimize=False):
    pairs = [(self.instructions[i * 18 + 5][2],
              self.instructions[i * 18 + 15][2]) for i in range(14)]
    stack = []
    links = {}
    for i, (a, b) in enumerate(pairs):
      if a > 0:
        stack.append((i, b))
      else:
        j, bj = stack.pop()
        links[i] = (j, bj + a)
    assignments = {}
    for i, (j, delta) in links.items():
      assignments[i] = max(1, 1 + delta) if minimize else min(9, 9 + delta)
      assignments[j] = max(1, 1 - delta) if minimize else min(9, 9 - delta)
    result = "".join(str(assignments[x]) for x in range(14))
    return result

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
    for pc, instruction in enumerate(self.instructions):
      result += f'\n{pc:03} {instruction}'
    return result


def puzzle(filename):
  alu = ALU()

  for i, line in enumerate(open(filename, 'r')):
    alu.addInstruction(line)

  print(alu)

  return alu.solve(minimize=True)


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")