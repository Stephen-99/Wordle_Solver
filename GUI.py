import PySimpleGUI as sg

yellow = "#a39529"
gray = "#424242"
green = "#459824"

# TODO return the results somehow and interact with Guess.py


# This code is written by AI. It is kind of average. Instead of persisting state via a list, I would like to have the squares backed by soem data object I can reference.
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


if __name__ == "__main__":
    obtainGuessResults("joker")
