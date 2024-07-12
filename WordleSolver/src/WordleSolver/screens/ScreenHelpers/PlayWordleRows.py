import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour
from WordleLibrary.Guess import Guess

class PlayWordleRow:
    SQUARESIZE = 70
    def __init__(self):
        self.squares = [self.CreateTextSquare() for _ in range(5)]
        self.box = toga.Box(style=Pack(direction=ROW))
        [self.box.add(square) for square in self.squares]

    def CreateTextSquare(self):
        return toga.TextInput(style=Pack(padding=5, font_weight="bold", font_size=self.SQUARESIZE//2, width=self.SQUARESIZE-10, color="#ffffff", background_color=LetterColour.gray),
                              on_change=self.FormatTextInput, readonly=True)
    
    def FormatTextInput(self, widget: toga.TextInput):
        if widget.value and widget.value[0] == " ":
            if len(widget.value) > 2:
                widget.value = widget.value[0:2]
            return
        
        widget.value = " " + widget.value

    def AddToBox(self, box: toga.Box):
        box.add(self.box)

    def SetReadonly(self, isReadonly = True):
        for square in self.squares:
            square.readonly = isReadonly

    def UpdateColours(self, guessResult: Guess):
        raise NotImplementedError()

class PlayWordleRows:
    def __init__(self):
        self.rows = [PlayWordleRow() for _ in range(6)]
        self.curRowIdx = 0
        self.setNewCurRow() #Can't do this sine it will increment curRowIdx. and setting it to -1 will give indexOutOf bounds

    def rowSetup(self):
        pass
        #To complete the work of setNewCurRow but properly for the initial setup

    def setNewCurRow(self):
        #INSTEAD OF THIS READONLY CALL HAVE A SET INACTIVE AND SET ACTIVE
        
        #set these to readonly and change the colours accordingly
        self.rows[self.curRowIdx].SetReadonly()
        #row.updateColours(guessResult)

        self.curRowIdx += 1
        self.rows[self.curRowIdx].SetReadonly(isReadonly = False)
        #set these to not be readonly and make the colours ligher to show it's active.


    def AddToBox(self, box: toga.Box):
        for row in self.rows:
            row.AddToBox(box)
    