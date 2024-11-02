import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour

from .Screen import Screen
from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import SubmitGuessResultsEvent, ReturnToMainMenuEvent

class SolverScreen(Screen):
    def __init__(self, word="tempw"):
        super().__init__()
        self.letters = [LetterColour() for _ in range(5)]
        self.UpdateWord(word)

        self.solverBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))

        self.titleLabel = toga.Label("Please enter the following word as your guess\nClick the buttons to match the result :D", style=Pack(padding=(2,5), font_size=16, text_align='center'))
        self.letterButtonsBox = toga.Box(style=Pack(direction=ROW))
        self.submitButtonsBox = toga.Box(style=Pack(direction=ROW))
        self.userGuessBox =toga.Box(style=Pack(direction=ROW))

        self.submitButton = toga.Button("Submit", on_press=self.SolverSubmitHandler, style=Pack(padding=5, font_size=12))
        self.correctButton = toga.Button("Correct Guess!", on_press=self.CorrectGuessHandler, style=Pack(padding=5, font_size=12))
        self.backButton = toga.Button("Back", on_press=self.BackButtonHandler, style=Pack(padding=5, font_size=12))
        self.userGuessButton = toga.Button("I've already made a guess", on_press=self.UserGuessButtonHandler, style=Pack(padding=5, font_size=12, flex=-1))
        
        self.eventLoop = asyncio.get_event_loop() #TODO: move to Screen

    def UpdateWord(self, word):
        if len(word) != 5:
            raise AttributeError("Word must be 5 letters long")
        self.word = word

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
        self.userGuessBox.add(self.userGuessButton)

        self.innerBox.add(self.titleLabel, self.letterButtonsBox, self.submitButtonsBox, self.userGuessBox)
        self.solverBox.add(self.innerBox)

        return self.solverBox

    def CreateLetterButton(self, letter, colourData: LetterColour):
        colourData.ResetState()
        size = 80
        button = toga.Button(letter, on_press=colourData, style=Pack(padding=5, font_weight="bold", font_size=28, width=size, height=size, color="#ffffff", background_color=colourData.colour))
        return button
    
    def SolverSubmitHandler(self, widget) -> None:
        EventSystem.EventOccured(SubmitGuessResultsEvent(self.letters))
    
    def CorrectGuessHandler(self, widget) -> None:
        EventSystem.EventOccured(ReturnToMainMenuEvent())

    def BackButtonHandler(self, widget) -> None:
        EventSystem.EventOccured(ReturnToMainMenuEvent())

    def UserGuessButtonHandler(self, widget) -> None:
        #probably want anothe box for this and then can set it to invisible
        self.titleLabel.style.visibility = "hidden" #This works. It just leaves the space empty though.
                                                    #Might need to make a func to add and remove the bits instead
        self.submitButtonsBox.style.visibility = "hidden" #may actually want the back and submit button here, but will have to have a check in the handlers to handle ti slightly differently
        self.letterButtonsBox.style.visibility = "hidden"
        self.innerBox.insert(1, toga.TextInput(value="Enter your guess", style=Pack(padding=(10, 50), font_weight="bold", font_size=18)))

        #And an ok button.
        #After they hit ok, validate inpout is 5 letters (No other checks)
        #Then remove this text input and update the letter buttons.

        #Could also hide the letter buttons while all this is going on.
            #As well as the submit and correct guess buttons

    async def RemoveError(self):
        self.innerBox.remove(self.errorBox)

    def ShowError(self, errorBox: toga.Box):
        self.innerBox.remove(self.errorBox)
        self.errorBox = errorBox
        self.innerBox.add(self.errorBox)
        self.SetErrorTimeout()
        return self.solverBox
    
    

