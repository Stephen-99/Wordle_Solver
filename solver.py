from operator import eq
import random
import requests
import time
import csv
import pymongo
import certifi
import time
from pathlib import Path
from bs4 import BeautifulSoup

#TODO restructure to put stuff in different files.
#Especially the classes. 
#Seperate out different types of logic, maybe like the web connection from the rest.

#Then piece at a time cleanup the comments.

#TODO LIST
    # - Make the variety word work to completion
    # - Instead of randomly generated word, interface with the wordle site
    # - Make the solver avialable giving 1 word at a time, and getting the result from the user.
    # - Make that work through a simple GUI
    # - Allow the user to play it as a game by randomly selecting a word


def main():
    words, allowedWords = GetWords()

    #TEST WORD UPDATE THIS TO EITHER
        #Scrape from webpage
        #randomly pick a word
        #OR DON'T USE A WORD
            #Learn results of accuracy by trying guess in the online game
    TESTWORD = GetRandomWord(words)
    #TESTWORD = "silly"
    print("Randomly selected word is:", TESTWORD)
    
    commonalityLookup = DetermineNumberOfOccurrences(words)
    print("Took ", RunGame(words, commonalityLookup, TESTWORD), "guesses")

    #Testing().TestWordsLostTo()
    Testing().TestGetAllLettersFilter()
    #TODO:
        # print out with colours (yellow and green)
        # add the option for the user to play, making their own guesses
        # try input guesses into the actual site
            # otherwise just scrape for the answer and use that.
        # add option for user to play for a random word, or the offical word of the day

#TODO: 
    # Use the allowed words to pick a variety word
    # Use db filtering to determine which words are still valid after a guess etc.
        # This should involve an update to the Guess class

