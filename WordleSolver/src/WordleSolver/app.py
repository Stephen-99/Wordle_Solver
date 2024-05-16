"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
from typing import Any
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleLibrary.solver import PlayWordle, RunWithUserInput


class WordleSolver(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        #self.main_window.content = self.CreateMainScreen()
        self.main_window.content = self.CreateSolverScreen("irate")
        self.main_window.show()

    def CreateSolverScreen(self, word):
        solverBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))
        letterButtonsBox = toga.Box(style=Pack(direction=ROW))
        letterButtons  = [self.CreateLetterButton(letter) for letter in word.upper()]
        [letterButtonsBox.add(button) for button in letterButtons]

        innerBox.add(letterButtonsBox)
        solverBox.add(innerBox)
        return solverBox


    def CreateLetterButton(self, letter):
        colourData = LetterColour()
        size = 100
        button = toga.Button(letter, on_press=colourData, style=Pack(padding=5, font_weight="bold", font_size=32, width=size, height=size, color="#ffffff", background_color=colourData.colour))
        #Can't seem to get button border to change color... :(
        return button

    def CreateMainScreen(self):
        mainBox = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        welcomeTextLabel = toga.Label("Hello! Welcome to Wordle Solver!\nPlease choose to either play a game of Wordle, use the solver to solve a wordle puzzle, or exit.",
                                      style=Pack(padding=(2,5), font_size=16, text_align='center'))
        
        buttonsBox = toga.Box()
        playButton = toga.Button("Play Wordle", on_press=self.PlayWordleHandler, args='hi', style=Pack(padding=5, font_size=12))
        solveButton = toga.Button("Use the solver", on_press=self.RunSolverHandler, style=Pack(padding=5, font_size=12))
        exitButton = toga.Button("Exit", on_press=self.ExitAppHandler, style=Pack(padding=5, font_size=12))
        buttonsBox.add(playButton, solveButton, exitButton)

        mainBox.add(welcomeTextLabel, buttonsBox)
    
        return mainBox
    

    def ExitAppHandler(self, widget) -> None:
        self.app.exit()

    def PlayWordleHandler(self, widget) -> None:
        PlayWordle()

    def RunSolverHandler(self, widget) -> None:
        self.main_window.content = self.CreateSolverScreen("irate")
        self.main_window.show()
        RunWithUserInput()

class LetterColour:    
    yellow = "#a39529"
    gray = "#424242"
    green = "#459824"
    
    def __init__(self):
        self.colour = self.gray

    def  __call__(self, widget: toga.Button, *args: Any, **kwds: Any) -> Any:
        self.UpdateColour()
        widget.style.background_color = self.colour
    
    def UpdateColour(self):
        if self.colour == self.gray:
            self.colour = self.yellow
        elif self.colour == self.yellow:
            self.colour = self.green
        else:
            self.colour = self.gray

def main():

    return WordleSolver()
