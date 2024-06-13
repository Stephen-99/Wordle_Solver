

class ScreenManager:
    #Also the different screens that we do have.
    #Can we decouple the screens from this manager somehow?
    #We just have a listener that takes the screen to update as a parameter.
        #Will have an event that has the screen as a parameter
        #Will call to updateScreen, and then call self.changeScreens
    def __init__(self, changeScreensFunc):
        self.changeScreens = changeScreensFunc


    #Should handle the appListener stuff. 