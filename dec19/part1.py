import argparse
import time
import re
import sys


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


def get_rotations(x, y, z):
  return [
      (x, y, z),
      (-y, x, z),
      (-x, -y, z),
      (y, -x, z),
  ]


def get_z_orientations(x, y, z):
  return [
      (x, y, z),
      (x, z, -y),
      (x, -y, -z),
      (x, -z, y),
      (-z, y, x),
      (z, y, -x),
  ]


def get_orientations(x, y, z):
  for x0, y0, z0 in get_z_orientations(x, y, z):
    yield from get_rotations(x0, y0, z0)


class Scanner():

  def __init__(self, number):
    self.number = number
    self.position = None
    self.orientations = [[] for _ in range(24)]
    self.fixedBeacons = None

  def addBeacon(self, x, y, z):
    for p, pos in enumerate(get_orientations(x, y, z)):
      self.orientations[p].append(pos)

  def findPairs(self, scanners):
    if self.fixedBeacons:
      return
    for scanner in scanners:
      if not scanner.fixedBeacons:
        continue
      if self.findOverlap(scanner):
        return

  def findOverlap(self, other):
    for orientation in self.orientations:
      for fx, fy, fz in other.fixedBeacons:
        for bx, by, bz in orientation:
          dx, dy, dz = (fx - bx, fy - by, fz - bz)
          shiftedBeacons = {(x + dx, y + dy, z + dz) for x, y, z in orientation}
          common_beacons = shiftedBeacons & other.fixedBeacons
          if len(common_beacons) >= 12:
            self.fixedBeacons = shiftedBeacons
            self.pos = (dx, dy, dz)
            return True
    return False

  def distanceTo(self, other):
    x, y, z = self.pos
    ox, oy, oz = other.pos
    return abs(ox - x) + abs(oy - y) + abs(oz - z)

  def __repr__(self):
    return f"Scanner {self.number}"


patternScanner = re.compile('--- scanner (\d+) ---')
patternBeacon = re.compile('(-?\d+),(-?\d+),(-?\d+)')


def puzzle(filename):
  currScanner = None
  scanners = []
  for line in open(filename, 'r'):
    m = re.match(patternScanner, line)
    if m:
      currScanner = Scanner(int(m.group(1)))
      scanners.append(currScanner)
    else:
      m = re.match(patternBeacon, line)
      if m:
        currScanner.addBeacon(int(m.group(1)), int(m.group(2)), int(m.group(3)))

  firstScanner = scanners[0]
  firstScanner.fixedBeacons = set(firstScanner.orientations[0])
  firstScanner.pos = (0, 0, 0)

  while len([scanner for scanner in scanners if not scanner.fixedBeacons]):
    for scanner in scanners:
      scanner.findPairs(scanners)
  beacons = set()
  for scanner in scanners:
    beacons |= scanner.fixedBeacons

  print("Num Beacons", len(beacons))
  maxDistance = 0
  for aScanner in scanners:
    for bScanner in scanners:
      if aScanner != bScanner:
        distance = aScanner.distanceTo(bScanner)
        if distance > maxDistance:
          maxDistance = distance

  return maxDistance


if __name__ == "__main__":
  args = parseArgs()

  startTime = time.time()
  answer = puzzle(args.infile)
  endTime = time.time()

  print(f"Answer: {answer}\nTook: {endTime-startTime}")