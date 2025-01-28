#To create and setup the listeners

#Listeners
from wordle.screens.ScreenManager import ScreenManager
from .SolverListener import SolverListener
from .PlayWordleListener import PlayWordleListener
from .ErrorHandler import ErrorHandler
from wordle.screens.ScreenHelpers.PlayWordleRows import PlayWordleRows

#Dependencies of those listeners.
from WordleLibrary.solver import WordleSolver
from WordleLibrary.PlayWordle import PlayWordle

class ListenerCreator:
    def __init__(self) -> None:
        self.listeners = []

    def SetupListeners(self, changeScreensFunc, solver: WordleSolver, playWordleClient: PlayWordle, wordleRows: PlayWordleRows, screenWidth: int):
        self.listeners.append(ScreenManager(changeScreensFunc, wordleRows, screenWidth))
        self.listeners.append(SolverListener(solver))
        self.listeners.append(PlayWordleListener(playWordleClient, wordleRows))
        self.listeners.append(ErrorHandler(screenWidth))