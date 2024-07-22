#All the events in one file for easy imports :D

from typing import List

from WordleLibrary.LetterColour import LetterColour
from WordleLibrary.Guess import Guess

#TODO make all events data classes

class NewWordEvent:
    def __init__(self, word: List[str]):
        self.word = word

class ExitAppEvent:
    pass

class PlayWordleEvent:
    pass

class RunSolverEvent:
    pass

class ReturnToMainMenuEvent:  #TODO Does it make sense to update this tpo a return to mainmenue event?
    pass

class PlayWordleGuessEvent:
    def __init__(self, word: str):
        self.word = word

class IncorrectGuessEvent:
    def __init__(self, guess: Guess):
        self.guess = guess

class SubmitGuessResultsEvent:
    def __init__(self, letters: List[LetterColour]):
        self.letters = letters

class ErrorOccuredEvent:
    def __init__(self, errorMsg):
        self.errorMsg = errorMsg

#TODO: error event should become a temporary overlay type thing, and this a new screen
class ShowTextScreenEvent(ErrorOccuredEvent):
    def __init__(self, msg):
        super.__init__(msg)

class WonGameEvent(ShowTextScreenEvent):
    def __init__(self, msg):
        super().__init__(msg)

class LostGameEvent(ShowTextScreenEvent):
    def __init__(self, msg):
        super().__init__(msg)