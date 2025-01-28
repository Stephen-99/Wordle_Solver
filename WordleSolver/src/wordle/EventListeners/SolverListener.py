from threading import Thread
from wordle.Events import EventSystem
from wordle.Events.Events import *
from WordleLibrary.solver import WordleSolver

class SolverListener:
    def __init__(self, solver: WordleSolver):
        self.solver = solver
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(SubmitGuessResultsEvent, self.SubmitGuessHandler)
        EventSystem.subscribe(RunSolverEvent, self.RunSolverHandler)
        EventSystem.subscribe(SolverGuessByUser, self.UpdateSolverGuess)

    async def SubmitGuessHandler(self, event: SubmitGuessResultsEvent):
        self.solver.ProcessGuessResults(event.letters)
    
    async def RunSolverHandler(self, event: RunSolverEvent):
        #Does this actually help? We still have to wait till solver is setup before showing the screen
        #It would seem creating the char commonality from scratch takes a long time. Let's cahce an initial one
        #ok, that didn't seem to be the issue. Try profiling it. Likely the db call just takes too long
            #can cache that too...
        Thread(target=self.SolverSetup).start()

    async def UpdateSolverGuess(self, event: SolverGuessByUser):
        self.solver.SetUserGuess(event.word)

    def SolverSetup(self):
        self.solver.resetSolver()
        self.solver.GetNextGuess()
        

