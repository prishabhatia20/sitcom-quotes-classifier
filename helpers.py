import os
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Download stopwords
nltk.download('stopwords')

# Constants
from constants import NUM_WORDS, MAX_LEN, NUM_CLASSES


def preprocess_text(sentences, tokenizer=None, maxlen=MAX_LEN, num_words=NUM_WORDS, train_mode=False):
    """
    Preprocess the input sentences: remove non-alphanumeric characters,
    convert to lowercase, and remove stopwords.
    """
    stop_words = set(stopwords.words('english'))
    cleaned_sentences = [
        " ".join(word for word in re.sub(r'[^a-zA-Z\s]', '', sentence.lower()).split() if word not in stop_words)
        for sentence in sentences
    ]
    
    if tokenizer is None and train_mode:
        tokenizer = Tokenizer(num_words=num_words, oov_token='<OOV>')
        tokenizer.fit_on_texts(cleaned_sentences)
    elif tokenizer is None:
        raise ValueError("Tokenizer must be provided when not in train mode.")
    
    sequences = tokenizer.texts_to_sequences(cleaned_sentences)
    sequences = pad_sequences(sequences, padding='post', maxlen=maxlen, truncating='post')
    return sequences, tokenizer


def tokenize_and_sequence(train_sentences, test_sentences, num_words=NUM_WORDS, maxlen=MAX_LEN):
    """
    Tokenize and convert sentences to sequences for both training and testing datasets.
    """
    tokenizer = Tokenizer(num_words=num_words, oov_token='<OOV>')
    tokenizer.fit_on_texts(train_sentences)

    train_sequences = tokenizer.texts_to_sequences(train_sentences)
    train_sequences = pad_sequences(train_sequences, padding='post', maxlen=maxlen, truncating='post')

    test_sequences = tokenizer.texts_to_sequences(test_sentences)
    test_sequences = pad_sequences(test_sequences, padding='post', maxlen=maxlen, truncating='post')

    return train_sequences, test_sequences, tokenizer


def save_tokenizer(tokenizer, filepath):
    """
    Save the tokenizer object to a file using pickle.
    """
    with open(filepath, 'wb') as file:
        pickle.dump(tokenizer, file)


def load_tokenizer(filepath):
    """
    Load a tokenizer object from a file using pickle.
    """
    with open(filepath, 'rb') as file:
        return pickle.load(file)


def get_class_weights(labels, num_classes=NUM_CLASSES):
    """
    Compute class weights for imbalanced datasets.
    """
    class_counts = [sum(1 for label in labels if label == i) for i in range(num_classes)]
    total = sum(class_counts)
    class_weights = {i: total / (num_classes * class_counts[i]) for i in range(num_classes) if class_counts[i] > 0}
    return class_weights


def split_and_preprocess_data(data, data_X, data_y, train_ratio=0.8):
    """
    Split the dataset into training and testing sets, preprocess the text data, and return the splits.
    """
    X_train, X_test, y_train, y_test = train_test_split(data_X, data_y, train_size=train_ratio, stratify=data['character'])
    return X_train, X_test, y_train, y_test


def split_game_data(data, game_size=30):
    """
    Split the dataset into unseen quotes to be used in the game and data to be used
    to train and test the model.
    """
    game_data, training_data = train_test_split(data, train_size=game_size)
    return game_data, training_data


def clean_character_names(row, typos_dict):
    """
    Correct typos in character names using a dictionary of common typos.
    """
    for correct_name, typo_list in typos_dict.items():
        if row in typo_list:
            return correct_name
    return row


def balance_data(data_X, data_y):
    """
    Balance the dataset using oversampling for underrepresented classes.
    """
    from imblearn.over_sampling import SMOTE
    smote = SMOTE()
    data_X_resampled, data_y_resampled = smote.fit_resample(data_X, data_y)
    return data_X_resampled, data_y_resampled
