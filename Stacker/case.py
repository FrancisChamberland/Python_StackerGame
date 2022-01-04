from enum import  Enum
from constants import *

class CaseType(Enum):
    Empty = 0
    Filled = 1

class Case:
    def __init__(self, window, row, col, type):
        self.row = row
        self.col = col
        self.type = type
        self.window = window
        self.color = None
        self.updateColor()

    def updateColor(self):
        if (self.type == CaseType.Empty):
            self.color = self.window.backgroundColor
        elif (self.type == CaseType.Filled):
            self.color = self.window.primaryColor

    def setType(self, type):
        self.type = type
        self.updateColor()

    def isFilled(self):
        return self.type == CaseType.Filled