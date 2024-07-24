#To create and setup the listeners

#Listeners
from WordleSolver.screens.ScreenManager import ScreenManager
from .SolverListener import SolverListener
from .PlayWordleListener import PlayWordleListener
from WordleSolver.screens.ScreenHelpers.PlayWordleRows import PlayWordleRows

#Dependencies of those listeners.
from WordleLibrary.solver import WordleSolver
from WordleLibrary.PlayWordle import PlayWordle

class ListenerCreator:
    def __init__(self) -> None:
        self.listeners = []

    def SetupListeners(self, changeScreensFunc, exitFunc, solver: WordleSolver, playWordleClient: PlayWordle, wordleRows: PlayWordleRows):
        self.listeners.append(ScreenManager(changeScreensFunc, exitFunc, wordleRows))
        self.listeners.append(SolverListener(solver))
        self.listeners.append(PlayWordleListener(playWordleClient, wordleRows))