from pygame import *
from numpy import *
from case import *

class Window:
    def __init__(self, width, height, title, caseSize, backgroundColor, primaryColor, secondaryColor=None):
        self.width = width
        self.height = height
        self.title = title
        self.backgroundColor = backgroundColor
        self.primaryColor = primaryColor
        self.secondaryColor = secondaryColor
        self.screen = None
        self.caseSize = caseSize
        self.rowCount = int(height / self.caseSize)
        self.colCount = int(width / self.caseSize)
        self.array = self.createArray(self.rowCount, self.colCount)
        self.fillArray(array)

    def display(self):
        display.set_caption(self.title)
        self.screen = display.set_mode((self.width, self.height))
        self.screen.fill(self.backgroundColor)
        display.flip()

    def createArray(self, rowCount, colCount):
        return zeros((rowCount, colCount), dtype="object")

    def fillArray(self, array):
        for r in range(self.rowCount):
            for c in range(self.colCount):
                self.array[r][c] = Case(self, r, c, CaseType.Empty)

    def updateCase(self, case):
        top = case.row * self.caseSize
        left = case.col * self.caseSize
        height, width = (self.caseSize, self.caseSize)
        draw.rect(self.screen, case.color, (left, top, width, height))

    def update(self):
        for r in range(self.rowCount):
            for c in range(self.colCount):
                indexCase = self.array[r][c]
                self.updateCase(indexCase)

        display.flip()