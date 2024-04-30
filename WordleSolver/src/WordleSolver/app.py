"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.solver import PlayWordle, RunWithUserInput


class WordleSolver(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.CreateMainScreen()
        self.main_window.show()

    def ExitAppHandler(self, widget) -> None:
        self.app.exit()

    def PlayWordleHandler(self, widget) -> None:
        PlayWordle()

    def RunSolverHandler(self, widget) -> None:
        self.main_window.content = self.CreateSolverScreen("irate")
        self.main_window.show()
        RunWithUserInput()

    def CreateSolverScreen(self, word):
        solverBox = toga.Box(style=Pack(direction=COLUMN))
        letterButtonsBox = toga.Box(style=Pack(direction=ROW))
        letterButtons  = [self.CreateLetterButton(letter) for letter in word]
        for button in letterButtons:
            letterButtonsBox.add(button) #TODO: surely a way to one line this.

        solverBox.add(letterButtonsBox)
        return solverBox


    def CreateLetterButton(self, letter):
        button = toga.Button(letter, style=Pack(padding=5, font_weight="bold", font_size=20))
        button.width = button.height = 50  # Set button size as a square
        return button

    def CreateMainScreen(self):
        mainBox = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        welcomeTextLabel = toga.Label("Hello! Welcome to Wordle Solver!\nPlease choose to either play a game of Wordle, use the solver to solve a wordle puzzle, or exit.",
                                      style=Pack(padding=(2,5), font_size=16, text_align='center'))
        
        buttonsBox = toga.Box()
        playButton = toga.Button("Play Wordle", on_press=self.PlayWordleHandler, style=Pack(padding=5, font_size=12))
        solveButton = toga.Button("Use the solver", on_press=self.RunSolverHandler, style=Pack(padding=5, font_size=12))
        exitButton = toga.Button("Exit", on_press=self.ExitAppHandler, style=Pack(padding=5, font_size=12))
        buttonsBox.add(playButton, solveButton, exitButton)

        mainBox.add(welcomeTextLabel, buttonsBox)
    
        return mainBox
def main():
    return WordleSolver()

#TODO:
#Create a basic landing page similar to what's in the existing app.