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
        self.solver.resetSolver()
        self.solver.GetNextGuess()

#TODO: try updating to use latest version of toga. see if it helps.
#It still trys to pull in simpleyPyGUI too even though I removed it so find out what's up wiht that..