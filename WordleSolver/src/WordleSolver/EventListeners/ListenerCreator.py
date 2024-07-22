#To create and setup the listeners

#Listeners
from WordleSolver.screens.ScreenManager import ScreenManager
from .SolverListener import SolverListener
from .PlayWordleListener import PlayWordleListener

#Dependencies of those listeners.
from WordleLibrary.solver import WordleSolver
from WordleLibrary.PlayWordle import PlayWordle

class ListenerCreator:
    def __init__(self) -> None:
        self.listeners = []

    def SetupListeners(self, changeScreensFunc, exitFunc, solver: WordleSolver, playWordleClient: PlayWordle):
        self.listeners.append(ScreenManager(changeScreensFunc, exitFunc))
        self.listeners.append(SolverListener(solver))
        self.listeners.append(PlayWordleListener(playWordleClient))