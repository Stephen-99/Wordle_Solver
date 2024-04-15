"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class WordleSolver(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        mainBox = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        welcomeTextLabel = toga.Label("Hello! Welcome to Wordle Solver!\nPlease choose to either play a game of Wordle, use the solver to solve a wordle puzzle, or exit.",
                                      style=Pack(padding=(2,5), font_size=16, text_align='center'))
        
        buttonsBox = toga.Box()
        #Todo bind button calls to methods in wordleLibrary
        playButton = toga.Button("Play Wordle", on_press=None, style=Pack(padding=5, font_size=12))
        solveButton = toga.Button("Use the solver", on_press=None, style=Pack(padding=5, font_size=12))
        exitButton = toga.Button("Exit", on_press=None, style=Pack(padding=5, font_size=12))
        buttonsBox.add(playButton, solveButton, exitButton)

        mainBox.add(welcomeTextLabel, buttonsBox)


        #Welcom text
        #Button x 3


        

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = mainBox
        self.main_window.show()


def main():
    return WordleSolver()

#TODO:
#Create a basic landing page similar to what's in the existing app.