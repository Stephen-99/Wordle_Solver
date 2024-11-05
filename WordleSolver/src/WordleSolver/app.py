"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
import toga
import time

from WordleLibrary.solver import WordleSolver as Solver
from WordleLibrary.Database import WordleDB
from WordleLibrary.PlayWordle import PlayWordle
from WordleSolver.screens.ScreenHelpers.PlayWordleRows import PlayWordleRows
from .EventListeners.ListenerCreator import ListenerCreator

class WordleSolver(toga.App):
    #TODO some kind of llocal db caching. Getting the list of words from the db is the culprit.
        #Also doing it twice. Once for solver and once for playWordle. Re-use the words.

    #Doesn't account for time before startup...
    def startup(self):
        t1 = time.perf_counter(), time.process_time()
        self.main_window = toga.MainWindow(title=self.formal_name)
        t2 = time.perf_counter(), time.process_time()
        print("Setting main window:")
        print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
        print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
        print()
        
        db = WordleDB()
        validWords, allowedWords = db.GetWords()

        #TODO: Move these 2 into the Injector
        #I could instead do lazy initialization for the solver and playWordle objects. Have them as singletons
        #The listeners can create them as needed.
        t1 = time.perf_counter(), time.process_time()
        solver = Solver(db, validWords, allowedWords) #takes 1.6s, but onlly 0.2s cpu time
        t2 = time.perf_counter(), time.process_time()
        print("initialising solver:")
        print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
        print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
        print()

        t1 = time.perf_counter(), time.process_time()
        wordleRows = PlayWordleRows()
        t2 = time.perf_counter(), time.process_time()
        print("init playWordle rows:")
        print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
        print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
        print()

        t1 = time.perf_counter(), time.process_time()
        playWordleClient = PlayWordle(validWords, allowedWords)  #takes 1.26s but only 0.17s CPU time
        t2 = time.perf_counter(), time.process_time()
        print("init play wordle:")
        print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
        print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
        print()

        t1 = time.perf_counter(), time.process_time()
        ListenerCreator().SetupListeners(self.ChangeScreen, solver, playWordleClient, wordleRows)
        t2 = time.perf_counter(), time.process_time()
        print("listner creator:")
        print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
        print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
        print()

    def ChangeScreen(self, screenContent):
        self.main_window.content = screenContent
        self.main_window.show()    

def main():
    return WordleSolver()

#  ~~~~~  Must do before releasing to play store  ~~~~~  #
    # Fix text not fitting on home screen ~~ :D ~~

#  ~~~~~  Like to do before releasing to play store  ~~~~~  #
    # Play wordle, jump to next box after entering a letter ~~ :D ~~
    # Play wordle, on clicking a box, set cursor to the start ~~ Don't seem to be able to move the cursor with Toga ~~
    # Cause errors to not send back to the home screen ~~ :D ~~
    # Add back buttons to playWordle and solver screens ~~ :D ~~
    # Allow players to input their own word choices and results so far ~~ :D ~~
    # Fix long initial load times --> what's actually causing that delay? Try profile it.
    # Make it work on Windows 
    # 2nd letter only highlight if it is in the word twice.

#  ~~~~~  Would like to do  ~~~~~  #
    # putting GUI stuff on a separate thread. It's all single-threaded atm (done kinda)
    # Make it work for landscape, or enforce portrait mode --> only play wordle doesn't fit landscape
    # Nicer won and loss screens
    # An app logo