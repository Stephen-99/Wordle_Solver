"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
from typing import Any
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.solver import WordleSolver as Solver
from WordleLibrary.LetterColour import LetterColour
from .EventListeners.SolverListener import SolverListener
from .screens.MainMenuScreen import MainMenuScreen
from .screens.SolverScreen import SolverScreen

class WordleSolver(toga.App):
    #Have an init. Setup thimgs like a solver gui class. Looks after the buttons and their colours.
    def startup(self):
        #TODO: Move these 2 into the init of the solver screen..
        self.solver = Solver(self)
        self.solverListner = SolverListener(self.solver)

        self.solverScreen = SolverScreen("words")
        #self.mainScreen = MainMenuScreen()
        self.solverScreen.CreateScreen()
        #self.mainScreen.CreateScreen()
    
        self.main_window = toga.MainWindow(title=self.formal_name)

        #self.SetMainScreen()
        self.SetSolverScreen(self.solver.GetNextGuess()) #TODO use events and things for all this.

    def SetSolverScreen(self, word):
        self.main_window.content = self.solverScreen.UpdateScreen()
        self.main_window.show()

    def SetMainScreen(self):
        self.main_window.content = self.mainScreen.UpdateScreen()
        self.main_window.show()    



def main():
    return WordleSolver()
