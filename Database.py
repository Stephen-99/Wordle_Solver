#For any access to the DB.
#Should maybe be a class
import time
import certifi
import pymongo

from WebScraper import *

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

def FindOneAllowedWord(filter):
    db = ConnectToDB()
    allowedWords = db["allowedWords"]
    return allowedWords.find_one(eval(filter))