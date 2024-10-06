import toga

class Screen:
    def CreateScreen(self):
        raise NotImplementedError("This should be implemented by all child classes")
    
    def UpdateScreen(self):
        raise NotImplementedError("This should be implemented by all child classes")
    
    def ShowError(self, errorBox: toga.Box):
        raise NotImplementedError("This should be implemented by all child classes")
    
    def RemoveError(self) -> toga.Box:
        raise NotImplementedError("This should be implemented by all child classes")