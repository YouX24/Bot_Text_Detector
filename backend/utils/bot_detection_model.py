import tensorflow as tf
import pandas as pd
import nltk
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download(["vader_lexicon", "punkt", "stopwords", "averaged_perceptron_tagger", "cmudict"])


# Load the external dataset using Pandas + add heading to each column
df = pd.read_csv('../data/cleaned-wiki-intro.csv', names=["text", "text_length", "unique_words", "punctuation", "sia_neg", "sia_neu", "sia_pos", "avg_sent_len", "kincaid_score", "target"])

# first 150,000 values are bot text, remaining 150,000 are human text.
bot_data = df.iloc[:150000]
human_data = df.iloc[150000:]

# split BOT data into training data, training target/label, testing data, testing target/label
train_bot_data, test_bot_data, train_bot_target, test_bot_target = train_test_split(
    bot_data[["text", "text_length", "unique_words", "punctuation", "sia_neg", "sia_neu", "sia_pos", "avg_sent_len", "kincaid_score"]],
    bot_data["target"],
    test_size=0.2,
    random_state=42,
    stratify=bot_data["target"]
)

# split HUMAN data into training data, training target/label, testing data, testing target/label
train_human_data, test_human_data, train_human_targets, test_human_targets = train_test_split(
    human_data[["text", "text_length", "unique_words", "punctuation", "sia_neg", "sia_neu", "sia_pos", "avg_sent_len", "kincaid_score"]],
    human_data["target"],
    test_size=0.2,
    random_state=42,
    stratify=human_data["target"]
)

# combine the bot and human TRAINING data
training_data = pd.concat([train_bot_data, train_human_data], ignore_index=True)
training_targets = pd.concat([train_bot_target, train_human_targets], ignore_index=True)

# combine the bot and human TESTING data
testing_data = pd.concat([test_bot_data, test_human_data], ignore_index=True)
testing_targets = pd.concat([test_bot_target, test_human_targets], ignore_index=True)

# Convert text in dataset text into integers / floating point values, in order to be used in predictive models => feature extraction / vectorization
# Create a TF-IDF vectorizer || Term Frequency and Inverse Document Frequecy
vectorizer = TfidfVectorizer(max_features=10000)

# extract features from training and testing dataset text
training_text_features = vectorizer.fit_transform(training_data["text"])
testing_text_features = vectorizer.transform(testing_data["text"])

# convert the extracted features represented in a sparse matrix into a dataframe so we can combine the new extracted features with the original features in our dataset
training_text_df = pd.DataFrame.sparse.from_spmatrix(training_text_features, index=training_data.index)
testing_text_df = pd.DataFrame.sparse.from_spmatrix(testing_text_features, index=testing_data.index)

# combine extracted features with original data features
training_features = pd.concat([training_text_df, training_data[["text_length", "unique_words", "punctuation", "sia_neg", "sia_neu", "sia_pos", "avg_sent_len", "kincaid_score"]]], axis=1)
testing_features = pd.concat([testing_text_df, testing_data[["text_length", "unique_words", "punctuation", "sia_neg", "sia_neu", "sia_pos", "avg_sent_len", "kincaid_score"]]], axis=1)

# Train model
model = Sequential()
model.add(Dense(8, activation='relu', name="layer1")) # a layer of dense neural networks consisting on 128, every neuron is receiving input from all previous neurons
model.add(Dense(8, activation='relu', name="layer2"))  # a layer of dense neural networks consisting on 128, every neuron is receiving input from all previous neurons
model.add(Dense(1, activation="sigmoid", name="layer3")) # maps input to a probability. 1 or 0

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(training_features, training_targets, epochs=5, batch_size=32, validation_data=(testing_features, testing_targets))

model.evaluate(testing_features, testing_targets)

model.save("bot_human_text_detector_model.h5")