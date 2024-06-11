#To create and setup the listeners

#Listeners
from .AppListener import AppListener
from .SolverListener import SolverListener

#Dependencies of those listeners.
from WordleLibrary.solver import WordleSolver

class ListenerCreator:
    def __init__(self) -> None:
        self.listeners = []

    def SetupListeners(self, appFunc, solver: WordleSolver):
        self.listeners.append(AppListener(appFunc))
        self.listeners.append(SolverListener(solver))