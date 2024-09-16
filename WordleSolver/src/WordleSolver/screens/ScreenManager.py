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

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)
        EventSystem.subscribe(ReturnToMainMenuEvent, self.SolverFinished)
        #EventSystem.subscribe(ErrorOccuredEvent, self.ErrorOccured)
        EventSystem.subscribe(PlayWordleEvent, self.PlayWordle)
        EventSystem.subscribe(PlayWordleUpdatedEvent, self.UpdatePlayWordleScreen)

    def UpdateSolverScreen(self, event: NewWordEvent):
        self.solverScreen.UpdateWord(event.word)
        self.ChangeScreen(self.solverScreen)

    def ChangeScreen(self, screen: Screen):
        screenContent = screen.UpdateScreen()
        self.changeScreens(screenContent)

    def SolverFinished(self, event: ReturnToMainMenuEvent):
        self.ChangeScreen(self.menuScreen)

    def PlayWordle(self, event: PlayWordleEvent):
        self.ChangeScreen(self.playWordleScreen)

    def UpdatePlayWordleScreen(self, event: PlayWordleUpdatedEvent):
        self.ChangeScreen(self.playWordleScreen)

    def AddErrorBoxToCurScreen(self, errorBox: toga.Box):
        screen = toga.app.current.main_window.content
        screen.ShowError(errorBox)
        #So Screens will need to implement a method to add error content.
        #Let's try add that and see what happens

        #SO currentlya n error occured event is raised and that calls the function below, but we actually want the erro hanfler to be called...
        #Currently commenterd out the registration for the below func

        #I think I need to make the error handler a listener.

        #I think I can call a thing to get the main app and get the cur screen from there. Idk tho. might have to keep track fo the current screen here otherwise.

    #TODO Should be updated to use ShowTextScreenEvent
    def ErrorOccured(self, event: ErrorOccuredEvent):
        self.errorScreen.UpdateMessage(event.errorMsg)
        self.ChangeScreen(self.errorScreen)

        #So currently getting these events. This is good. Need to update  to instead create a box with the error message, and then add that to the relevant screen.
        #Need to know the current screen though. 
        #Create a separate erreroHandler for this. It should handle creating the box
        #The event will also need a custom object. One with the error message and the screen it came from.