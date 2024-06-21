#All the events in one file for easy imports :D

from typing import List

from WordleLibrary.LetterColour import LetterColour

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

class SolverFinishedEvent:
    pass

class SubmitGuessResultsEvent:
    def __init__(self, letters: List[LetterColour]):
        self.letters = letters
