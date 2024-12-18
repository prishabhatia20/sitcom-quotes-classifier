from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

def filter_data(data, accuracy_criteria):
    """
    Filters a dataset based on model prediction confidence.

    Args:
        data: A pandas DataFrame with at least two columns: 'quote' (text data) and 'character' (labels).
        accuracy_criteria: The minimum probability required for a quote to be retained.

    Returns:
        data_filtered: A filtered version of the input DataFrame where quotes with prediction probabilities
                 below the accuracy_criteria are removed.
    """
    quotes_to_remove = []
    X = data['quote'] 
    y = data['character']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=42)

    # Preprocess quotes: strip whitespace and convert to lowercase
    data['quote'] = data['quote'].str.strip().str.lower()
    X_test = X_test.str.strip().str.lower()

    # Vectorize the training data using bag-of-words
    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)

    # Print any unseen test quotes not present in the preprocessed dataset
    print(set(X_test).difference(data['quote']))

    # Train a Multinomial Naive Bayes model
    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)

    # Transform the entire dataset using the vectorizer
    data_vectorized = vectorizer.transform(data['quote'])

    # Predict probabilities for each quote
    y_pred = model.predict_proba(data_vectorized)
    for (probs, quote) in zip(y_pred, data['quote']):
        # If the maximum predicted probability is below the threshold, mark the quote for removal
        if max(probs) < accuracy_criteria:
            quotes_to_remove.append(quote)

    # Remove quotes that don't meet the accuracy criteria
    data_filtered = data[~data['quote'].isin(quotes_to_remove)]
    return data_filtered


def run_model(data):
    """
    Trains a Multinomial Naive Bayes model on the dataset and evaluates its performance.

    Parameters:
        data: A pandas DataFrame with at least two columns: 'quote' (text data) and 'character' (labels).

    Returns:
        model: The trained Naive Bayes model.
        vectorizer: The vectorizer used to transform the text data.
    """
    X = data['quote']
    y = data['character']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Vectorize the training and testing data using bag-of-words
    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Train a Multinomial Naive Bayes model
    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test_vectorized)

    # Print evaluation metrics
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Compute and display the confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot(cmap=plt.cm.Blues, xticks_rotation='vertical')
    plt.title("Confusion Matrix")
    plt.show()

    return model, vectorizer
