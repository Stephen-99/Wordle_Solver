import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour


#TODO create another class for a single row. Keep it in this file.
class PlayWordleRows:
    def __init__(self):
        self.rows = [self.CreateRow() for _ in range(6)]
        self.curRowIdx = 0
        self.setNewCurRow() #Can't do this sine it will increment curRowIdx. and setting it to -1 will give indexOutOf bounds

    def rowSetup(self):
        pass
        #To complete the work of setNewCurRow but properly for the initial setup

    def setNewCurRow(self):
        self.rows[self.curRowIdx] #set these to readonly and change the colours accordingly
        self.curRowIdx += 1
        self.rows[self.curRowIdx] #set these to not be readonly and make the colours ligher to show it's active.

    def CreateRow(self):
        squares = [self.CreateTextSquare() for _ in range(5)]
        row = toga.Box(style=Pack(direction=ROW))
        [row.add(square) for square in squares]

        return row
    
    def CreateTextSquare(self):
        size = 70
        return toga.TextInput(style=Pack(padding=5, font_weight="bold", font_size=size//2, width=size-10, color="#ffffff", background_color=LetterColour.gray),
                              on_change=self.FormatTextInput, readonly=True)
    
    
    def FormatTextInput(self, widget: toga.TextInput):
        if widget.value and widget.value[0] == " ":
            if len(widget.value) > 2:
                widget.value = widget.value[0:2]
            return
        
        widget.value = " " + widget.value

    def AddToBox(self, box: toga.Box):
        for row in self.rows:
            box.add(row)