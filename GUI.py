import PySimpleGUI as sg

from LetterColour import LetterColour
from solver import PlayWordle, RunWithUserInput
from Guess import Guess

# TODO: make the entire experience a GUI
# - On exit, or correct guess (or out of guesses) display some ending text then return back to the start screen
# - Have a fixed size screen and don't close it in-between, just clear it and show the new data.
#   probably will use a gui thread, similar to what I did for my thesis
#   commenting out the window.close() just causes a new window to be created each time. Will need a way to keep track of the window
#   so create a clas for the gui perhaps. May not need a new thread


def DisplayStartScreen():

    while True:
        window = CreateDisplayWindow()
        event, values = window.read()
        if event == "Play Wordle":
            window.close()
            PlayWordle()
        elif event == "Use the solver":
            window.close()
            RunWithUserInput()
        elif event == "Exit" or event == sg.WINDOW_CLOSED:
            break
    window.close()


def CreateDisplayWindow():
    layout = [
        [
            sg.Text(
                "Hello! Welcome to Wordle Solver!\nPlease choose to either play a game of Wordle, use the solver to solve a wordle puzzle, or exit.",
                font=("Helvetica", 18),
            )
        ],
        [sg.Button("Play Wordle"), sg.Button("Use the solver"), sg.Button("Exit")],
    ]
    return sg.Window("Wordle Solver", layout)


def GetGuessFromUser():
    raise NotImplementedError()


def DisplayErrorMessage():
    raise NotImplementedError()


def DisplayGuessResult(guess: Guess):
    raise NotImplementedError()


def DisplayWonScreen():
    raise NotImplementedError()


def DisplayLostScreen():
    raise NotImplementedError()


def ObtainGuessResults(guess: str) -> list[LetterColour]:
    layout = CreateButtonsLayout(5, guess.upper())
    layout.insert(
        0,
        [
            sg.Text(
                "Please enter guess and click buttons to match result",
                font=("Helvetica", 18),
            )
        ],
    )
    window = sg.Window("Wordle Solver", layout)

    square_colours = []
    for _ in range(5):
        square_colours.append(LetterColour())

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Correct Guess!":
            window.close()
            return None
        if event == "Submit":
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
        [sg.Button("Submit"), sg.Button("Correct Guess!")],
    ]


if __name__ == "__main__":
    ObtainGuessResults("joker")
