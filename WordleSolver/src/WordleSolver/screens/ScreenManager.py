import toga
from WordleSolver.screens.Screen import Screen
from WordleSolver.screens.MainMenuScreen import MainMenuScreen
from WordleSolver.screens.SolverScreen import SolverScreen
from WordleSolver.screens.ErrorScreen import TextScreen
from WordleSolver.screens.PlayWordleScreen import PlayWordleScreen

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *

#TODO create a listener interface this can implement.
class ScreenManager:
    def __init__(self, changeScreensFunc, wordleRows):
        self.changeScreens = changeScreensFunc
        self.curScreen = None
        self.RegisterHandlers()

        #initiate screens
        self.solverScreen = SolverScreen()
        self.solverScreen.CreateScreen()
        self.menuScreen = MainMenuScreen()
        self.menuScreen.CreateScreen()
        self.errorScreen = TextScreen()
        self.errorScreen.CreateScreen()
        self.playWordleScreen = PlayWordleScreen(wordleRows)
        self.playWordleScreen.CreateScreen()

        #start with menuScreen (This may need to move to a separate startup func)
        self.ChangeScreen(self.menuScreen)
        self.curScreen = self.menuScreen

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)
        EventSystem.subscribe(ReturnToMainMenuEvent, self.SolverFinished)
        EventSystem.subscribe(ShowTextScreenEvent, self.ShowTextScreen)
        EventSystem.subscribe(ShowErrorContentEvent, self.AddErrorBoxToCurScreen)
        EventSystem.subscribe(PlayWordleEvent, self.PlayWordle)
        EventSystem.subscribe(PlayWordleUpdatedEvent, self.UpdatePlayWordleScreen)

    def UpdateSolverScreen(self, event: NewWordEvent):
        self.solverScreen.UpdateWord(event.word)
        self.ChangeScreen(self.solverScreen)

    def ChangeScreen(self, screen: Screen):
        screenContent = screen.UpdateScreen()
        self.changeScreens(screenContent)
        self.curScreen = screen

    def SolverFinished(self, event: ReturnToMainMenuEvent):
        self.ChangeScreen(self.menuScreen)

    def PlayWordle(self, event: PlayWordleEvent):
        self.ChangeScreen(self.playWordleScreen)

    def UpdatePlayWordleScreen(self, event: PlayWordleUpdatedEvent):
        self.ChangeScreen(self.playWordleScreen)

    def AddErrorBoxToCurScreen(self, event: ShowErrorContentEvent):
        updatedScreenContent = self.curScreen.ShowError(event.content)
        self.changeScreens(updatedScreenContent)
        #So Screens will need to implement a method to add error content.

    def ShowTextScreen(self, event: ShowTextScreenEvent):
        self.errorScreen.UpdateMessage(event.msg)
        self.ChangeScreen(self.errorScreen)
