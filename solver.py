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

#TODO: refactor this to actually be the passed in filename, we want a different one when getting all the allwoed words
#This will become redundant when it gets shifted to the db.
filename = "words.csv"

def main():
    #TODO Currently there is hidden coupling where both the allowed and actual words get updated if the csv is > 7days old
    #This means ReadWordsFromCsv needs to happen b4 GetAllowedWords. 
    #When the validAnswers get added to the db, the scraping should appear as a separate function that will be called b4 getting the words
    words = GetAnswers()
    allowedWords = GetAllowedWords()

    

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

    Testing().TestWordsLostTo()
    #TODO:
        # print out with colours (yellow and green)
        # add the option for the user to play, making their own guesses
        # try input guesses into the actual site
            #otherwise just scrape for the answer and use that.
        # add option for user to play for a random word, or the offical word of the day


#TODO add another collection in the db and use that for accessing and filtering the words
def WriteWordsToCsv(words):
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(words)
    print("Finished writing to csv")


def ReadWordsFromCsv():
    last_modified = time.time() - Path(filename).stat().st_mtime

    #convert from seconds to days
    last_modified = last_modified / 60 / 60 / 24

    print("Csv file last modified:", round(last_modified, 2), "days ago.")
    #If its more than a week old refresh the data by scraping the page again
    if (last_modified > 7):
        return ScrapeWebpage()
    
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile)
        words = list(reader)[0]

    print("Finished reading from", filename)
    return words

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
    words = WordUnscrambler()
    UpdateAllowedWords(ScrapeAllowedWords())
    WriteWordsToCsv(words)
    return words

def WordUnscrambler():
    url = 'https://www.wordunscrambler.net/word-list/wordle-word-list'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    wordsHtml = soup.findAll('li', {'class': 'invert light'})    
    return [htmlWord.text.strip() for htmlWord in wordsHtml]

#TODO: update this to only get called on scrape webpage
    #all other calls should access the database
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

    if len(bestWord) >= 3 and len(words) < 30:
        #a commonality score for this word won't make sense, as some of the letters might be missing
        return Guess(PickVarietyWord(commonalityLookup, len(bestWord))), 0

    return Guess(bestWord[0]), bestScore

#TODO Query the allowed word db for words containing specific letters.
    #Example query: 
        # {$and: [{word: {$regex: 'e.*e.*e'}}, {word: {$regex: 'b'}}]}
        #can and each letter to find together. multiple instances of the same letter need special handling
def PickVarietyWord(lookup, numWords):
    #may want to just pick most variety from the best guesses, may want to pick the best variety from all letters

    print("\nLooking for the least common letters:")
    letters = lookup.GetLeastCommonLetters(numWords)
    print(letters, "\n")


    #Much better idea is to go through the valid words, keep track of the ones that contain the most of the letters we want.
        #exit as soon as there is one word with 5 of the letters we want
        #will need to check as we go also using the letters in letters[1] and letters[2] in case none match perfectly
            #maybe have some sort of score to give them, and keep track of the best word
        #Maybe I can filter the allowed words list with a regex?

    #if len(letters[0] >= 5):
        #for Each set of 5 letters in letters[0]:
            #if its a valid word:
                #return word
        
        #for each set of 4 letters 
            #for each letter in the alphabet:
                #for each set with the 4 letters and the letter:
                    #if its a valid word:
                        #return word


    #TODO find a valid word using these letters.
        #if its more than 5 letters, and we can't find a word with the first 5, we want to swap the last one
        #but if the second last or third last etc. have the same val we could swap with them and get more 
        #letter combinations that might give us a valid word with the same amount of variability

        #So may need to pass in the values, but better would be a way to return the letters segregated 
        #into their commonality. Maybe as a dictionary?
    #This is meant to crash the program since we assume 5 letters in a lot of places
    #could maybe look to change that though. At the least use a global constant.

    return "test non standard length word"

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
        self.words = ReadWordsFromCsv()
        lookup = DetermineNumberOfOccurrences(self.words)
        for word in self.wordsLostTo:
            guesses = RunGame(self.words, lookup, word)
            print("took", guesses, "guesses\n")


    def LookupUpdateImpact(self):
        self.words = ReadWordsFromCsv()
        resultsWith = self._withLookupUpdate()
        resultsWithout = self._withoutLookupUpdate()
        
        print("avg with lookup updates:", sum(resultsWith)/len(resultsWith))            #3.692
        print("avg without lookup updates:", sum(resultsWithout)/len(resultsWithout))   #3.810

        numWithBetter = 0
        numWithoutBetter = 0
        numEqual = 0

        withLost = []
        withoutLost = []
        for ii in range(len(resultsWith)):
            if resultsWith[ii] < resultsWithout[ii]:
                numWithBetter += 1
            elif resultsWith[ii] > resultsWithout[ii]:
                numWithoutBetter += 1
            else:
                numEqual += 1
            if resultsWith[ii] > 6:
                withLost.append(self.words[ii])
            if resultsWithout[ii] > 6:
                withoutLost.append(self.words[ii])

        print("Number of times lookup was better:", numWithBetter) #738
        print("Number of times without lookup was better:", numWithoutBetter) #565
        print("Number of times they were equal:", numEqual) #1006
        print("Number of times lookup lost:", len(withLost)) #18
        print("Number of times without lookup lost:", len(withoutLost)) #36
        print("Words lost to with lookup:", withLost)
        print("Words lost to without lookup:", withoutLost)


    def _withLookupUpdate(self):
        results = []
        lookup = DetermineNumberOfOccurrences(self.words)
        for word in self.words:
            results.append(self._runGame(self.words, lookup, word))
        return results

    def _withoutLookupUpdate(self):
        results = []
        lookup = DetermineNumberOfOccurrences(self.words)
        for word in self.words:
            results.append(self._runGameNotUpdatingLookup(self.words, lookup, word))
        return results

    def _runGame(self, validWords, commonalityLookup, answer):
        guess, score = DetermineGuess(commonalityLookup, validWords)
        correctGuess = guess.ValidateGuess(answer)
        guesses = 1
        while not correctGuess:
            validWords = FilterWords(validWords, guess)
            commonalityLookup = DetermineNumberOfOccurrences(validWords)
            guess, score = DetermineGuess(commonalityLookup, validWords)
            correctGuess = guess.ValidateGuess(answer)
            guesses += 1
        return guesses

    def _runGameNotUpdatingLookup(self, validWords, commonalityLookup, answer):
        guess, score = DetermineGuess(commonalityLookup, validWords)
        correctGuess = guess.ValidateGuess(answer)
        guesses = 1
        while not correctGuess:
            validWords = FilterWords(validWords, guess)
            guess, score = DetermineGuess(commonalityLookup, validWords)
            correctGuess = guess.ValidateGuess(answer)
            guesses += 1
        return guesses

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
