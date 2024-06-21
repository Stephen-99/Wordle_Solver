from enum import Enum
from typing import Any

import toga


class WordleStates(Enum):
    INCORRECT = 1
    MISPLACED = 2
    CORRECT = 3


class LetterColour:
    yellow = "#a39529"
    gray = "#424242"
    green = "#459824"

    def __init__(self):
        self.colour = self.gray
        self.state = WordleStates.INCORRECT

    def  __call__(self, widget: toga.Button, *args: Any, **kwds: Any) -> Any:
        self.ChangeState()
        widget.style.background_color = self.colour

    def ChangeState(self):
        match self.state:
            case WordleStates.INCORRECT:
                self.state = WordleStates.MISPLACED
                self.colour = self.yellow
            case WordleStates.MISPLACED:
                self.state = WordleStates.CORRECT
                self.colour = self.green
            case WordleStates.CORRECT:
                self.state = WordleStates.INCORRECT
                self.colour = self.gray
                
    def ResetState(self):
        self.colour = self.gray
        self.state = WordleStates.INCORRECT
