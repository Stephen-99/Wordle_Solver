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
        self.okButton = toga.Button("Ok", on_press=self.OkButtonHandler, style=Pack(padding=5, font_size=12))
        
        self.box.add(self.text)
        self.box.add(self.okButton)
    
    def UpdateMessage(self, msg):
        self.errorMsg = msg

    def UpdateScreen(self):
        old = self.text
        self.text = toga.Label(self.errorMsg, style=Pack(padding=(2,5), font_size=16, text_align='center'))
        
        #So replace doesn't work, Can get the index, remove it, and re-add the new one. 
        #Don't want to have to re-add all the elements here. If it gets bigger, that becomes a pain.
        self.box.replace(old, self.text)

        return self.box

    def OkButtonHandler(self, widget):
        EventSystem.EventOccured(ReturnToMainMenuEvent)
