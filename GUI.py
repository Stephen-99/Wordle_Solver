import PySimpleGUI as sg
from enum import Enum


class WordleStates(Enum):
    INCORRECT = 1
    MISPLACED = 2
    CORRECT = 3


# TODO these will be able to be removed once LetterColour is fully implemented
yellow = "#a39529"
gray = "#424242"
green = "#459824"

# TODO return the results somehow and interact with Guess.py


# This code is written by AI. It is kind of average. Instead of persisting state via a list, I would like to have the squares backed by soem data object I can reference.
# TODO:
# - Split this up into multiple functions
# - Create some data object for storing the information about the colour. It should also handle state changes and make it easy for Guess to interact with.
# - Length of word = 5 is hard coded in a bunch of places. Use a constant somewhere. Throughout the app even.


class LetterColour:
    yellow = "#a39529"
    gray = "#424242"
    green = "#459824"

    def __init__(self):
        self.colour = gray
        self.state = WordleStates.INCORRECT

    def changeState(self):
        match self.state:
            case WordleStates.INCORRECT:
                self.state = WordleStates.MISPLACED
                self.colour = yellow
            case WordleStates.MISPLACED:
                self.state = WordleStates.CORRECT
                self.colour = green
            case WordleStates.CORRECT:
                self.state = WordleStates.INCORRECT
                self.colour = gray


def obtainGuessResults(guess: str):
    word = guess.upper()
    # display a square button for each letter, with the letter inside that button
    layout = [
        [
            sg.Button(
                word[i],
                size=(5, 2),
                key=f"square{i}",
                font=("Helvetica", 32, "bold"),
                button_color=("white", gray),
            )
            for i in range(5)
        ],
        [sg.Button("Submit")],
    ]

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


if __name__ == "__main__":
    obtainGuessResults("joker")
