import csv
import re
import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
from unidecode import unidecode
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download(["vader_lexicon", "punkt", "stopwords"])

def cleanTextData(text):
    cleaned_text = text.lower() # lowercase string
    cleaned_text = re.sub(r'[^\w\s.,!?\'":;()\[\]{}—–-]+|\s+', ' ', cleaned_text) # remove special characters except punctuation
    cleaned_text = unidecode(cleaned_text) # replace accented characters
    return cleaned_text

# def removeStopWords(words):
#     stop_words = set(stopwords.words("english"))
#     filteredWords = []
#     for word in words:
#         if word not in stop_words:
#             filteredWords.append(word)
#     return filteredWords


# def lemmatizeData(words):
#     lemmatizer = WordNetLemmatizer()
#     lemmatized_words = []
#     for word in words:
#         lemmatized_words.append(lemmatizer.lemmatize(word))
#     return lemmatized_words


# get number of unique words
def uniqueWords(text):
    unique = set()
    for word in text.split():
        if word not in unique:
            unique.add(word)
    return len(unique)


# get number of punctuations
import string
def getNumpunctuation(text):
    punctCount = 0
    for c in text:
        if c in string.punctuation:
            punctCount += 1
    return punctCount


def cleanData(inputBotFilePath, inputHumanFilePath, outputFilePath):
    with open(outputFilePath, 'w', newline='') as outputFile:
        writer = csv.writer(outputFile)
        
        with open(inputBotFilePath, 'r', encoding="latin1") as file1:
            csvreader = csv.reader(file1)
            
            for row in csvreader:
                text = cleanTextData(row[0])
                text_length = len(text)
                text_unique_words = uniqueWords(text)
                text_num_punctuation = getNumpunctuation(text)
                
                sia = SentimentIntensityAnalyzer()
                sia_result = sia.polarity_scores(text)
                text_sentiment_neg = sia_result['neg']
                text_sentiment_neu = sia_result['neu']
                text_sentiment_pos = sia_result['pos']
                
                writer.writerow([text, text_length, text_unique_words, text_num_punctuation, text_sentiment_neg, text_sentiment_neu, text_sentiment_pos, 1])
        
        with open(inputHumanFilePath, 'r', encoding="latin1") as file2:
            csvreader = csv.reader(file2)
            
            for row in csvreader:
                text = cleanTextData(row[0])
                text_length = len(text)
                text_unique_words = uniqueWords(text)
                text_num_punctuation = getNumpunctuation(text)
                
                sia = SentimentIntensityAnalyzer()
                sia_result = sia.polarity_scores(text)
                text_sentiment_neg = sia_result['neg']
                text_sentiment_neu = sia_result['neu']
                text_sentiment_pos = sia_result['pos']
                
                writer.writerow([text, text_length, text_unique_words, text_num_punctuation, text_sentiment_neg, text_sentiment_neu, text_sentiment_pos, 0])


cleanData("../data/wiki-bot-text.csv", "../data/wiki-human-text.csv", "../data/cleaned-wiki-text.csv")
# cleanData("../data/bot-wiki-intro.csv", "../data/human-wiki-intro.csv", "../data/cleaned-wiki-intro-lem.csv")