"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
import threading
import toga
from time import sleep

from WordleLibrary.solver import WordleSolver as Solver
from WordleLibrary.PlayWordle import PlayWordle
from WordleSolver.screens.ScreenHelpers.PlayWordleRows import PlayWordleRows
from .EventListeners.ListenerCreator import ListenerCreator

class WordleSolver(toga.App):
    def startup(self):
        self.guiTasks = []
        self.results = []
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        #TODO: Move these 2 into the Injector
        #I could instead do lazy initialization for the solver and playWordle objects. Have them as singletons
        #The listeners can create them as needed.
        solver = Solver()
        wordleRows = PlayWordleRows()
        playWordleClient = PlayWordle()

        #Some of what this calls is setting up the new screens, so that will need to be on the gui thread.
        #What if instead I make some gui thread object, and pass that into the screens to use for setting up. 
            #It will need some from of queue etc.
        #ONE last chance to see if toga has made an easy way to do this.

        #TODO: create this with new thread. all gui requests to come here.
        ListenerCreator().SetupListeners(self.ChangeScreen, self.UpdateGui, solver, playWordleClient, wordleRows)

    def ChangeScreen(self, screenContent):
        self.main_window.content = screenContent
        self.main_window.show()

    #My other option is to manually call this function with what I know is the main thread. I suppose it can't run this loop forever
    #unless I spawn everything else in different threads.
    def on_running(self):
        #This is never getting called
        print("On running is CALLLEEEEEEEEEEEEED\n\n\n\n\n\n\n")
        #NEW EVENT SYSTEM HERE WHAT FUN!
        #Really just the current event system needs to know about this, and can pass specific gui events here.
        while True:
                #Need to setup and get a lock here to avoid race conditions
            if len(self.guiTasks) > 0:
                print("Running gui task", self.guiTasks[0])
                res = self.guiTasks[0]()
                del self.guiTasks[0]
                self.results.append(res)
                print("gui task result:", self.results) 
                #SOmething something notify results


    def UpdateGui(self, fnToRun):
        self.guiTasks.append(fnToRun)
        sleep(5)
        result = self.results[0]
        return result
    
    



def main():
    return WordleSolver()


#  ~~~~~  Must do before releasing to play store  ~~~~~  #
    # Fix text not fitting on home screen ~~ :D ~~

#  ~~~~~  Like to do before releasing to play store  ~~~~~  #
    # Play wordle, jump to next box after entering a letter ~~ :D ~~
    # Play wordle, on clicking a box, set cursor to the start ~~ Don't seem to be able to move the cursor with Toga ~~
    # Cause errors to not send back to the home screen
    # Add back buttons to playWordle and solver screens
    # Nicer won and loss screens
    # An app logo
    # Allow players to input their own word choices and results so far
    # 2nd letter only highlight if it is in the word twice. (Check how does nytimes do it?)

#  ~~~~~  Would like to do  ~~~~~  #
    # putting GUI stuff on a separate thread. It's all single-threaded atm
    # Make it work for landscape, or enforce portrait mode