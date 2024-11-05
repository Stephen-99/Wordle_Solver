# For any access to the DB.
# Should maybe be a class
import time
import certifi
import pymongo
import dns.resolver as dns_res
import os

from .WebScraper import *

class WordleDB:
    def __init__(self):
        dns_res.default_resolver=dns_res.Resolver(configure=False)
        dns_res.default_resolver.nameservers=['8.8.8.8']
        self.db = self.ConnectToDB()

    def ConnectToDB(self) -> pymongo.database.Database:
        #with open("C:/Dev/Wordle_Solver/WordleSolver/src/WordleLibrary/password") as passFile:
        #    password = passFile.readline()
        password = "4BiCaHWwA25bwHSS"

        cert = certifi.where()
        client = pymongo.MongoClient(
            #"mongodb+srv://admin:"
            "mongodb+srv://user:"
            + password
            + "@wordlesolver.u6oi1ao.mongodb.net/?retryWrites=true&w=majority",
            tls=True,
            tlsCAFile=cert,
        )
        return client.wordle

    def GetAnswers(self) -> list[str]:
        answers = self.db["answers"]

        return [doc["word"] for doc in answers.find({})]

    def UpdateDB(self) -> tuple[list[str], list[str]]:
        lastUpdateCollection = self.db["lastUpdate"]
        lastUpdate = lastUpdateCollection.find_one({})["lastUpdate"]
        curTime = time.time()

        if ((lastUpdate - curTime) / 3600 / 24) > 7:
            lastUpdateCollection.insert_one({"lastUpdate": time.time()})
            answers, allowedWords = ScrapeWebpage()
            self.UpdateAnswers(answers)
            self.UpdateAllowedWords(allowedWords)

            return answers, allowedWords
        return None, None

    def GetWords(self) -> tuple[list[str], list[str]]:
        #answers, allowedWords = self.UpdateDB()
        #if not answers:

        #Time overhead is in the initial request to db. the 2nd request is always faster
        #This also shows the 2nd time the db is hit for the words lists. It's faster.
            #like a wakeup tiem for the db
        t1 = time.perf_counter(), time.process_time()
        allowedWords = self.GetAllowedWords()
        t2 = time.perf_counter(), time.process_time()
        print("get allowed words:")
        print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
        print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
        print()

        t1 = time.perf_counter(), time.process_time()
        answers = self.GetAnswers()
        t2 = time.perf_counter(), time.process_time()
        print("Get answers:")
        print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
        print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
        print()

        return answers, allowedWords
        #TODO: run these in parallele maybe
        #return self.GetAnswers(), self.GetAllowedWords()

    def UpdateAnswers(self, words: list[str]):
        answers = self.db["answers"]
        dbWords = [doc["word"] for doc in answers.find({})]
        dbDict = dict.fromkeys(dbWords)

        wordsNotFound = []
        for word in words:
            try:
                # check if word exists, if it does assign its value to true
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

    def UpdateAllowedWords(self, words: list[str]):
        allowedWords = self.db["allowedWords"]

        dbWords = [doc["word"] for doc in allowedWords.find({})]
        dbDict = dict.fromkeys(dbWords)

        wordsNotFound = []
        for word in words:
            try:
                # check if word exists, if it does assign its value to true
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

    def GetAllowedWords(self) -> list[str]:
        allowedWords = self.db["allowedWords"]

        return [doc["word"] for doc in allowedWords.find({})]

    def FindOneAllowedWord(self, filter: str) -> str:
        allowedWords = self.db["allowedWords"]
        try:
            return allowedWords.find_one(eval(filter), batch_size=10)
        except Exception as e:
            print("ERROR:", e)
