#HAve to think do I maybe instead want to decouple this so that the solver doesn't have anything to do with the eventSystem
#Otherewise I have to worry about wrapping every little edge case. Solver causes most of the events, makes sense for it to raise them
from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *

from .Guess import *
from .CharCommonality import *
from .Database import *
from .WebScraper import *

# TODO LIST
# - Instead of randomly generated word, interface with the wordle site (de-prioritised)
# - Allow the user to play it as a game by randomly selecting a word
# - Make an exe for easy windows deployment
# - Create a GUI pop up for errors instead of print statements
# - Make a mobile deployment (BeeWare)
# - Make database accessible from any device (only for reading though)
# - Ability to use the solver mid way when some guesses have already been made
    # have a 'different guess used button or something

class WordleSolver:
    def __init__(self):
        self.db = WordleDB()
        self.validWords, self.allowedWords = self.db.GetWords()
        self.lookup = CharCommonality(self.validWords)
        self.curGuess = None
        self.guesses = 0

    def resetSolver(self):
        self.validWords, self.allowedWords = self.db.GetWords()
        self.lookup = CharCommonality(self.validWords)
        self.curGuess = None
        self.guesses = 0

    def GetNextGuess(self):
        try:
            self.curGuess, score = self.DetermineGuess()
        except InvalidWordLength as e:
            print(e.message)
            EventSystem.EventOccured(ErrorOccuredEvent(e.message))
            return
        except IndexError as err:
            print("Invalid selection. There are no valid words left.")
            EventSystem.EventOccured(ErrorOccuredEvent("Invalid selection. There are no valid words left."))
            return

        #    print("Best guess is:", guess.word, " With a score of:", score)

        EventSystem.EventOccured(NewWordEvent(self.curGuess.word))
        #TODO: can maybe remove this return
        return self.curGuess.word

    def ProcessGuessResults(self, res: list[LetterColour]):
        if res == None:
            #This shouldn't be possible.
            print("\n\n~~~WHAT HAPPENED HERE?!~~~\n\n")
            EventSystem.EventOccured(ReturnToMainMenuEvent())
            return

        self.guesses += 1
        correctGuess = self.curGuess.UserValidateGuess(res)
        if correctGuess:
            #This should never happen. They should press the correct guess button!
            EventSystem.EventOccured(ErrorOccuredEvent("You got the correct answer!"))
            return

        self.FilterWords()
        self.DetermineNumberOfOccurrences()
        
        #TODO: can maybe remove this return
        return self.GetNextGuess()

    def DetermineGuess(self) -> tuple[Guess, int]:
        # TODO Won't need to return bestScore once all setup
        bestScore = 0
        bestWord = []
        for word in self.validWords:
            score = self.lookup.RetriveCommonality(word)
            if score > bestScore:
                bestScore = score
                bestWord = [word]
            elif score == bestScore:
                bestWord.append(word)
        #print("bestGuesses:", bestWord, "    Remaining number of valid words:", len(self.validWords))

        try:
            if len(bestWord) >= 2 and 2 < len(self.validWords) < 7:
                # a commonality score for this word won't make sense, as some of the letters might be missing
                return Guess(self.PickVarietyWord(minLetters=2)), 0
            if len(bestWord) >= 4 and 3 < len(self.validWords) < 11:
                return Guess(self.PickVarietyWord(minLetters=4)), 0
            if len(bestWord) >= 4 and 11 < len(self.validWords) < 20:
                return Guess(self.PickVarietyWord(minLetters=5)), 0
        except InvalidWordLength as e:
            pass

        return Guess(bestWord[0]), bestScore
    
    def PickVarietyWord(self, minLetters: int = 2) -> str:
        # print("Looking for the least common letters:")
        letters = self.lookup.GetLeastCommonLetters(self.validWords)

        # print(letters)

        if len(letters) < 2:
            return "A variety word is not helpful here"

        letterCombs = ProcessLeastCommonLetters(letters)

        ii = min(5, len(letterCombs[0]))
        varietyWord = None
        while not varietyWord and ii >= minLetters:
            varietyWord = self.TryGetVarietyWord(letterCombs, ii)
            ii -= 1

        # Should never trigger but you know how things go
        if not varietyWord:
            return "Non-standard word length"

        return varietyWord["word"]
    
    def TryGetVarietyWord(self, lettersOptionsByWord: list[list[str]], maxLetters: int) -> str:
        letterCombs = []
        for letters in lettersOptionsByWord:
            letterCombs.extend(GetLetterCombinations(letters, maxLetters))

        filter = GetFilterForCombinations(letterCombs)
        return self.db.FindOneAllowedWord(filter)
    
    def FilterWords(self) -> list[str]:
        self.validWords = [word for word in self.validWords if self.curGuess.ConsistentWithGuess(word)]

    def DetermineNumberOfOccurrences(self):
        self.lookup = CharCommonality(self.validWords)



# converts them from a per word basis to a list of letter combinations.
# GetLetterCombinations can then take these and convert them to combinations based on the number of required letters
# like a 5 choose 3 type situation.
def ProcessLeastCommonLetters(LCLetters: list[list[str]]) -> list[list[str]]:
    letterCombs = []
    for letter in LCLetters[0]:
        if len(LCLetters) > 1:
            combs = ProcessLeastCommonLetters(LCLetters[1:])
            for comb in combs:
                comb.append(letter)
                letterCombs.append(comb)
        else:
            letterCombs.append([letter])
    return letterCombs


def GetLetterCombinations(letters: list[str], maxLetters: int) -> list[list[str]]:
    if len(letters) >= maxLetters:
        return LetterCombinations(letters, maxLetters)

    # This will occur if there are less letters then the given maxLetters
    return LetterCombinations(letters, len(letters))

def LetterCombinations(letters: list[str], max: int = 5) -> list[list[str]]:
    if len(letters) == max:
        return [letters]
    return _LCR(letters, max, combs=[])


def _LCR(
    letters: list[str],
    max: int = 5,
    pos: int = 0,
    curIdx: int = 0,
    combs: list[list[str]] = [],
    curLetters: list[str] = [],
) -> list[list[str]]:
    if (max - pos) == 0:
        combs.append(curLetters.copy())
        return combs

    for ii in range(curIdx, len(letters) - (max - pos - 1)):
        curLetters.append(letters[ii])
        combs = _LCR(letters, max, pos + 1, ii + 1, combs, curLetters)
        del curLetters[-1]
    return combs


def GetFilterForCombinations(combinations: list[list[str]]) -> str:
    if len(combinations) == 1:
        return GetAllLetterFilter(combinations[0])

    filter = "{"
    filter += "'$or': ["
    for combination in combinations:
        filter += GetAllLetterFilter(combination)
        filter += ", "
    filter = filter[:-2] + "]}"
    return filter


def GetAllLetterFilter(letters: list[str]) -> str:
    filter = "{'$and': ["

    for ii in range(min(len(letters), 5) - 1):

        filter += "{'word': {'$regex': '" + letters[ii] + "'}}, "
    filter += "{'word': {'$regex': '" + letters[min(len(letters) - 1, 4)] + "'}}]}"

    return filter


