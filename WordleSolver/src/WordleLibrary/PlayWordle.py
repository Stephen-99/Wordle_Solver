import random

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import WonGameEvent, LostGameEvent, PlayWordleGuessMadeEvent

from .Database import *
from .Guess import *

class PlayWordle:
    def __init__(self):
        self.db = WordleDB()
        self.validWords, self.allowedWords = self.db.GetWords()
        self.guesses = 0
        self.answer = self.GetRandomWord()

    #Will need to be caused by an event raised in wordleRow.
    #Will then raise an event on competion to so wordleRow can updateColours
    def MakeAGuess(self, word: str):
        self.guesses += 1
        guess = Guess(word)
        guessIsCorrect = guess.ValidateGuess(self.answer)

        if guessIsCorrect:
            EventSystem.EventOccured(WonGameEvent("~~~You Won!~~~"))
            return
    
        if self.guesses >= 6:
            EventSystem.EventOccured(LostGameEvent("You Lost :("))
            return
        
        EventSystem.EventOccured(PlayWordleGuessMadeEvent(guess))




    def GetRandomWord(self) -> str:
        return random.choice(self.validWords)
