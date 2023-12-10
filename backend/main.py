import pandas as pd
import re
import nltk
nltk.download(["vader_lexicon", "punkt", "stopwords", "averaged_perceptron_tagger", "cmudict"])
from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer
from unidecode import unidecode


# clean the input text
def cleanTextData(text):
    cleaned_text = text.lower() # lowercase string
    cleaned_text = re.sub(r'[^\w\s.,!?\'":;()\[\]{}—–-]+|\s+', ' ', cleaned_text) # remove special characters except punctuation
    cleaned_text = unidecode(cleaned_text) # replace accented characters
    return cleaned_text


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


# get the average sentence length from the text
def getAverageSentenceLen(text):
    tokens = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    return len(tokens) / len(sentences)


# calculate the kincaid score (readability score) of the text
cmu_dict = nltk.corpus.cmudict.dict()
def getKincaidScore(text):
    num_sentences = len(nltk.sent_tokenize(text))
    words = text.split()
    num_words = len(words)
    syllables = 0
    
    for word in words:
        if word in cmu_dict:
            wordSyllables = len(cmu_dict[word][0])
            if wordSyllables == 0:
                syllables += 1
            else:
                syllables += wordSyllables
    
    # kincaid score = 0.39 x (words/sentences) + 11.8 x (syllables/words) – 15.59
    kincaid_score = 0.39 * (num_words / num_sentences) + 11.8 * (syllables / num_words) - 15.59
    return kincaid_score


# load the model
model = load_model('bot_human_text_detector.h5')


# API
app = Flask(__name__)
CORS(app)

# Root = endpoint to get data
@app.route("/detection", methods=["POST"])
def text_detection():
    
    # get text from the request body
    data = request.get_json()
    text = data["text"]
    
    # clean / process the text
    ctd = [(cleanTextData(text))]
    tl = [(len(text))]
    uw = [(uniqueWords(text))]
    gp = [(getNumpunctuation(text))]

    sia = SentimentIntensityAnalyzer()
    sia_result = sia.polarity_scores(text)
    text_sentiment_neg = sia_result['neg']
    text_sentiment_neu = sia_result['neu']
    text_sentiment_pos = sia_result['pos']
    sneg = [(text_sentiment_neg)]
    sneu = [(text_sentiment_neu)]
    spos = [(text_sentiment_pos)]
    
    asl = [(getAverageSentenceLen(text))]
    ks = [(getKincaidScore(text))]
    
    # create dataframe of text and its features
    text_features = {"text": ctd, "text_length":tl, "unique_words":uw, "punctuation":gp, "sia_neg":sneg, "sia_neu":sneu, "sia_pos":spos, "avg_sent_len":asl, "kincaid_score":ks}
    df = pd.DataFrame(text_features)
    
    vectorizer = TfidfVectorizer(max_features=10000)

    # convert text into integers / floating point values || extract features
    text_extracted_features = vectorizer.fit_transform(df["text"])

    # add padding to the extracted features (need padding inorder for consistency and for input text features to work with the model)
    padded_extracted_features = pad_sequences(text_extracted_features.toarray(), maxlen=10000, dtype="float32", padding="post", value=0.0)
    
    # convert extracted features into a dataframe
    extract_features_df = pd.DataFrame(padded_extracted_features)
    
    # combine extracted features with original features
    complete_features = pd.concat([extract_features_df, df[["text_length", "unique_words", "punctuation", "sia_neg", "sia_neu", "sia_pos", "avg_sent_len", "kincaid_score"]]], axis=1)
    
    # make prediction using the model with the complete text features as input
    prediction = model.predict(complete_features)
    
    pred_result = prediction[0][0]
    
    bot_probability = pred_result
    human_probability = 1 - pred_result

    result = {
        "bot" : str(bot_probability),
        "human" : str(human_probability)
    }
    
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)