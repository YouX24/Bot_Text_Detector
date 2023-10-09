import csv
import re
import nltk
nltk.download('punkt')
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def cleanTextData(text):
    text = text.lower() # lowercase string
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text) # remove special chars
    text = re.sub(r'\d+', '', text) # remove numbers
    wordsInText = word_tokenize(text) # tokenization
    filteredTextData = removeStopWords(wordsInText) # remove stop words
    lemmatizedTextData = lemmatizeData(filteredTextData) # lemmatization
    return " ".join(lemmatizedTextData)


def removeStopWords(words):
    stop_words = set(stopwords.words("english"))
    filteredWords = []
    for word in words:
        if word not in stop_words:
            filteredWords.append(word)
    return filteredWords


def lemmatizeData(words):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = []
    for word in words:
        lemmatized_words.append(lemmatizer.lemmatize(word))
    return lemmatized_words


def cleanData(inputFilePath, outputFilePath):
    with open(outputFilePath, 'w', newline='') as outputFile:
        writer = csv.writer(outputFile)
        
        with open(inputFilePath, 'r', encoding="latin1") as file:
            csvreader = csv.reader(file)
            
            for row in csvreader:
                writer.writerow([cleanTextData(row[0])])
                


cleanData("data/twitter-human-text.csv", "data/cleaned-twitter-human-text.csv")
cleanData("data/wiki-bot-text.csv", "data/cleaned-wiki-bot-text.csv")
cleanData("data/wiki-human-text.csv", "data/cleaned-wiki-human-text.csv")