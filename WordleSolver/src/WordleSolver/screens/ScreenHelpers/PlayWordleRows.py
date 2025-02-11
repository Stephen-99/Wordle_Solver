import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import PlayWordleGuessEvent, ErrorOccuredEvent, PlayWordleUpdatedEvent

from WordleLibrary.LetterColour import LetterColour
from WordleLibrary.Guess import Guess

#WORK TODO, shouldn't scale to be this small... Also need to scale height not just width. MOREOVER,
#Padding also needs to scale...
class PlayWordleRow:
    SQUARESIZE = 80 
    ACTIVECOLOUR = "#848484"
    
    def __init__(self, screenWidth):
        self.scale = screenWidth / 549
        self.squareSize = self.ScaleValue(self.SQUARESIZE)
        self.squareWithFocusIdx = -1 #No square starts with the focus
        self.squares = [self.CreateTextSquare() for _ in range(5)]
        self.box = toga.Box(style=Pack(direction=ROW))
        [self.box.add(square) for square in self.squares]

    def Reset(self):
        for square in self.squares:
            square.value = ""
            square.readonly = True
            square.style.background_color = LetterColour.gray

    def ScaleValue(self, value):
        return int(value * self.scale) + 1 #Duplicated in Screen.py and Errorhandler.py

    def CreateTextSquare(self):
        return toga.TextInput(style=Pack(padding=self.ScaleValue(5), font_weight="bold", font_size=self.squareSize//2, width=self.squareSize, height=self.squareSize + 10, color="#ffffff", background_color=LetterColour.gray),
                              on_change=self.FormatTextInput, on_gain_focus=self.FocusWasSetToSquare, readonly=True)
    
    #Formats it to always have 1 character preceded by 1 space
    def FormatTextInput(self, widget: toga.TextInput):
        if not widget.value:
            return
        if widget.value[0] == " " and widget.value.upper() == widget.value and len(widget.value) < 3:
            return #Return when already in the right format to avoid infinite recursion
        
        valToSet = widget.value.upper()        
        if widget.value[0] != " ":
            valToSet = " " + valToSet
        if len(valToSet) > 2:
            valToSet = valToSet[0:2]
        
        widget.value = valToSet
        self.MoveFocusToNextSquare()

    def MoveFocusToNextSquare(self):
        #This causes an error on the last idx atm
        if self.squareWithFocusIdx < len(self.squares)-1:
            self.squareWithFocusIdx += 1
            self.squares[self.squareWithFocusIdx].focus()

    def FocusWasSetToSquare(self, widget: toga.TextInput):
        for ii, square in enumerate(self.squares):
            if square == widget:
                self.squareWithFocusIdx = ii
                break

    def AddToBox(self, box: toga.Box):
        self.box.clear()
        for square in self.squares:
            self.box.add(square)
        box.add(self.box)

    def SquaresUpdated(self):
        self.box.clear()
        for square in self.squares:
            self.box.add(square)

    def SetActive(self):
        self.SetReadonly(isReadonly = False)
        for square in self.squares:
            square.style.background_color = self.ACTIVECOLOUR
        self.SquaresUpdated()

    def SetInactive(self, guessResult: Guess):
        self.SetReadonly()
        self.UpdateColours(guessResult)
        self.SquaresUpdated()

    def SetReadonly(self, isReadonly = True):
        for square in self.squares:
            square.readonly = isReadonly

    def UpdateColours(self, guessResult: Guess):
        for ii in range(5):
            self.squares[ii].style.background_color = self.GetColour(guessResult, ii)
    
    def GetColour(self, guess: Guess, idx: int):
        if guess.correct[idx]:
            return LetterColour.green
        if guess.misplaced[idx]:
            return LetterColour.yellow
        return LetterColour.gray

    def ValidateRow(self) -> str:
        word = ""
        for square in self.squares:
            word += square.value
        word = word.replace(" ", "")
        
        if len(word) != 5:
            EventSystem.EventOccured(ErrorOccuredEvent("Make sure every square has a letter"))
            return
        return word.lower()

class PlayWordleRows:
    def __init__(self, screenWidth):
        self.rows = [PlayWordleRow(screenWidth) for _ in range(6)]
        self.curRowIdx = 0
        self.rows[self.curRowIdx].SetActive()

    def Reset(self):
        self.curRowIdx = 0
        for row in self.rows:
            row.Reset()
        self.rows[self.curRowIdx].SetActive()

    def SetNewCurRow(self):
        word = self.rows[self.curRowIdx].ValidateRow()
        if word:
            EventSystem.EventOccured(PlayWordleGuessEvent(word))

    def UpdateActiveRow(self, guess: Guess):
        self.rows[self.curRowIdx].SetInactive(guess)
        self.curRowIdx += 1
        self.rows[self.curRowIdx].SetActive()
        EventSystem.EventOccured(PlayWordleUpdatedEvent()) 

    def AddToBox(self, box: toga.Box):
        for row in self.rows:
            row.AddToBox(box)
    