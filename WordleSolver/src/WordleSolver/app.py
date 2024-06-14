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
    #Have an init. Setup thimgs like a solver gui class. Looks after the buttons and their colours.
    

    #TODO:
        #OK. So still circular imports. Because this app class is special, I can't manually create this app class and trigger 
        # dependencies like I might normally do. Instead, I need to separate almost everything out of it. 
            #The one screenManager opr whatever, will need to be provided with a callback to the app for the one functionality 
            # of changing the screen. I could also just subvert the problem for now by providing a callback. That is only an average soln though.
    def startup(self):
        #TODO: Move these 2 into the init of the solver screen..
        solver = Solver(self)
        ListenerCreator().SetupListeners(self.ChangeScreen, solver)

        self.main_window = toga.MainWindow(title=self.formal_name)



    

        #self.SetMainScreen()
        self.SetSolverScreen(solver.GetNextGuess()) #TODO use events and things for all this.

    def ChangeScreen(self, screenContent):
        self.main_window.content = screenContent
        self.main_window.show()

    def SetSolverScreen(self, word):
        self.solverScreen.UpdateWord(word)
        self.main_window.content = self.solverScreen.UpdateScreen()
        self.main_window.show()

    def SetMainScreen(self):
        self.main_window.content = self.mainScreen.UpdateScreen()
        self.main_window.show()    


def main():
    return WordleSolver()
