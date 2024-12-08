import toga
from WordleSolver.screens.Screen import Screen
from WordleSolver.screens.MainMenuScreen import MainMenuScreen
from WordleSolver.screens.SolverScreen import SolverScreen
from WordleSolver.screens.TextScreen import TextScreen
from WordleSolver.screens.PlayWordleScreen import PlayWordleScreen

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *

#TODO create a listener interface this can implement.
class ScreenManager:
    def __init__(self, changeScreensFunc, wordleRows, screenWidth):
        self.changeScreens = changeScreensFunc
        self.curScreen = None
        self.RegisterHandlers()

        #initiate screens
        self.solverScreen = SolverScreen(screenWidth)
        self.solverScreen.CreateScreen()
        self.menuScreen = MainMenuScreen(screenWidth)
        self.menuScreen.CreateScreen()
        self.errorScreen = TextScreen(screenWidth)
        self.errorScreen.CreateScreen()
        self.playWordleScreen = PlayWordleScreen(wordleRows, screenWidth)
        self.playWordleScreen.CreateScreen()

        #start with menuScreen (This may need to move to a separate startup func)
        self.changeScreens(self.menuScreen.UpdateScreen())
        self.curScreen = self.menuScreen

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)
        EventSystem.subscribe(ReturnToMainMenuEvent, self.ReturnToMenu)
        EventSystem.subscribe(ShowTextScreenEvent, self.ShowTextScreen)
        EventSystem.subscribe(ShowErrorContentEvent, self.AddErrorBoxToCurScreen)
        EventSystem.subscribe(PlayWordleEvent, self.PlayWordle)
        EventSystem.subscribe(PlayWordleUpdatedEvent, self.UpdatePlayWordleScreen)

    async def UpdateSolverScreen(self, event: NewWordEvent):
        self.solverScreen.TryUpdateWord(event.word)
        await self.ChangeScreen(self.solverScreen)

    async def ChangeScreen(self, screen: Screen):
        screenContent = screen.UpdateScreen()
        self.changeScreens(screenContent)
        self.curScreen = screen

    async def ReturnToMenu(self, event: ReturnToMainMenuEvent):
        await self.ChangeScreen(self.menuScreen)

    async def PlayWordle(self, event: PlayWordleEvent):
        await self.ChangeScreen(self.playWordleScreen)

    async def UpdatePlayWordleScreen(self, event: PlayWordleUpdatedEvent):
        await self.ChangeScreen(self.playWordleScreen)

    async def AddErrorBoxToCurScreen(self, event: ShowErrorContentEvent):
        updatedScreenContent = self.curScreen.ShowError(event.content)
        self.changeScreens(updatedScreenContent)
        #So Screens will need to implement a method to add error content.

    async def ShowTextScreen(self, event: ShowTextScreenEvent):
        self.errorScreen.UpdateMessage(event.msg)
        await self.ChangeScreen(self.errorScreen)
