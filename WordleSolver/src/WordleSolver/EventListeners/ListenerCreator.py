#To create and setup the listeners

#Listeners
from WordleSolver.screens.ScreenManager import ScreenManager
from .SolverListener import SolverListener

#Dependencies of those listeners.
from WordleLibrary.solver import WordleSolver

class ListenerCreator:
    def __init__(self) -> None:
        self.listeners = []

    def SetupListeners(self, changeScreensFunc, solver: WordleSolver):
        self.listeners.append(ScreenManager(changeScreensFunc))
        self.listeners.append(SolverListener(solver))