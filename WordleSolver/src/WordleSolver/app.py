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
from .screens.MainMenuScreen import MainMenuScreen
from .screens.SolverScreen import SolverScreen

#REMEMBER I can use other classes in other files :D
#Ayum. Should use toga's event system... (ig I am with buttons...)
#More importantly, have a separate class for each view. The Wordle Library acts kind fo like the model, and this kind of like the controller/presenter.
class WordleSolver(toga.App):
    #Have an init. Setup thimgs like a solver gui class. Looks after the buttons and their colours.
    def startup(self):
        self.letters = [] #TODO this should move into a different class.
        self.solver = Solver(self)
        self.solverScreen = SolverScreen("words")
        #self.mainScreen = MainMenuScreen()
        self.solverScreen.CreateScreen()
        #self.mainScreen.CreateScreen()
    
        self.main_window = toga.MainWindow(title=self.formal_name)

        #self.SetMainScreen()
        self.SetSolverScreen(self.solver.GetNextGuess())

    def SetSolverScreen(self, word):
        self.main_window.content = self.solverScreen.UpdateScreen()
        self.main_window.show()

    def SetMainScreen(self):
        self.main_window.content = self.mainScreen.UpdateScreen()
        self.main_window.show()

    
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
