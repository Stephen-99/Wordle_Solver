from WordleSolver.screens.Screen import Screen
from WordleSolver.screens.MainMenuScreen import MainMenuScreen
from WordleSolver.screens.SolverScreen import SolverScreen

from WordleSolver.Events import EventSystem
from WordleSolver.Events.NewWordEvent import NewWordEvent
from WordleSolver.Events.ExitAppEvent import ExitAppEvent
from WordleSolver.Events.SolverFinishedEvent import SolverFinishedEvent

#TODO create a listener interface this can implement.
class ScreenManager:
    #Also the different screens that we do have.
    #Can we decouple the screens from this manager somehow?
    #We just have a listener that takes the screen to update as a parameter.
        #Will have an event that has the screen as a parameter
        #Will call to updateScreen, and then call self.changeScreens
    def __init__(self, changeScreensFunc, exitAppFunc):
        self.changeScreens = changeScreensFunc
        self.exit = exitAppFunc
        
        #initiate screens
        self.solverScreen = SolverScreen()
        self.solverScreen.CreateScreen()
        self.menuScreen = MainMenuScreen()
        self.menuScreen.CreateScreen()

        #start with menuScreen (This may need to move to a separate startup func)
        self.ChangeScreen(self.menuScreen)

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)
        EventSystem.subscribe(ExitAppEvent, self.ExitAllScreens)
        EventSystem.subscribe(SolverFinishedEvent, self.menuScreen)

    def UpdateSolverScreen(self, event: NewWordEvent):
        self.solverScreen.UpdateWord(event.word)
        self.ChangeScreen(self.solverScreen)

    def ChangeScreen(self, screen: Screen):
        screenContent = screen.UpdateScreen()
        self.changeScreens(screenContent)
 
    def ExitAllScreens(self, event: ExitAppEvent):
        self.exit()

    def SolverFinished(self, event: SolverFinishedEvent):
        self.ChangeScreen(self.menuScreen)