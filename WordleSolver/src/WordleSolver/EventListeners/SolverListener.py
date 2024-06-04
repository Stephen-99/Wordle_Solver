from WordleSolver.Events import EventSystem
from WordleSolver.Events.PlayWordleEvent import PlayWordleEvent
from WordleSolver.Events.SubmitGuessResultsEvent import SubmitGuessResultsEvent
from WordleSolver.Events.NewWordEvent import NewWordEvent

from WordleLibrary.solver import WordleSolver, PlayWordle


class SolverListener:
    def __init__(self, solver: WordleSolver):
        self.solver = solver
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(PlayWordleEvent, self.PlayWordleHandler)
        EventSystem.subscribe(SubmitGuessResultsEvent, self.SubmitGuessHandler)

    def PlayWordleHandler(self, event: PlayWordleEvent):
        #TODO: ideally this belongs to the wordle Solver class, or a different class and a different listener.
        PlayWordle()

    def SubmitGuessHandler(self, event: SubmitGuessResultsEvent):
        newWord = self.solver.ProcessGuessResults(event.letters)
        EventSystem.EventOccured(NewWordEvent(newWord))
        #TODO add handling for this event.
        #So solverscreen and app need listners for this.
            #The solver screen needs to update it's word, and then the app needs to update screen
            #The order is important though so maybe the app should have the listener..