def ConnectToDB():
    with open("password") as passFile:
        password = passFile.readline()

    cert = certifi.where()
    client = pymongo.MongoClient("mongodb+srv://admin:" + password + "@wordlesolver.u6oi1ao.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=cert)
    return client.wordle

def GetAnswers():
    db = ConnectToDB()
    answers = db["answers"]
    
    return [doc["word"] for doc in answers.find({})]

def UpdateDB():
    db = ConnectToDB()
    lastUpdateCollection = db["lastUpdate"]
    lastUpdate = lastUpdateCollection.find_one({})["lastUpdate"]
    curTime = time.time()
    
    if ((lastUpdate - curTime) / 3600 / 24)  > 7:
        lastUpdateCollection.insert_one({"lastUpdate": time.time()})
        answers, allowedWords = ScrapeWebpage()
        UpdateAnswers(answers)
        UpdateAllowedWords(allowedWords)

        return answers, allowedWords
    return None, None

def GetWords():
    answers, allowedWords = UpdateDB()
    if (not answers):
        answers = GetAnswers()
        allowedWords = GetAllowedWords()
    return answers, allowedWords

def UpdateAnswers(words):
    db = ConnectToDB()
    answers = db["answers"]
    dbWords = [doc["word"] for doc in answers.find({})]
    dbDict = dict.fromkeys(dbWords)
    
    wordsNotFound = []
    for word in words:
        try:
            #check if word exists, if it does assign its value to true
            dbDict[word]
            dbDict[word] = True
        except KeyError:
            wordsNotFound.append({"word": word})

    if len(wordsNotFound) != 0:
        answers.insert_many(wordsNotFound)
    print("Num words to add:", len(wordsNotFound))

    wordsToRemove = []
    for word, allowedWord in dbDict.items():
        if not allowedWord:
            wordsToRemove.append(word)
    
    if len(wordsToRemove) == 0:
        return

    deleteQuery = {"word": {"$in": wordsToRemove}}
    answers.delete_many(deleteQuery)

def UpdateAllowedWords(words):
    db = ConnectToDB()
    allowedWords = db["allowedWords"]
    
    dbWords = [doc["word"] for doc in allowedWords.find({})]
    dbDict = dict.fromkeys(dbWords)
    
    wordsNotFound = []
    for word in words:
        try:
            #check if word exists, if it does assign its value to true
            dbDict[word]
            dbDict[word] = True
        except KeyError:
            wordsNotFound.append({"word": word})

    if len(wordsNotFound) != 0:
        allowedWords.insert_many(wordsNotFound)

    wordsToRemove = []
    for word, allowedWord in dbDict.items():
        if not allowedWord:
            wordsToRemove.append(word)
    
    if len(wordsToRemove) == 0:
        return

    deleteQuery = {"word": {"$in": wordsToRemove}}
    allowedWords.delete_many(deleteQuery)


def GetAllowedWords():
    db = ConnectToDB()
    allowedWords = db["allowedWords"]
    
    return [doc["word"] for doc in allowedWords.find({})]

def ScrapeWebpage():
    words = ScrapeAnswers()
    allowedWords = ScrapeAllowedWords()
    return words, allowedWords

def ScrapeAnswers():
    url = 'https://www.wordunscrambler.net/word-list/wordle-word-list'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    wordsHtml = soup.findAll('li', {'class': 'invert light'})    
    return [htmlWord.text.strip() for htmlWord in wordsHtml]

def ScrapeAllowedWords():
    url = "https://github.com/tabatkins/wordle-list/blob/main/words"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    wordsHtml = soup.findAll('td', {'class': 'blob-code blob-code-inner js-file-line'})
    words = [word.text.strip() for word in wordsHtml]
    return words

def DetermineNumberOfOccurrences(words):
    charsLookup = CharCommonality()
    charsLookup.AddCommonality(words)
    return charsLookup

def CharOccurrencesInWord(word):
    charCount = {}
    for char in word:
        if char in charCount:
            charCount[char] += 1
        else:
            charCount[char] = 1
    return charCount

def DetermineGuess(commonalityLookup, words):
    #TODO Won't need to return bestScore once all setup
    bestScore = 0
    bestWord = []
    for word in words:
        score = commonalityLookup.RetriveCommonality(word)
        if score > bestScore:
            bestScore = score
            bestWord = [word]
        elif score == bestScore:
            bestWord.append(word)
    print("bestGuesses:", bestWord)

    #TODO vary these 2 parameters and see what gives the best overall score.
    if len(bestWord) >= 3 and len(words) < 20:
        #a commonality score for this word won't make sense, as some of the letters might be missing
        return Guess(PickVarietyWord(commonalityLookup, len(bestWord))), 0

    return Guess(bestWord[0]), bestScore

def FiveLetterCombinations(letters):
    if len(letters) == 5:
        return letters
    #return _LetterCombinationsRec(letters, 0, 5)
    return _LCR(letters, combs=[])
    
    """ OLD iterative solution. Backup for if there is issues with the recursive soln.
    combinations = []
    for ii in range(len(letters) - 4):
        for jj in range(ii+1, len(letters) - 3):
            for kk in range(jj+1, len(letters) - 2):
                for ll in range(kk+1, len(letters) - 1):
                    for mm in range(ll+1, len(letters)):
                        combinations.append([letters[ii], letters[jj], letters[kk], letters[ll], letters[mm]])
    return combinations
    """


def _LCR(letters, max=5, pos=0, curIdx=0, combs = [], curLetters = []):
    if (max-pos) == 0:
        combs.append(curLetters.copy())
        return combs

    for ii in range(curIdx, len(letters) - (max-pos-1)):
        curLetters.append(letters[ii])
        combs = _LCR(letters, max, pos+1, ii+1, combs, curLetters)
        del curLetters[-1]
    return combs


#TODO Query the allowed word db for words containing specific letters.
    #Example query: 
        # {$and: [{word: {$regex: 'e.*e.*e'}}, {word: {$regex: 'b'}}]}
        #can and each letter to find together. multiple instances of the same letter need special handling
#This method does come with a performance hit due to hitting the db, but it doesn't typically happen that often so its ok
    #The delay isn't too bad, still < 1sec. just adds up in tests when they all happen back-to-back
def PickVarietyWord(lookup, numWords):
    #may want to just pick most variety from the best guesses, may want to pick the best variety from all letters

    print("\nLooking for the least common letters:")
    letters = lookup.GetLeastCommonLetters(numWords)
    print(letters, "\n")

    if len(letters) == 0:
        return "test non standard length word"

    db = ConnectToDB()
    allowedWords = db["allowedWords"]
    
    filter = "{"
    if len(letters[0]) >= 5:
        #use a filter for every combination of 5 letters.
        #filer = {$or: [{5-letter comb}, {}, {}...]}

        #if len == 5, might not won't this. Is a singular statement inside an or valid?
            # a singular or is valid so this is fine
        filter += "'$or': ["
        fiveLetterCombs = FiveLetterCombinations(letters[0])
        print(fiveLetterCombs)
        for fiveLetterComb in fiveLetterCombs:
            #TODO make sure this filter gets formed up properly.
            filter += GetAllLetterFilter(letters[0])
            pass

    elif len(letters) > 1:
        #use all the letters in all the sections but the last one
            #supplement to 5 letters from the last section. Make an or query using all such 5-letter combinations
        pass
    else:
        #less than 5 leastCommonLetters, just make a query with the letters we have
        pass

    #TODO if it fails to find a valid, word need to relax the conditon to 4 letters.
        #should be able to make a loop for the flexibility of reducing number of letters required until we get an answer
        #as we decrease required letters the number of combinations increases a lot
            #but if we had lot of letters to start with, the likelihood that we need to relax the condition is less.
    
    '''
    filter = "{'$and': ["

    for ii in range(min(len(letters[0]), 5)-1):

        filter += "{'word': {'$regex': '" + letters[0][ii] + "'}}, "
    filter += "{'word': {'$regex': '" + letters[0][min(len(letters[0])-1, 4)] + "'}}]}"
    '''
    
    filter = GetAllLetterFilter(letters[0])

    #TODO: works! but sometimes doesn't find any matching words. Want to consider looking at 2nd least common letters or even relaxing it to less letters.
    varietyWord = allowedWords.find_one(eval(filter))
    print("VARIETYWORD:\n\n", varietyWord, "\n\n")

    if not varietyWord:
        return "COULDN'T GET A VARIETY WORD :C"
    return varietyWord["word"]
    #Different idea is to go through the valid words, keep track of the ones that contain the most of the letters we want.
        #exit as soon as there is one word with 5 of the letters we want
        #will need to check as we go also using the letters in letters[1] and letters[2] in case none match perfectly
            #maybe have some sort of score to give them, and keep track of the best word
        #Maybe I can filter the allowed words list with a regex?

#TODO verify this works. Test it with a combo that should return a word, and one that shouldn't
def GetAllLetterFilter(letters):
    filter = "{'$and': ["

    for ii in range(min(len(letters), 5)-1):

        filter += "{'word': {'$regex': '" + letters[ii] + "'}}, "
    filter += "{'word': {'$regex': '" + letters[min(len(letters)-1, 4)] + "'}}]}"

    return filter


def FilterWords(words, guess):
    return [word for word in words if guess.ConsistentWithGuess(word)]

def GetRandomWord(words):
    return random.choice(words)

def RunGame(validWords, commonalityLookup, answer):
    try:
        guess, score = DetermineGuess(commonalityLookup, validWords)
    except InvalidWordLength as e:
        print(e.message)
        return
    print("Best guess is:", guess.word, " With a score of:", score)
    correctGuess = guess.ValidateGuess(answer)
    guesses = 1
    while not correctGuess:
        validWords = FilterWords(validWords, guess)
        commonalityLookup = DetermineNumberOfOccurrences(validWords)
        try:
            guess, score = DetermineGuess(commonalityLookup, validWords)
        except InvalidWordLength as e:
            print(e.message)
            return
        print("Best guess is:", guess.word, " With a score of:", score)
        correctGuess = guess.ValidateGuess(answer)
        guesses += 1
        #print(validWords)
    return guesses

class Testing:
    def __init__(self):
        self.wordsLostTo = ['foyer', 'goner', 'homer', 'jolly', 'patch', 'pound', 'saner', 'shave', 'silly', 'swore', 'taste', 'tight', 'vaunt', 'waste', 'watch', 'wight', 'willy', 'wound']

    def TestWordsLostTo(self):
        self.words = GetAnswers()
        lookup = DetermineNumberOfOccurrences(self.words)
        for word in self.wordsLostTo:
            guesses = RunGame(self.words, lookup, word)
            print("took", guesses, "guesses\n")

    def TestGetAllLettersFilter(self):
        db = ConnectToDB()
        allowedWords = db["allowedWords"]

        #5 letters with no valid words
        filter = GetAllLetterFilter(['a', 'b', 'c', 'd', 'e'])
        res = allowedWords.find_one(eval(filter))
        assert res == None
        
        #5 letters with one valid word
        filter = GetAllLetterFilter(['a', 'i', 'u', 'd', 'e'])
        res = allowedWords.find_one(eval(filter))
        assert res['word'] == 'adieu'


    #just prints what the results were for future reference.
    def LookupUpdateImpact(self):
        print("avg with lookup updates: 3.692")
        print("avg without lookup updates: 3.810")

        print("Number of times lookup was better:", 738)
        print("Number of times without lookup was better:", 565)
        print("Number of times they were equal:", 1006)
        print("Number of times lookup lost:", 18)
        print("Number of times without lookup lost:", 36)


class Guess:
    def __init__(self, word):
        #TODO seems like a bad idea to have an exception in the constructor maybe make a GuessFactory to perform injection
        if (len(word) != 5):
            raise InvalidWordLength()
        self.word = word
        self.correct = [False, False, False, False, False]
        self.misplaced = [False, False, False, False, False]
        self.incorrect = [False, False, False, False, False]

    def ValidateGuess(self, correctWord):
        for ii in range(len(self.word)):
            if self.word[ii] == correctWord[ii]:
                self.correct[ii] = True
            elif self.word[ii] in correctWord:
                self.misplaced[ii] = True
            else:
                self.incorrect[ii] = True

        if False not in self.correct:
            return True
        return False
    
    def ConsistentWithGuess(self, word):
        for ii in range(len(word)):
            if self.correct[ii] and (self.word[ii] != word[ii]):
                return False
            if self.incorrect[ii] and (self.word[ii] in word):
                return False
            if self.misplaced[ii] and ((self.word[ii] == word[ii]) or (self.word[ii] not in word)):
                return False
        return True

class CharCommonality:
    def __init__(self):
        #First one is number of words with that char, 2nd number of words with it twice etc.
        self.dicts = [{}, {}, {}]
    
    def AddCommonality(self, words):
        for word in words:
            charCount = CharOccurrencesInWord(word)
            for char, count in charCount.items():
                for ii in range(count):
                    self._AddCharCommonality(char, ii)

    def RetriveCommonality(self, word):
        charCount = CharOccurrencesInWord(word)

        commonality = 0
        for char, count in charCount.items():
            for ii in range(count):
                commonality += self._GetCharCommonality(char, ii)
        return commonality

    def GetLeastCommonLetters(self, numWords):
        #only worth looking at the single instance of letters
        sortedList = sorted(self.dicts[0].items(), key = lambda x: x[1])

        #TODO feels like bad code. Refactor it to be better
        leastCommonLetters = []
        lastVal = 0
        ii = -1
        count = 0
        for charNVal in sortedList:
            #Is this numWords really necassary? Maybe not since why do we care about the number of best guesses when we want to whittle down all viable guesses
            if charNVal[1] >= numWords:
                break
            if (count >= 5) and (charNVal[1] > lastVal):
                break
            if (charNVal[1] > lastVal):
                leastCommonLetters.append([])
                ii += 1
            leastCommonLetters[ii].append(charNVal[0])
            count += 1
            lastVal = charNVal[1]
        return leastCommonLetters

    def _GetCharCommonality(self, char, index):
        try:
            return self.dicts[index][char]
        except (IndexError, KeyError):
            #Not in dictionary
            return 0

    def _AddCharCommonality(self, char, index):
        try:
            if char in self.dicts[index]:
                self.dicts[index][char] += 1
            else:
                self.dicts[index][char] = 1
        except IndexError:
            print("\n\nERROR:\tCouldn't add commonality for a word with the same letter", index+1, "times\n\n")


class InvalidWordLength(Exception):
    def __init__(self, length = 5, message = "Word length must be "):
        self.message = message + str(length)
        super().__init__(self.message)


if __name__ == "__main__":
    main()
