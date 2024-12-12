import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from helpers import split_game_data



# Loading The Office dataset
office_monologue = pd.read_csv("datasets/talking_head.csv")
office_response = pd.read_csv("datasets/parent_reply.csv.zip", compression='zip')

office_monologue.drop(['quote_id'], axis=1, inplace=True)
office_response.drop(['parent_id', 'parent'], axis=1, inplace=True)
office_response.rename(columns={'reply': 'quote'}, inplace=True)
office_data = pd.concat([office_monologue, office_response]).reset_index(drop=True)

office_data_game, office_data_training = split_game_data(office_data)

def filter_data(data, accuracy_criteria):

    X = data['quote']
    y = data['character']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # office_X_train, office_X_test, office_y_train, office_y_test = train_test_split(office_X, office_y, test_size=0.2, random_state=42)

    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.fit_transform(X_test)

    # office_X_train_vectorized = vectorizer.fit_transform(office_X_train)
    # office_X_test_vectorized = vectorizer.transform(office_X_test)

    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)
    y_pred = model.predict_proba(X_test_vectorized)
    for (probs, quote) in zip(y_pred, X_test):
        if max(probs) < accuracy_criteria:
            pass
        # Add the quote to a list to be removed


    # office_model = MultinomialNB()
    # office_model.fit(office_X_train_vectorized, office_y_train)
    # office_y_pred = office_model.predict_proba(office_X_test_vectorized)
    # for (probs, quote) in zip(office_y_pred, office_X_test):
    #     print(probs, quote)
    print("Accuracy:", accuracy_score(office_y_test, office_y_pred))
    print("Classification Report:\n", classification_report(office_y_test, office_y_pred))

office_test_quotes = office_data_game['quote']
office_test_vectorized = vectorizer.transform(office_test_quotes)
predictions = office_model.predict(office_test_vectorized)

for quote, character in zip(office_test_quotes, predictions):
    print(f"Quote: '{quote}' -> Character: {character}")