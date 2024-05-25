"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
from typing import Any
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.solver import PlayWordle, RunWithUserInput
from WordleLibrary.solver import WordleSolver as Solver
from WordleLibrary.LetterColour import LetterColour

#REMEMBER I can use other classes in other files :D
#Ayum. Should use toga's event system... (ig I am with buttons...)
#More importantly, have a separate class for each view. The Wordle Library acts kind fo like the model, and this kind of like the controller/presenter.
class WordleSolver(toga.App):
    #Have an init. Setup thimgs like a solver gui class. Looks after the buttons and their colours.
    def startup(self):
        self.letters = [] #TODO this should move into a different class.
        self.solver = Solver(self)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.SetMainScreen()
        #self.SetSolverScreen(self.solver.GetNextGuess())

    def CreateMainScreen(self):
        mainBox = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        welcomeTextLabel = toga.Label("Hello! Welcome to Wordle Solver!\nPlease choose to either play a game of Wordle, use the solver to solve a wordle puzzle, or exit.",
                                      style=Pack(padding=(2,5), font_size=16, text_align='center'))
        
        buttonsBox = toga.Box()
        playButton = toga.Button("Play Wordle", on_press=self.PlayWordleHandler, style=Pack(padding=5, font_size=12))
        solveButton = toga.Button("Use the solver", on_press=self.RunSolverHandler, style=Pack(padding=5, font_size=12))
        exitButton = toga.Button("Exit", on_press=self.ExitAppHandler, style=Pack(padding=5, font_size=12))
        buttonsBox.add(playButton, solveButton, exitButton)

        mainBox.add(welcomeTextLabel, buttonsBox)
    
        return mainBox

    def CreateSolverScreen(self, word):
        self.letters = []
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

    def SetSolverScreen(self, word):
        self.main_window.content = self.CreateSolverScreen(word)
        self.main_window.show()

    def SetMainScreen(self):
        self.main_window.content = self.CreateMainScreen()
        self.main_window.show()

    def CreateLetterButton(self, letter):
        colourData = LetterColour()
        self.letters.append(colourData)
        size = 100
        button = toga.Button(letter, on_press=colourData, style=Pack(padding=5, font_weight="bold", font_size=32, width=size, height=size, color="#ffffff", background_color=colourData.colour))
        #Can't seem to get button border to change color... :(
        return button

    
    def ExitAppHandler(self, widget) -> None:
        self.app.exit()

    def PlayWordleHandler(self, widget) -> None:
        PlayWordle()

    def RunSolverHandler(self, widget) -> None:
        self.SetSolverScreen(self.solver.GetNextGuess())

    def SolverSubmitHandler(self, widget) -> None:
        #Somehow need the state of the letter buttons to pass on. Will need to re-think how this class is structured.
        #TODO: rethink about how the whole app is structured. This file particularly. Should there be separate classes fro solver and main screens?
            #Each screen should have it's own class with it's own set of variables and functions.
            #May need some Inheritance hierachy So can use all the screens interchangeably.
        #if it returns none, don't set solver screen, go to main.
        self.SetSolverScreen(self.solver.ProcessGuessResults(self.letters))


def main():
    return WordleSolver()
