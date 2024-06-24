import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .Screen import Screen
from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import ReturnToMainMenuEvent

#Show error, and on clicking ok, go back to mainScreen
#If different bahviour required, can extend this class and overide the OkButtonHandler.
class ErrorScreen(Screen):
    def __init__(self):
        self.errorMsg = None
        self.box = None
        self.text = None
        self.okButton = None

    def CreateScreen(self):
        self.box = toga.Box(style=Pack(direction=COLUMN, alignment="center"))
        self.text = toga.Label(self.errorMsg, style=Pack(padding=(2,5), font_size=16, text_align='center'))

        #TODO: restrict the width fo this button (just needs to fit the text really)
        self.okButton = toga.Button("Ok", on_press=self.OkButtonHandler, style=Pack(padding=5, font_size=12))
        
        self.box.add(self.text)
        self.box.add(self.okButton)
    
    def UpdateMessage(self, msg):
        self.errorMsg = msg

    def UpdateScreen(self):
        self.box.remove(self.text)
        self.text = toga.Label(self.errorMsg, style=Pack(padding=(2,5), font_size=16, text_align='center'))
        self.box.insert(0, self.text)

        return self.box

    def OkButtonHandler(self, widget):
        EventSystem.EventOccured(ReturnToMainMenuEvent())
