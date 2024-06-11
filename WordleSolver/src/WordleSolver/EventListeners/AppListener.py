from WordleSolver.Events import EventSystem
from WordleSolver.Events.NewWordEvent import NewWordEvent

class AppListener:
    #The function from the app is expected for when setting solver screen
    def __init__(self, appFunc):
        self.setSolverScreen = appFunc
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)

    def UpdateSolverScreen(self, event: NewWordEvent):
        self.setSolverScreen(event.word)
