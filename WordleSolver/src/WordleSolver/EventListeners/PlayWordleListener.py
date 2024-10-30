from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *

from WordleLibrary.PlayWordle import PlayWordle
from WordleSolver.screens.ScreenHelpers.PlayWordleRows import PlayWordleRows

class PlayWordleListener:
    def __init__(self, playWordleClient: PlayWordle, wordleRows: PlayWordleRows):
        self.playWordleClient = playWordleClient
        self.wordleRows = wordleRows
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(PlayWordleGuessEvent, self.NewGuessHandler)
        EventSystem.subscribe(PlayWordleEvent, self.PlayWordle)
        EventSystem.subscribe(IncorrectGuessEvent, self.IncorrectGuessHandler)

    async def NewGuessHandler(self, event: PlayWordleGuessEvent):
        self.playWordleClient.MakeAGuess(event.word)

    async def PlayWordle(self, event: PlayWordleEvent):
        self.playWordleClient.Reset()
        self.wordleRows.Reset()

    async def IncorrectGuessHandler(self, event: IncorrectGuessEvent):
        self.wordleRows.UpdateActiveRow(event.guess)