from threading import Thread
from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *
from WordleLibrary.solver import WordleSolver

class SolverListener:
    def __init__(self, solver: WordleSolver):
        self.solver = solver
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(SubmitGuessResultsEvent, self.SubmitGuessHandler)
        EventSystem.subscribe(RunSolverEvent, self.RunSolverHandler)

    def SubmitGuessHandler(self, event: SubmitGuessResultsEvent):
        self.solver.ProcessGuessResults(event.letters)
    
    def RunSolverHandler(self, event: RunSolverEvent):
        Thread(target=self.SolverSetup).start()

    def SolverSetup(self):
        self.solver.resetSolver()
        self.solver.GetNextGuess()
        

