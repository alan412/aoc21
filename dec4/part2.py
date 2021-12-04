import argparse
import re


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input file')
  return parser.parse_args()


class BingoSquare:

  def __init__(self, number, row, col):
    self.number = number
    self.row = row
    self.col = col

  def __repr__(self):
    return f"{self.row} {self.col}: {self.number}"


class Bingo:

  def __init__(self, row):
    self.marked = []
    self.unmarked = {}
    self.addRow(row, 0)
    self.markedRows = [0] * 5
    self.markedCols = [0] * 5

  def addRow(self, row, rowNum):
    col = 0
    for value in row.split():
      self.unmarked[value] = BingoSquare(int(value), rowNum, col)
      col += 1

  def markNumber(self, number):
    if number in self.unmarked:
      newOne = self.unmarked.pop(number)
      self.marked.append(newOne)
      self.markedRows[newOne.row] += 1
      self.markedCols[newOne.col] += 1
      return self.isWinner()
    return False

  def isWinner(self):
    if len(self.marked) < 5:
      return False
    for i in range(5):
      if self.markedRows[i] == 5:
        return True
      if self.markedCols[i] == 5:
        return True

  def getUnmarkedSum(self):
    sum = 0
    for square in self.unmarked.values():
      sum += square.number
    return sum


def puzzle(filename):
  bingoNumbers = []
  bingoCards = []
  currentCard = None
  rowNum = 0

  for line in open(filename, 'r'):
    if not bingoNumbers:
      bingoNumbers = line.split(',')
    elif line.strip():
      if not currentCard:
        currentCard = Bingo(line)
        bingoCards.append(currentCard)
        rowNum = 1
      else:
        currentCard.addRow(line, rowNum)
        rowNum += 1
    else:
      currentCard = None
  for number in bingoNumbers:
    if len(bingoCards) > 1:
      bingoCards = [card for card in bingoCards if not card.markNumber(number)]
    else:
      card = bingoCards[0]
      winner = card.markNumber(number)
      if winner:
        print(f"Last number: {number} {card.getUnmarkedSum()}")
        return int(number) * card.getUnmarkedSum()

  print("No winner")
  return 0


if __name__ == "__main__":
  args = parseArgs()

  print(f"Answer: {puzzle(args.infile)}")