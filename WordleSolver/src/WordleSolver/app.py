"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
import toga

from WordleLibrary.solver import WordleSolver as Solver
from .EventListeners.ListenerCreator import ListenerCreator

class WordleSolver(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        #TODO: Move these 2 into the Injector
        #I could instead do lazy initialization for the solver and playWordle objects. Have them as singletons
        #The listeners can create them as needed.
        solver = Solver()
        ListenerCreator().SetupListeners(self.ChangeScreen, self.app.exit, solver)


    def ChangeScreen(self, screenContent):
        self.main_window.content = screenContent
        self.main_window.show()


def main():
    return WordleSolver()
