import PySimpleGUI as sg


#This code is written by AI. It is kind of average. Instead of persisting state via a list, I would like to have the squares backed by soem data object I can reference.
def main(word: str):
    layout = [
        [sg.Button(word[i], size=(5, 2), key=f'square{i}', font=('Helvetica', 32, 'normal'), button_color=('black', 'gray')) for i in range(5)],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Colorful Squares', layout)

    color_sequence = ['gray', 'yellow', 'green']
    square_colors = ['gray'] * 5  # Initialize all squares to gray

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event.startswith('square'):
            square_index = int(event[len('square'):])
            current_color_index = color_sequence.index(square_colors[square_index])
            new_color_index = (current_color_index + 1) % len(color_sequence)
            square_colors[square_index] = color_sequence[new_color_index]
            window[event].update(button_color=(square_colors[square_index]))
    window.close()

if __name__ == '__main__':
    main("joker")
