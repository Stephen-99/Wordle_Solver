from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *

from WordleLibrary.PlayWordle import PlayWordle
from WordleSolver.screens.ScreenHelpers.PlayWordleRows import PlayWordleRows

class PlayWordleListener:
    def __init__(self, playWordleClient: PlayWordle):
        self.playWordleClient = playWordleClient
        self.wordleRows = PlayWordleRows()
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(PlayWordleGuessEvent, self.NewGuessHandler)
        EventSystem.subscribe(PlayWordleEvent, self.PlayWordle)
        EventSystem.subscribe(IncorrectGuessEvent, self.IncorrectGuessHandler)

    def NewGuessHandler(self, event: PlayWordleGuessEvent):
        self.playWordleClient.MakeAGuess(event.word)

    def PlayWordle(self, event: PlayWordleEvent):
        self.playWordleClient.reset()

    def IncorrectGuessHandler(self, event: IncorrectGuessEvent):
        self.wordleRows.UpdateActiveRow(event.guess)