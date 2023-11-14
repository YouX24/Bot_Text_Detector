import csv
import re
import nltk
nltk.download('punkt')
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode


def cleanTextData(text):
    cleaned_text = text.lower() # lowercase string
    # cleaned_text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text) # remove ALL special chars
    cleaned_text = re.sub(r'[^\w\s.,!?\'":;()\[\]{}—–-]+|\s+', ' ', cleaned_text) # remove special characters except punctuation
    # cleaned_text = re.sub(r'\d+', '', text) # remove numbers
    cleaned_text = unidecode(cleaned_text) # replace accented characters
    wordsInText = word_tokenize(cleaned_text.strip()) # tokenization    # filteredTextData = removeStopWords(wordsInText) # remove stop words
    lemmatizedTextData = lemmatizeData(wordsInText) # lemmatization
    return " ".join(lemmatizedTextData) # remove any spaces from front and end of text, return


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


def cleanData(inputBotFilePath, inputHumanFilePath, outputFilePath):
    with open(outputFilePath, 'w', newline='') as outputFile:
        writer = csv.writer(outputFile)
        
        with open(inputBotFilePath, 'r', encoding="latin1") as file1:
            csvreader = csv.reader(file1)
            
            for row in csvreader:
                writer.writerow([cleanTextData(row[0]), 'bot'])
        
        with open(inputHumanFilePath, 'r', encoding="latin1") as file2:
            csvreader = csv.reader(file2)
            
            for row in csvreader:
                writer.writerow([cleanTextData(row[0]), 'human'])


# cleanData("../data/wiki-bot-text.csv", "../data/wiki-human-text.csv", "../data/cleaned-wiki-text.csv")
# cleanData("../data/bot-wiki-intro.csv", "../data/human-wiki-intro.csv", "../data/cleaned-wiki-intro-lem.csv")