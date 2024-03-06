import PySimpleGUI as sg
from enum import Enum

class WordleStates(Enum):
    INCORRECT = 1
    MISPLACED = 2
    CORRECT = 3

#TODO these will be able to be removed once LetterColour is fully implemented
yellow = "#a39529"
gray = "#424242"
green = "#459824"

# TODO return the results somehow and interact with Guess.py


# This code is written by AI. It is kind of average. Instead of persisting state via a list, I would like to have the squares backed by soem data object I can reference.
# TODO:
# - Split this up into multiple functions
# - Create some data object for storing the information about the colour. It should also handle state changes and make it easy for Guess to interact with.

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

    # on click will change from gray -> yellow -> green -> gray...
    color_sequence = [gray, yellow, green]
    square_colors = [gray] * 5  # Initialize all squares to gray

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Submit":
            break
        elif event.startswith("square"):
            square_index = int(event[len("square") :])
            current_color_index = color_sequence.index(square_colors[square_index])
            new_color_index = (current_color_index + 1) % len(color_sequence)
            square_colors[square_index] = color_sequence[new_color_index]
            window[event].update(button_color=(square_colors[square_index]))
    window.close()

    return square_colors

if __name__ == "__main__":
    obtainGuessResults("joker")
