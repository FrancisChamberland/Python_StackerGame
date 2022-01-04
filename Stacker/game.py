from case import *
import sys
import random

class Direction(Enum):
    Left = 1
    Right = 2

class Game:
    def __init__(self, window):
        self.window = window
        self.array = self.window.array
        self.level = 1
        self.maxLevel = len(self.array)
        self.speed = 0
        self.activeCasesCount = 3
        self.currentRow = None
        self.currentDirection = Direction.Right
        self.delayActive = 0
        self.delayFalling = 0
        self.stopped = True
        self.updateCurrentRow()

    def start(self):
        self.spawnActiveCases()
        self.startMovingCases()

    def fillCase(self, case):
        case.setType(CaseType.Filled)

    def emptyCase (self, case):
        case.setType(CaseType.Empty)

    def moveCaseLeft(self, case):
        if case.col - 1 >= 0:
            oldCase = self.getCase(case.row, case.col)
            newCase = self.getCase(case.row, case.col - 1)
            self.emptyCase(oldCase)
            self.fillCase(newCase)

    def moveCaseRight(self, case):
        if case.col + 1 < len(self.array[0]):
            oldCase = self.getCase(case.row, case.col)
            newCase = self.getCase(case.row, case.col + 1)
            self.emptyCase(oldCase)
            self.fillCase(newCase)

    def moveCaseDown(self, case):
        if case.row + 1 < len(self.array):
            oldCase = self.getCase(case.row, case.col)
            newCase = self.getCase(case.row + 1, case.col)
            self.emptyCase(oldCase)
            self.fillCase(newCase)

    def levelUp(self):
        self.level += 1
        self.speed += 5
        self.delayActive = 0
        self.updateCurrentRow()
        self.spawnActiveCases()
        self.startMovingCases()

    def updateCurrentRow(self):
        self.currentRow = len(self.array) - self.level

    def spawnActiveCases(self):
        spawnSide = random.randrange(1, 3)
        case = None
        for i in range(self.activeCasesCount):
            if spawnSide == 1:
                case = self.getCase(self.currentRow, len(self.array[0]) - 1 - i)
            elif spawnSide == 2:
                case = self.getCase(self.currentRow, i)
            self.fillCase(case)

    def getActiveCases(self):
        cases = []
        for i in range(len(self.array[0])):
            case = self.getCase(self.currentRow, i)
            if case.isFilled():
                cases.append(case)
        return cases

    def moveActiveCasesLeft(self):
        cases = self.getActiveCases()
        for case in cases:
            self.moveCaseLeft(case)

    def moveActiveCasesRight(self):
        cases = self.getActiveCases()
        for case in reversed(cases):
            self.moveCaseRight(case)

    def changeDirection(self):
        if self.currentDirection == Direction.Left:
            self.currentDirection = Direction.Right
        elif self.currentDirection == Direction.Right:
            self.currentDirection = Direction.Left

    def mustChangeDirection(self):
        cases = self.getActiveCases()
        if self.currentDirection == Direction.Left:
            return cases[0].col - 1 < 0
        elif self.currentDirection == Direction.Right:
            return cases[-1].col + 1 == len(self.array[0])

    def moveCases(self):
        self.moveActiveCases()
        self.moveFallingCases()

    def moveActiveCases(self):
        if self.stopped == False:
            if self.delayActive == 100 - self.speed:
                self.delayActive = 0
                if self.mustChangeDirection():
                    self.changeDirection()
                if self.currentDirection == Direction.Left:
                    self.moveActiveCasesLeft()
                elif self.currentDirection == Direction.Right:
                    self.moveActiveCasesRight()
            else:
                self.delayActive += 1

    def moveFallingCases(self):
        if self.delayFalling == 400:
            self.delayFalling = 0
            for case in self.getAllFilledCases():
                if case.row != self.currentRow and self.caseUnderIsEmpty(case):
                    self.moveCaseDown(case)
        else:
            self.delayFalling += 1

    def stopMovingCases(self):
        self.stopped = True

    def startMovingCases(self):
        self.stopped = False

    def updateActiveCases(self):
        cases = self.getActiveCases()
        for case in cases:
            if self.caseUnderIsEmpty(case):
                self.activeCasesCount -= 1

    def canLevelUp(self):
        if self.level == 1: return True
        if self.level == self.maxLevel: return False
        return self.activeCasesCount > 0

    def gameOver(self):
        print(f"Game Over - You reached level {self.level - 1}")
        sys.exit(0)

    def stack(self):
        self.stopMovingCases()
        self.updateActiveCases()
        if self.canLevelUp():
            self.levelUp()
        else:
            self.gameOver()

    def getCase(self, row, col):
        return self.array[row][col]

    def getAllFilledCases(self):
        cases = []
        for r in range(len(self.array)):
            for c in range(len(self.array[0])):
                case = self.getCase(r, c)
                if case.isFilled():
                    cases.append(case)
        return cases

    def caseUnderIsEmpty(self, case):
        if case.row + 1 >= len(self.array): return False
        caseUnder = self.getCase(case.row + 1, case.col)
        return caseUnder.isFilled() is False
