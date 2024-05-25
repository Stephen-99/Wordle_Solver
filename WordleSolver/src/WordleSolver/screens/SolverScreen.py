import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.LetterColour import LetterColour
import Screen

class SolverScreen(Screen):
    def __init__(self):
        self.letters = [LetterColour() for _ in range(5)]
    
    def CreateScreen(self, word: list[str]) -> toga.Box:
        solverBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))

        titleLabel = toga.Label("Please enter the following word as your guess\nClick the buttons to match the result :D", style=Pack(padding=(2,5), font_size=16, text_align='center'))
        letterButtonsBox = toga.Box(style=Pack(direction=ROW))
        submitButtonsBox = toga.Box(style=Pack(direction=ROW))

        letterButtons  = [self.CreateLetterButton(letter) for letter in word.upper()]
        [letterButtonsBox.add(button) for button in letterButtons]

        #TODO add integration with the wordle library here so that it can actually use the solver.
        submitButton = toga.Button("Submit", on_press=self.SolverSubmitHandler, style=Pack(padding=5, font_size=12))
        correctButton = toga.Button("Correct Guess!", style=Pack(padding=5, font_size=12))
        submitButtonsBox.add(submitButton, correctButton)

        innerBox.add(titleLabel, letterButtonsBox, submitButtonsBox)
        solverBox.add(innerBox)
        return solverBox

    def CreateLetterButton(self, letter):
        colourData = LetterColour()
        self.letters.append(colourData)
        size = 100
        button = toga.Button(letter, on_press=colourData, style=Pack(padding=5, font_weight="bold", font_size=32, width=size, height=size, color="#ffffff", background_color=colourData.colour))
        #Can't seem to get button border to change color... :(
        return button
    
    def SolverSubmitHandler(self, widget) -> None:
        #Somehow need the state of the letter buttons to pass on. Will need to re-think how this class is structured.
        #TODO: rethink about how the whole app is structured. This file particularly. Should there be separate classes fro solver and main screens?
            #Each screen should have it's own class with it's own set of variables and functions.
            #May need some Inheritance hierachy So can use all the screens interchangeably.
        self.SetSolverScreen(self.solver.ProcessGuessResults(self.letters))
        #HMM, will need some sort of cool logic pattern to be able to pass on back to the main screen when it's time to change screens
            #Some kind of observer type pattern mayhaps.
            #don't want to too tightly couple the screens. This screen should call app to let it know it's finished. App can decide to show main screen.

