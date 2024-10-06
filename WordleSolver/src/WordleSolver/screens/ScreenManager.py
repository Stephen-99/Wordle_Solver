import toga
from WordleSolver.screens.Screen import Screen
from WordleSolver.screens.MainMenuScreen import MainMenuScreen
from WordleSolver.screens.SolverScreen import SolverScreen
from WordleSolver.screens.ErrorScreen import ErrorScreen
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
        self.errorScreen = ErrorScreen()
        self.errorScreen.CreateScreen()
        self.playWordleScreen = PlayWordleScreen(wordleRows)
        self.playWordleScreen.CreateScreen()

        #start with menuScreen (This may need to move to a separate startup func)
        self.ChangeScreen(self.menuScreen)
        self.curScreen = self.menuScreen

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)
        EventSystem.subscribe(ReturnToMainMenuEvent, self.SolverFinished)
        #EventSystem.subscribe(ErrorOccuredEvent, self.ErrorOccured)
        EventSystem.subscribe(ShowErrorContentEvent, self.AddErrorBoxToCurScreen)
        EventSystem.subscribe(RemoveErrorEvent, self.RemoveErrorBoxFromCurScreen)
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

    def RemoveErrorBoxFromCurScreen(self, event: RemoveErrorEvent):
        if event.screen == type(self.curScreen):
            updatedScreenContent = self.curScreen.RemoveError()
            self.changeScreens(updatedScreenContent)

    #TODO Should be updated to use ShowTextScreenEvent
    def ErrorOccured(self, event: ErrorOccuredEvent):
        self.errorScreen.UpdateMessage(event.errorMsg)
        self.ChangeScreen(self.errorScreen)
