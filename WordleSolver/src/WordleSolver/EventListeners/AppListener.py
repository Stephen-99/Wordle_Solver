from WordleSolver.Events import EventSystem
from WordleSolver.Events.NewWordEvent import NewWordEvent

from WordleSolver.app import WordleSolver as App

class AppListener:
    def __init__(self, app: App):
        self.app = app
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(NewWordEvent, self.UpdateSolverScreen)

    def UpdateSolverScreen(self, event: NewWordEvent):
        self.app.SetSolverScreen(event.word)
