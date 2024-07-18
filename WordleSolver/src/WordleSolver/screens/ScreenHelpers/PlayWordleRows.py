import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour
from WordleLibrary.Guess import Guess

#TODO: Should these be backed by guess objects?
class PlayWordleRow:
    SQUARESIZE = 70
    ACTIVECOLOUR = "#848484"
    
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
        
        widget.value = " " + widget.value.lower()

    def AddToBox(self, box: toga.Box):
        box.add(self.box)

    def SetActive(self):
        self.SetReadonly(isReadonly = False)
        for square in self.squares:
            square.style.background_color = self.ACTIVECOLOUR

    def SetInactive(self):
        self.SetReadonly()
        #Update to colours based on correctness of the thingo. Will need to call the solver
            #Have a separate one for playing.

    def SetReadonly(self, isReadonly = True):
        for square in self.squares:
            square.readonly = isReadonly

    def UpdateColours(self, guessResult: Guess):
        raise NotImplementedError()

class PlayWordleRows:
    def __init__(self):
        self.rows = [PlayWordleRow() for _ in range(6)]
        self.curRowIdx = 0
        self.rows[self.curRowIdx].SetActive()

    def setNewCurRow(self):
        #set these to readonly and change the colours accordingly
        self.rows[self.curRowIdx].SetInactive()
        #row.updateColours(guessResult)

        self.curRowIdx += 1
        self.rows[self.curRowIdx].SetActive()
        #set these to not be readonly and make the colours ligher to show it's active.

    #~~~~~~~~~~~~~TODO: setup a listener and event to manage this (trigger on submit button)~~~~~~~~~~~~~~~~~~~~~~~~

    def AddToBox(self, box: toga.Box):
        for row in self.rows:
            row.AddToBox(box)
    