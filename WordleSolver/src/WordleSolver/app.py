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
from .EventListeners.SolverListener import SolverListener
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
