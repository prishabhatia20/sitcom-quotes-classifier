from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

def filter_data(data, accuracy_criteria):
    quotes_to_remove = []
    X = data['quote']
    y = data['character']

    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    data['quote'] = data['quote'].str.strip().str.lower()
    X_test = X_test.str.strip().str.lower()

    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    # X_test_vectorized = vectorizer.transform(X_test)


    print(set(X_test).difference(data['quote']))


    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)

    # Now that the model has been trained, put the entire dataset into the model and filter that out
    data_vectorized = vectorizer.transform(data['quote'])


    y_pred = model.predict_proba(data_vectorized)
    for (probs, quote) in zip(y_pred, data['quote']):
        if max(probs) < accuracy_criteria:
            quotes_to_remove.append(quote)
        # else:
        #     print(probs, quote)



    data_filtered = data[~data['quote'].isin(quotes_to_remove)]
    return data_filtered


def run_model(data):
    X = data['quote']
    y = data['character']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)
    y_pred = model.predict(X_test_vectorized)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    return model, vectorizer

