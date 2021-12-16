import argparse
import time
import re
import sys


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class Packet:

  def __init__(self, binaryString):
    self.binaryString = binaryString
    self.version = int(binaryString[0:3], 2)
    self.typeID = int(binaryString[3:6], 2)
    self.value = 0
    self.sizeBits = 0
    self.subPackets = []

    if self.typeID == 4:  # literal
      index = 6
      numberString = ''
      while binaryString[index] == '1':
        numberString += binaryString[index + 1:index + 5]
        index += 5
      numberString += binaryString[index + 1:index + 5]
      self.value = int(numberString, 2)
      self.sizeBits = index + 5
    else:  # operator
      lengthType = binaryString[6]
      print("LT", lengthType)
      if lengthType == '0':
        length = int(binaryString[7:22], 2)
        index = 22
        totalParsed = 0
        while totalParsed < length:
          newPacket = Packet(binaryString[index:])
          totalParsed += newPacket.sizeBits
          index += newPacket.sizeBits
          self.subPackets.append(newPacket)
        self.sizeBits = index
      else:
        numPackets = int(binaryString[7:18], 2)
        index = 18
        for _ in range(numPackets):
          newPacket = Packet(binaryString[index:])
          index += newPacket.sizeBits
          self.subPackets.append(newPacket)
        self.sizeBits = index

  def sumVersionNumbers(self):
    result = self.version
    for packet in self.subPackets:
      result += packet.sumVersionNumbers()
    return result

  def __repr__(self):
    result = f'({self.binaryString[:self.sizeBits]}) V:{self.version} T:{self.typeID} - {self.value}: {self.subPackets}'
    return result


class BITS:

  def __init__(self, str):
    self.binary = ''

    for ch in str:
      self.binary += f'{int(ch, 16):0>4b}'
    self.packet = Packet(self.binary)
    print(self.packet)
    print("Leftovers:", self.binary[self.packet.sizeBits:])

  def sumVersionNumbers(self):
    return self.packet.sumVersionNumbers()


def puzzle(filename):
  for line in open(filename, 'r'):
    bits = BITS(line)
    return bits.sumVersionNumbers()


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")