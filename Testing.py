from solver import *

#This project is just for FUN. The testing here is minimal. 

class Testing:
    def __init__(self):
        self.wordsLostTo = ['jolly', 'match', 'paste', 'silly', 'watch', 'safer', 'pound', 'taste', 'light', 'vaunt', 'wight', 'wound', 'spore', 'shave', 'willy']
        #self.wordsLostTo = ['foyer', 'goner', 'homer', 'boxer']
        self.db = WordleDB()   
        #self.wordsLostTo = ['joker', 'match', 'paste', 'watch', 'safer', 'taste']

    def TestWordsLostTo(self):
        self.words = self.db.GetAnswers()
        lookup = DetermineNumberOfOccurrences(self.words)
        scores = []
        for word in self.wordsLostTo:
            guesses = RunGame(self.words, lookup, word, self.db)
            scores.append(guesses)
            print("\n", 50 * '-', "\n")
        print("\n\nNUMBER OF GUESSES FOR EACH WORD:\n", scores)

    def TestAllWords(self):
        self.words = self.db.GetAnswers()
        lookup = DetermineNumberOfOccurrences(self.words)
        scores = []
        count = 0
        for word in self.words:
            guesses = RunGame(self.words, lookup, word, self.db)
            scores.append(guesses)
            if (guesses > 6):
                print(word, "This word failed taking", guesses, "guesses")
            count += 1
            if count % 20 == 0:
            #if count > 1460: 
                print("just finished number", count)

        print("\n\nRESULTS:\n", scores)
        print("\nAverage: ", sum(scores)/len(scores))
        print("\nNum losses: ", len([k for k in scores if k > 6]))
    
    def TestOneWord(self):
        ii = -336
        
        self.words = self.db.GetAnswers()
        lookup = DetermineNumberOfOccurrences(self.words)
        print("word is: ", self.words[ii])
        res = RunGame(self.words, lookup, self.words[ii], self.db)
        print("\n\nTOOK: ", res, " GUESSES")

    def TestGetAllLettersFilter(self):
        allowedWords = self.db.GetAllowedWords()

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


    def TestGetLetterCombinations(self):
        result = GetLetterCombinations([['a', 'b'], ['c', 'd']], 5)
        print(f"Result from using the letters [['a', 'b'], ['c', 'd']]: {result}")
        result = GetLetterCombinations([['a', 'b'], ['c'], ['d']], 5)
        print(f"Result from using the letters [['a', 'b'], ['c'], ['d']]: {result}")
        result = GetLetterCombinations([['a', 'b'], ['c'], ['d', 'e', 'f']], 5)
        print(f"Result from using the letters [['a', 'b'], ['c'], ['d', 'e', 'f']]: {result}")
    

    def TestProcessLeastCommonLetters(LCLetters):
        combinations = ProcessLeastCommonLetters([['a', 'b'], ['c', 'd'], ['e', 'f']])
        print(combinations)
        #TODO should really do asserts here

#Testing().TestWordsLostTo()
#Testing().TestGetAllLettersFilter()
Testing().TestAllWords()
#Testing().TestGetLetterCombinations()
#Testing().TestOneWord()
#Testing().TestProcessLeastCommonLetters()