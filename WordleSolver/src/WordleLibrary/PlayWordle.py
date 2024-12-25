import random

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import WonGameEvent, LostGameEvent, IncorrectGuessEvent, ErrorOccuredEvent

from .Database import *
from .Guess import *

class PlayWordle:
    def __init__(self, validWords, allowedWords):
        self.validWords, self.allowedWords = validWords, allowedWords
        self.guesses = 0
        self.answer = self.GetRandomWord()

    def Reset(self):
        self.guesses = 0
        self.answer = self.GetRandomWord()

    def MakeAGuess(self, word: str):
        if not self.IsAllowedWord(word):
            EventSystem.EventOccured(ErrorOccuredEvent("Word is not an allowed word"))
            return
        
        guess, guessIsCorrect = self.GetGuess(word)

        if guessIsCorrect:
            EventSystem.EventOccured(WonGameEvent("~~~You Won!~~~"))
            return
    
        if self.guesses >= 6:
            EventSystem.EventOccured(LostGameEvent("You Lost :("))
            return
        
        EventSystem.EventOccured(IncorrectGuessEvent(guess))

    def GetGuess(self, word):
        self.guesses += 1
        guess = Guess(word)
        guessIsCorrect = guess.ValidateGuess(self.answer)
        
        return guess, guessIsCorrect

    def IsAllowedWord(self, word):
        return word in self.allowedWords

    def GetRandomWord(self) -> str:
        return random.choice(self.validWords)
