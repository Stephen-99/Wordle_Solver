#This will use s imilar section to the Solver screen. But not buttons. So don't actually create a reausable fragment type idea
#TODO:
#COMBINE WITH GETGUESSFROMUSER
    #We want to have a stacked list of words like in woordle itself.
    #bottom most one they can enter text in.
        #have it fixed with the 6 rows, just keep the last ones blank for now
    #After a guess the next row will become active, and the one above will get colours.

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour

from .Screen import Screen

#TODO add keyboard.
    #Should auto pop up, but can add highlighting to show which letters are unavailable or should be used.
class PlayWordleScreen(Screen):
    def __init__(self):
        self.outerBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.rows = [self.CreateRow() for _ in range(6)]
        self.curRow = self.rows[0]
        self.curRowIdx = 0 #TODO: these 2 things make me thing I need a small class for rows.

    def CreateScreen(self):
        [self.innerBox.add(row) for row in self.rows]
        #self.innerBox.add("SOME TEXT")
        self.outerBox.add(self.innerBox)

    
    def UpdateScreen(self):
        return self.outerBox

    def CreateRow(self):
        squares = [self.CreateTextSquare() for _ in range(5)]
        row = toga.Box(style=Pack(direction=ROW))
        [row.add(square) for square in squares]

        return row
    
    def CreateTextSquare(self):
        size = 70
        return toga.TextInput(style=Pack(padding=5, font_weight="bold", font_size=size//2, width=size, height=size, color="#ffffff", background_color=LetterColour.gray))