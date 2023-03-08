#For any access to the websites.. Maybe rename to WebInterface?
    #NO have a separte one for interacting with the wordle site.
from bs4 import BeautifulSoup
import requests


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