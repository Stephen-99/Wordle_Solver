import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .Screen import Screen
from wordle.Events import EventSystem
from wordle.Events.Events import ReturnToMainMenuEvent

#Show error, and on clicking ok, go back to mainScreen
#If different bahviour required, can extend this class and overide the OkButtonHandler.
class TextScreen(Screen):
    def __init__(self, screenWidth):
        super().__init__(screenWidth)
        self.errorMsg = None
        self.innerBox = None
        self.outerBox = None
        self.text = None
        self.okButton = None

    def CreateScreen(self):
        self.outerBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.CreateTextLabel()
        self.okButton = toga.Button("Ok", on_press=self.OkButtonHandler, style=Pack(padding=5, font_size=self.ScaleValue(12), width=self.ScaleValue(80)))
        
        self.innerBox.add(self.text)
        self.innerBox.add(self.okButton)
        self.outerBox.add(self.innerBox)

    def UpdateMessage(self, msg):
        self.errorMsg = msg

    def UpdateScreen(self):
        self.innerBox.remove(self.text)
        self.CreateTextLabel()
        self.innerBox.insert(0, self.text)

        return self.outerBox

    def CreateTextLabel(self):
        self.text = toga.Label(self.errorMsg, style=Pack(padding=(2,5), font_size=16, text_align='center'))

    def OkButtonHandler(self, widget):
        EventSystem.EventOccured(ReturnToMainMenuEvent())
