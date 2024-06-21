from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *
from WordleLibrary.solver import WordleSolver, PlayWordle

class SolverListener:
    def __init__(self, solver: WordleSolver):
        self.solver = solver
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(PlayWordleEvent, self.PlayWordleHandler)
        EventSystem.subscribe(SubmitGuessResultsEvent, self.SubmitGuessHandler)
        EventSystem.subscribe(RunSolverEvent, self.RunSolverHandler)

    def PlayWordleHandler(self, event: PlayWordleEvent):
        #TODO: ideally this belongs to the wordle Solver class, or a different class and a different listener.
        PlayWordle()

    def SubmitGuessHandler(self, event: SubmitGuessResultsEvent):
        self.solver.ProcessGuessResults(event.letters)
    
    def RunSolverHandler(self, event: RunSolverEvent):
        self.solver.resetSolver()
        self.solver.GetNextGuess()
