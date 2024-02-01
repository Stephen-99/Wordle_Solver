#For any access to the DB.
#Should maybe be a class
import time
import certifi
import pymongo

from WebScraper import *

class WordleDB:
    def __init__(self):
        self.db = self.ConnectToDB()

    def ConnectToDB(self):
        with open("password") as passFile:
            password = passFile.readline()

        cert = certifi.where()
        client = pymongo.MongoClient("mongodb+srv://admin:" + password + "@wordlesolver.u6oi1ao.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsCAFile=cert)
        return client.wordle

    def GetAnswers(self):
        answers = self.db["answers"]
        
        return [doc["word"] for doc in answers.find({})]

    def UpdateDB(self):
        lastUpdateCollection = self.db["lastUpdate"]
        lastUpdate = lastUpdateCollection.find_one({})["lastUpdate"]
        curTime = time.time()
        
        if ((lastUpdate - curTime) / 3600 / 24)  > 7:
            lastUpdateCollection.insert_one({"lastUpdate": time.time()})
            answers, allowedWords = ScrapeWebpage()
            self.UpdateAnswers(answers)
            self.UpdateAllowedWords(allowedWords)

            return answers, allowedWords
        return None, None

    def GetWords(self):
        answers, allowedWords = self.UpdateDB()
        if (not answers):
            answers = self.GetAnswers()
            allowedWords = self.GetAllowedWords()
        return answers, allowedWords

    def UpdateAnswers(self, words):
        answers = self.db["answers"]
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

    def UpdateAllowedWords(self, words):
        allowedWords = self.db["allowedWords"]
        
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

    def GetAllowedWords(self):
        allowedWords = self.db["allowedWords"]
        
        return [doc["word"] for doc in allowedWords.find({})]

    def FindOneAllowedWord(self, filter):
        allowedWords = self.db["allowedWords"]
        try:
            return allowedWords.find_one(eval(filter), batch_size=10)
        except Exception as e:
            print("EEROR:", e)