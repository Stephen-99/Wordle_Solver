import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import PlayWordleGuessEvent, ErrorOccuredEvent

from WordleLibrary.LetterColour import LetterColour
from WordleLibrary.Guess import Guess

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
    
    #Formats it to always have 1 character preceded by 1 space
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

    def SetInactive(self, guessResult: Guess):
        self.SetReadonly()
        self.UpdateColours(guessResult)

    def SetReadonly(self, isReadonly = True):
        for square in self.squares:
            square.readonly = isReadonly

    def UpdateColours(self, guessResult: Guess):
        for square in self.squares:
            print(square.value[1])

    def ValidateRow(self) -> str:
        word = ""
        for square in self.squares:
            word += square.value
        word = word.replace(" ", "")
        
        print(word)
        if len(word) != 5:
            EventSystem.EventOccured(ErrorOccuredEvent("Make sure every square has a letter"))
            return
        return word

class PlayWordleRows:
    def __init__(self):
        self.rows = [PlayWordleRow() for _ in range(6)]
        self.curRowIdx = 0
        self.rows[self.curRowIdx].SetActive()

    def SetNewCurRow(self):
        word = self.rows[self.curRowIdx].ValidateRow()
        EventSystem.EventOccured(PlayWordleGuessEvent(word))

    def UpdateActiveRow(self, guess: Guess):
        self.rows[self.curRowIdx].SetInactive(guess)

        self.curRowIdx += 1
        self.rows[self.curRowIdx].SetActive()

    def AddToBox(self, box: toga.Box):
        for row in self.rows:
            row.AddToBox(box)
    