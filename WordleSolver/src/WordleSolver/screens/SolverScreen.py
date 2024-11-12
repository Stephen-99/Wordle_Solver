import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour

from .Screen import Screen
from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import SubmitGuessResultsEvent, ReturnToMainMenuEvent, ErrorOccuredEvent

class SolverScreen(Screen):
    def __init__(self, word="tempw"):
        super().__init__()
        self.letters = [LetterColour() for _ in range(5)]
        self.TryUpdateWord(word)

        self.solverBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))

        self.titleLabel = toga.Label("Please enter the following word as your guess\nClick the buttons to match the result :D", style=Pack(padding=(2,5), font_size=16, text_align='center'))
        self.guessInput = toga.TextInput(style=Pack(padding=(10, 50), font_weight="bold", font_size=18))

        self.letterButtonsBox = toga.Box(style=Pack(direction=ROW))
        self.submitButtonsBox = toga.Box(style=Pack(direction=ROW))
        self.userGuessButtonBox =toga.Box(style=Pack(direction=ROW))

        self.submitButton = toga.Button("Submit", on_press=self.SolverSubmitHandler, style=Pack(padding=5, font_size=12))
        self.correctButton = toga.Button("Correct Guess!", on_press=self.CorrectGuessHandler, style=Pack(padding=5, font_size=12))
        self.backButton = toga.Button("Back", on_press=self.BackButtonHandler, style=Pack(padding=5, font_size=12))
        self.userGuessButton = toga.Button("I've already made a guess", on_press=self.UserGuessButtonHandler, style=Pack(padding=5, font_size=12, flex=-1))
        
        self.eventLoop = asyncio.get_event_loop() #TODO: move to Screen

    def TryUpdateWord(self, word):
        if len(word) != 5:
            EventSystem.EventOccured(ErrorOccuredEvent("Word must be 5 letters long"))
            return False
        else:
            self.word = word
            return True

    def UpdateScreen(self):
        letterButtons  = [self.CreateLetterButton(letter, colourData) for letter, colourData in zip(self.word.upper(), self.letters)]
        self.letterButtonsBox.clear()
        [self.letterButtonsBox.add(button) for button in letterButtons]

        return self.solverBox

    def CreateScreen(self) -> toga.Box:
        letterButtons  = [self.CreateLetterButton(letter, colourData) for letter, colourData in zip(self.word.upper(), self.letters)]
        [self.letterButtonsBox.add(button) for button in letterButtons]

        #TODO: rethink this button layout a little
        self.submitButtonsBox.add(self.submitButton, self.correctButton, self.backButton)
        self.userGuessButtonBox.add(self.userGuessButton)

        self.innerBox.add(self.titleLabel, self.letterButtonsBox, self.submitButtonsBox, self.userGuessButtonBox)
        self.solverBox.add(self.innerBox)

        return self.solverBox

    def CreateLetterButton(self, letter, colourData: LetterColour):
        colourData.ResetState()
        size = 80
        button = toga.Button(letter, on_press=colourData, style=Pack(padding=5, font_weight="bold", font_size=28, width=size, height=size, color="#ffffff", background_color=colourData.colour))
        return button
    
    def SolverSubmitHandler(self, widget) -> None:
        if self.GettingUserInput():
            self.UserGuessReceived(self.guessInput.value)
        else:
            EventSystem.EventOccured(SubmitGuessResultsEvent(self.letters))
    
    def CorrectGuessHandler(self, widget) -> None:
        EventSystem.EventOccured(ReturnToMainMenuEvent())

    def BackButtonHandler(self, widget) -> None:
        if self.GettingUserInput():
            self.ReturnToResultsView()
        else:
            EventSystem.EventOccured(ReturnToMainMenuEvent())

    def GettingUserInput(self) -> bool:
        return len(self.innerBox.children) < 4 #user input is active

    def UserGuessButtonHandler(self, widget) -> None:
        self.innerBox.clear()
        self.guessInput.value = "Enter your guess"

        buttonBox = toga.Box(style=Pack(direction=ROW))
        buttonBox.add(self.submitButton, self.backButton)
        self.innerBox.add(self.guessInput, buttonBox)

    def UserGuessReceived(self, word):
        #Need to let solver know to update it's word here too. 
        #Shouldn't be done in TryUpdateWord as that is called from solver already.
        if not self.TryUpdateWord(word):
            return
        self.ReturnToResultsView()

    def ReturnToResultsView(self):
        self.innerBox.clear()
        self.submitButtonsBox.insert(0, self.submitButton)
        self.submitButtonsBox.insert(2, self.backButton)
        self.innerBox.add(self.titleLabel, self.letterButtonsBox, self.submitButtonsBox, self.userGuessButtonBox)
        self.UpdateScreen()

    async def RemoveError(self):
        self.innerBox.remove(self.errorBox)

    def ShowError(self, errorBox: toga.Box):
        self.innerBox.remove(self.errorBox)
        self.errorBox = errorBox
        self.innerBox.add(self.errorBox)
        self.SetErrorTimeout()
        return self.solverBox
    
    

