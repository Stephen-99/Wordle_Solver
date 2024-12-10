import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import PlayWordleEvent, RunSolverEvent
from .Screen import Screen

class MainMenuScreen(Screen):
    def __init__(self, screenWidth):
        super().__init__(screenWidth)
        self.content = None

    def UpdateScreen(self):
        return self.content
    # TODO: what will need updating, if any.

    def CreateScreen(self):
        outerBox = toga.Box(style=Pack(direction=ROW, alignment='center'))
        mainBox = toga.Box(style=Pack(direction=COLUMN, alignment='center', padding=(20, 5), flex=1))
        welcomeTextLabel = toga.Label("Hello! Welcome to Wordle Solver!\n",
                                      style=Pack(padding=(2,5), font_size=self.ScaleValue(24), text_align='center'))
        
        buttonsBox = toga.Box()
        playButton = toga.Button("Play Wordle", on_press=self.PlayWordleHandler, style=Pack(padding=5, font_size=self.ScaleValue(14)))
        solveButton = toga.Button("Use the solver", on_press=self.RunSolverHandler, style=Pack(padding=5, font_size=self.ScaleValue(14)))
        buttonsBox.add(playButton, solveButton)

        mainBox.add(welcomeTextLabel, buttonsBox)
        outerBox.add(mainBox)
        self.content = outerBox

    def PlayWordleHandler(self, widget) -> None:
        EventSystem.EventOccured(PlayWordleEvent())

    def RunSolverHandler(self, widget) -> None:
        EventSystem.EventOccured(RunSolverEvent())

    async def RemoveError(self):
        self.content.remove(self.errorBox)
        return self.content

    def ShowError(self, errorBox: toga.Box):
        self.content.remove(self.errorBox)
        self.errorBox = errorBox
        self.content.add(self.errorBox)
        self.SetErrorTimeout()
        return self.content