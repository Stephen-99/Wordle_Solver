from WordleSolver.screens.Screen import Screen
from WordleSolver.screens.MainMenuScreen import MainMenuScreen
from WordleSolver.screens.SolverScreen import SolverScreen
from WordleSolver.screens.ErrorScreen import ErrorScreen
from WordleSolver.screens.PlayWordleScreen import PlayWordleScreen

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import NewWordEvent, ExitAppEvent, ReturnToMainMenuEvent, ErrorOccuredEvent

#TODO create a listener interface this can implement.
class ScreenManager:
    def __init__(self, changeScreensFunc, exitAppFunc):
        self.changeScreens = changeScreensFunc
        self.exit = exitAppFunc
        
        self.RegisterHandlers()

        #initiate screens
        self.solverScreen = SolverScreen()
        self.solverScreen.CreateScreen()
        self.menuScreen = MainMenuScreen()
        self.menuScreen.CreateScreen()
        self.errorScreen = ErrorScreen()
        self.errorScreen.CreateScreen()
        self.playWordleScreen = PlayWordleScreen()
        self.playWordleScreen.CreateScreen()

        #start with menuScreen (This may need to move to a separate startup func)
        #self.ChangeScreen(self.menuScreen)
        self.ChangeScreen(self.playWordleScreen)

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)
        EventSystem.subscribe(ExitAppEvent, self.ExitAllScreens)
        EventSystem.subscribe(ReturnToMainMenuEvent, self.SolverFinished)
        EventSystem.subscribe(ErrorOccuredEvent, self.ErrorOccured)

    def UpdateSolverScreen(self, event: NewWordEvent):
        self.solverScreen.UpdateWord(event.word)
        self.ChangeScreen(self.solverScreen)

    def ChangeScreen(self, screen: Screen):
        screenContent = screen.UpdateScreen()
        self.changeScreens(screenContent)
 
    def ExitAllScreens(self, event: ExitAppEvent):
        self.exit()

    def SolverFinished(self, event: ReturnToMainMenuEvent):
        self.ChangeScreen(self.menuScreen)

    def ErrorOccured(self, event: ErrorOccuredEvent):
        self.errorScreen.UpdateMessage(event.errorMsg)
        self.ChangeScreen(self.errorScreen)