"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
import toga

from WordleLibrary.solver import WordleSolver as Solver
from WordleSolver.src.WordleSolver.screens.ScreenManager import ScreenManager
from .EventListeners.ListenerCreator import ListenerCreator
from .screens.MainMenuScreen import MainMenuScreen
from .screens.SolverScreen import SolverScreen

class WordleSolver(toga.App):
    def startup(self):
        #TODO: Move these 2 into the Injector
        solver = Solver(self)
        ListenerCreator().SetupListeners(self.ChangeScreen, solver) #Todo pass appp exit: self.app.exit()

        self.main_window = toga.MainWindow(title=self.formal_name)

    def ChangeScreen(self, screenContent):
        self.main_window.content = screenContent
        self.main_window.show()


def main():
    return WordleSolver()
