import PySimpleGUI as sg
from enum import Enum

# TODO: make the entire experience a GUI
# - Start screen: Hello, and choice of play, or use solver
# - On exit, or correct guess (or out of guesses) display some ending text then return back to the start screen
# - Have a fixed size screen and don't close it in-between, just clear it and show the new data.
#   probably will use a gui thread, similar to what I did for my thesis
#   commenting out the window.close() just causes a new window to be created each time. Will need a way to keep track of the window
#   so create a clas for the gui perhaps. May not need a new thread


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
# TODO: handle them giving us window closed instead of submit.
                #On window closed, stop running the program
                #On correct, also stop.
                #only continue on submit. If no correct words left, we have to go back to what we had somehow.
# TODO: handle user giving bad input that's inconsistent with what they previously gave us.
def ObtainGuessResults(guess: str) -> list[LetterColour]:
    layout = CreateButtonsLayout(5, guess.upper())
    window = sg.Window("Colorful Squares", layout)

    square_colours = []
    for _ in range(5):
        square_colours.append(LetterColour())

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Submit" or event == "Correct Guess!":
            break
        elif event.startswith("square"):
            square_index = int(event[len("square") :])
            square_colours[square_index].changeState()
            window[event].update(button_color=(square_colours[square_index].colour))
    window.close()

    return square_colours


# TODO: add an option to say it's the correct word rather than all green
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
        [sg.Button("Submit"), sg.Button("Correct Guess!")],
        
    ]


if __name__ == "__main__":
    ObtainGuessResults("joker")
