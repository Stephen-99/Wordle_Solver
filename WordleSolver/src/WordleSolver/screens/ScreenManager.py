from WordleSolver.Events import EventSystem

from WordleSolver.Events.ChangeScreenEvent import ChangeScreenEvent
from WordleSolver.screens.MainMenuScreen import MainMenuScreen
from WordleSolver.screens.SolverScreen import SolverScreen
from WordleSolver.Events.NewWordEvent import NewWordEvent
from WordleSolver.screens.Screen import Screen

#TODO create a listener interface this can implement.
class ScreenManager:
    #Also the different screens that we do have.
    #Can we decouple the screens from this manager somehow?
    #We just have a listener that takes the screen to update as a parameter.
        #Will have an event that has the screen as a parameter
        #Will call to updateScreen, and then call self.changeScreens
    def __init__(self, changeScreensFunc):
        self.changeScreens = changeScreensFunc
        
        #initiate screens
        self.solverScreen = SolverScreen()
        self.solverScreen.CreateScreen()
        self.menuScreen = MainMenuScreen()
        self.menuScreen.CreateScreen()

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)

    def UpdateSolverScreen(self, event: NewWordEvent):
        self.solverScreen.UpdateWord(event.word)

    def ChangeScreen(self, screen: Screen):
        screen.UpdateScreen()
        self.changeScreens(screen)
 


    #It feels like screen manager should be responsible for setting up the different screens
         
    #Should handle the appListener stuff. 
        #idea is shouldn't have a listener on the app so get rid of that