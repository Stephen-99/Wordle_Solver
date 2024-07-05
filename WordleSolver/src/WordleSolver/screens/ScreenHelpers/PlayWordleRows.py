import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour

class PlayWordleRows:
    def __init__(self):
        self.rows = [self.CreateRow() for _ in range(6)]
        self.curRow = self.rows[0]
        self.curRowIdx = 0 #TODO: these 2 things make me thing I need a small class for rows.

    def CreateRow(self):
        squares = [self.CreateTextSquare() for _ in range(5)]
        row = toga.Box(style=Pack(direction=ROW))
        [row.add(square) for square in squares]

        return row
    
    def CreateTextSquare(self):
        size = 70
        return toga.TextInput(style=Pack(padding=5, font_weight="bold", font_size=size//2, width=size-10, color="#ffffff", background_color=LetterColour.gray),
                              on_change=self.FormatTextInput)
    
    
    def FormatTextInput(self, widget: toga.TextInput):
        if widget.value and widget.value[0] == " ":
            if len(widget.value) > 2:
                widget.value = widget.value[0:2]
            return
        
        widget.value = " " + widget.value