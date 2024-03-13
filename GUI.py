import PySimpleGUI as sg
from enum import Enum


class WordleStates(Enum):
    INCORRECT = 1
    MISPLACED = 2
    CORRECT = 3


# TODO return the results somehow and interact with Guess.py


class LetterColour:
    yellow = "#a39529"
    gray = "#424242"
    green = "#459824"

    def __init__(self):
        self.colour = self.gray
        self.state = WordleStates.INCORRECT

    def changeState(self):
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


# TODO: Add a title, saying to enter the guess and please pass back the results.
def ObtainGuessResults(guess: str) -> list[LetterColour]:
    layout = CreateButtonsLayout(5, guess.upper())
    window = sg.Window("Colorful Squares", layout)

    square_colours = []
    for _ in range(5):
        square_colours.append(LetterColour())

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Submit":
            break
        elif event.startswith("square"):
            square_index = int(event[len("square") :])
            square_colours[square_index].changeState()
            window[event].update(button_color=(square_colours[square_index].colour))
    window.close()

    return square_colours


def CreateButtonsLayout(numSquares: int, word: str) -> list[list[sg.Button]]:
    # display a square button for each letter, with the letter inside that button
    return [
        [
            sg.Button(
                word[i],
                size=(5, 2),
                key=f"square{i}",
                font=("Helvetica", 32, "bold"),
                button_color=("white", LetterColour.gray),
            )
            for i in range(numSquares)
        ],
        [sg.Button("Submit")],
    ]


if __name__ == "__main__":
    ObtainGuessResults("joker")
