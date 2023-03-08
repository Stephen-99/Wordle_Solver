class CharCommonality:
    def __init__(self):
        #First one is number of words with that char, 2nd number of words with it twice etc.
        self.dicts = [{}, {}, {}]
    
    def AddCommonality(self, words):
        for word in words:
            charCount = CharCommonality.CharOccurrencesInWord(word)
            for char, count in charCount.items():
                for ii in range(count):
                    self._AddCharCommonality(char, ii)

    def RetriveCommonality(self, word):
        charCount = CharCommonality.CharOccurrencesInWord(word)

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
            #if charNVal[1] >= numWords:
                #break
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

    def CharOccurrencesInWord(word):
        charCount = {}
        for char in word:
            if char in charCount:
                charCount[char] += 1
            else:
                charCount[char] = 1
        return charCount
