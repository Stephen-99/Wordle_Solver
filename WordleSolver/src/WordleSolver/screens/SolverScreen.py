import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour
from WordleSolver.screens.Screen import Screen

class SolverScreen(Screen):
    def __init__(self, word):
        self.letters = [LetterColour() for _ in range(5)]
        self.UpdateWord(word)

        self.solverBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))

        self.titleLabel = toga.Label("Please enter the following word as your guess\nClick the buttons to match the result :D", style=Pack(padding=(2,5), font_size=16, text_align='center'))
        self.letterButtonsBox = toga.Box(style=Pack(direction=ROW))
        self.submitButtonsBox = toga.Box(style=Pack(direction=ROW))

        #TODO add integration with the wordle library here so that it can actually use the solver.
        self.submitButton = toga.Button("Submit", on_press=self.SolverSubmitHandler, style=Pack(padding=5, font_size=12))
        self.correctButton = toga.Button("Correct Guess!", style=Pack(padding=5, font_size=12))


    def UpdateWord(self, word):
        if len(word) != 5:
            raise AttributeError("Word must be 5 letters long")
        self.word = word

    def UpdateScreen(self):
        letterButtons  = [self.CreateLetterButton(letter, colourData) for letter, colourData in zip(self.word.upper(), self.letters)]
        self.letterButtonsBox.clear()
        [self.letterButtonsBox.add(button) for button in letterButtons]
        
        #TODO: test if these will be needed or not.
        #self.innerBox.refresh()
        #self.solverBox.refresh()

        return self.solverBox


    def CreateScreen(self) -> toga.Box:
        letterButtons  = [self.CreateLetterButton(letter, colourData) for letter, colourData in zip(self.word.upper(), self.letters)]
        [self.letterButtonsBox.add(button) for button in letterButtons]

        self.submitButtonsBox.add(self.submitButton, self.correctButton)

        self.innerBox.add(self.titleLabel, self.letterButtonsBox, self.submitButtonsBox)
        self.solverBox.add(self.innerBox)

        return self.solverBox

    def CreateLetterButton(self, letter, colourData: LetterColour):
        colourData.ResetState()
        size = 100
        button = toga.Button(letter, on_press=colourData, style=Pack(padding=5, font_weight="bold", font_size=32, width=size, height=size, color="#ffffff", background_color=colourData.colour))
        #Can't seem to get button border to change color... :(
        return button
    
    def SolverSubmitHandler(self, widget) -> None:
        #Somehow need the state of the letter buttons to pass on. Will need to re-think how this class is structured.
        #TODO: rethink about how the whole app is structured. This file particularly. Should there be separate classes fro solver and main screens?
            #Each screen should have it's own class with it's own set of variables and functions.
            #May need some Inheritance hierachy So can use all the screens interchangeably.
        #if it returns none, don't set solver screen, go to main.
        self.SetSolverScreen(self.solver.ProcessGuessResults(self.letters))
        #HMM, will need some sort of cool logic pattern to be able to pass on back to the main screen when it's time to change screens
            #Some kind of observer type pattern mayhaps.
            #don't want to too tightly couple the screens. This screen should call app to let it know it's finished. App can decide to show main screen.

