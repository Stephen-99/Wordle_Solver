import random
import requests
import time
from pathlib import Path
import csv
from bs4 import BeautifulSoup

filename = "words.csv"

def main():
    words = ReadWordsFromCsv()

    #TEST WORD UPDATE THIS TO EITHER
        #Scrape from webpage
        #randomly pick a word
        #OR DON'T USE A WORD
            #Learn results of accuracy by trying guess in the online game
    TESTWORD = GetRandomWord(words)
    #TESTWORD = "silly"
    print("Randomly selected word is:", TESTWORD)
    
    #print(words)
    commonalityLookup = DetermineNumberOfOccurrences(words)
    print("Took ", RunGame(words, commonalityLookup, TESTWORD), "guesses")

    Testing().TestWordsLostTo()
    #TODO:
        # print out with colours (yellow and green)
        # add the option for the user to play, making their own guesses
        # try input guesses into the actual site
            #otherwise just scrape for the answer and use that.
        # add option for user to play for a random word, or the offical word of the day
        # make a list of words with equal highest commonality
            #pick the word from there with the most variety of letters.


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

def ScrapeWebpage():
    words = WordUnscrambler()
    WriteWordsToCsv(words)
    return words

def WordUnscrambler():
    url = 'https://www.wordunscrambler.net/word-list/wordle-word-list'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    wordsHtml = soup.findAll('li', {'class': 'invert light'})
    words = []
    
    for htmlWord in wordsHtml:
        words.append(htmlWord.text.strip())

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


    #TODO:
    #if len(bestWord) >= 3 and len(words) < SOME LIMIT (maybe like 8)
        #then try find a new word with as many of the unique letters as possible
        #Will need a new function for this. NOTE: not all cases will have just 1 letter different
            #look for the minimum used 5 letters in the lookup, try make a word with those.
                #otherwise drop to 4, with the other letter being anything etc.

    return Guess(bestWord[0]), bestScore

def PickVarietyWord(lookup, numWords):
    #sort key value pairs from the dictionary, and pick the minimum ones to create a new word
        #do we just look at the single letters here or double too?
            #we limit it to when small number of words. The cost of including a double letter 
            #for 1 extra letter of variability is highly unlikely to pay off.
                #we limit the number of equal weighted guesses, not the number of valid words...

    print("\nLooking for the least common letters:")
    letters = lookup.GetLeastCommonLetters(numWords)
    print(letters, "\n")

    #TODO find a valid word using these letters.
        #if its more than 5 letters, and we can't find a word witht eh first 5, we want to swap the last one
        #but if the second last or third last etc. have the same val we could swap with them and get more 
        #letter combinations that might give us a valid word with the same amount of variability

        #So may need to pass in the values, but better would be a way to return the letters segregated 
        #into their commonality. Maybe as a dictionary?
    return "test non standard length word"

def FilterWords(words, guess):
    return [word for word in words if guess.ConsistentWithGuess(word)]

def GetRandomWord(words):
    return random.choice(words)

def RunGame(validWords, commonalityLookup, answer):
    guess, score = DetermineGuess(commonalityLookup, validWords)
    print("Best guess is:", guess.word, " With a score of:", score)
    correctGuess = guess.ValidateGuess(answer)
    guesses = 1
    while not correctGuess:
        validWords = FilterWords(validWords, guess)
        commonalityLookup = DetermineNumberOfOccurrences(validWords)
        guess, score = DetermineGuess(commonalityLookup, validWords)
        print("Best guess is:", guess.word, " With a score of:", score)
        correctGuess = guess.ValidateGuess(answer)
        guesses += 1
        #print(validWords)
    return guesses

class Testing:
    def __init__(self):
        self.wordsLostTo = ['foyer', 'goner', 'homer', 'jolly', 'patch', 'pound', 'saner', 'shave', 'silly', 'swore', 'taste', 'tight', 'vaunt', 'waste', 'watch', 'wight', 'willy', 'wound']

    #TODO do testing on words were it loses to see if it can be improved.
        #when theres more than 2 with only 1 letter different, try find a word which uses all the 
        #different letters and so deduce which one is in the word.
            #may need to scrape an allowed wordlist which is different than the answers list.
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
                #TODO: check if its actually better with this change, or if just adding it to count-1 was better
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
        
        #TODO return least commonLetters as a dictionary of num occurences to letters
            # we don't really care about the number of occurences though, only that they are different,
            #could just use the lastVal to check where we need to make a change and return a list of lists

        leastCommonLetters = [[]]
        lastVal = 0
        ii = 0
        for charNVal in sortedList:
            if charNVal[1] >= numWords:
                break
            if (len(leastCommonLetters) >= 5) and (charNVal[1] > lastVal):
                break
            if (charNVal[1] > lastVal):
                leastCommonLetters.append([])
                ii += 1
            leastCommonLetters[ii].append(charNVal[0])
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



if __name__ == "__main__":
    main()
