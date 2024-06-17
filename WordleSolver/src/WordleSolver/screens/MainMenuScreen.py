import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleSolver.Events import EventSystem
from WordleSolver.Events.ExitAppEvent import ExitAppEvent
from WordleSolver.Events.PlayWordleEvent import PlayWordleEvent
from WordleSolver.Events.RunSolverEvent import RunSolverEvent

from .Screen import Screen

class MainMenuScreen(Screen):
    def __init__(self):
        self.content = None

    def UpdateScreen(self):
        return self.content
    #TODO: what will need updating, if any.

    def CreateScreen(self):
        mainBox = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        welcomeTextLabel = toga.Label("Hello! Welcome to Wordle Solver!\nPlease choose to either play a game of Wordle, use the solver to solve a wordle puzzle, or exit.",
                                      style=Pack(padding=(2,5), font_size=16, text_align='center'))
        
        buttonsBox = toga.Box()
        playButton = toga.Button("Play Wordle", on_press=self.PlayWordleHandler, style=Pack(padding=5, font_size=12))
        solveButton = toga.Button("Use the solver", on_press=self.RunSolverHandler, style=Pack(padding=5, font_size=12))
        exitButton = toga.Button("Exit", on_press=self.ExitAppHandler, style=Pack(padding=5, font_size=12))
        buttonsBox.add(playButton, solveButton, exitButton)

        mainBox.add(welcomeTextLabel, buttonsBox)
    
        self.content = mainBox
    
    def ExitAppHandler(self, widget) -> None:
        EventSystem.EventOccured(ExitAppEvent())

    def PlayWordleHandler(self, widget) -> None:
        EventSystem.EventOccured(PlayWordleEvent())

    def RunSolverHandler(self, widget) -> None:
        EventSystem.EventOccured(RunSolverEvent())