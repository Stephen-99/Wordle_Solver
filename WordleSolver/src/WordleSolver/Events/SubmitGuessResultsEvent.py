from typing import List

from WordleLibrary.LetterColour import LetterColour

#TODO make all events data classes
class SubmitGuessResultsEvent:
    def __init__(self, letters: List[LetterColour]):
        self.letters = letters