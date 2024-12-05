import os
# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from constants import NUM_WORDS, MAX_LEN, NUM_CLASSES
import pickle

def tokenize_and_sequence(train_sentences, test_sentences, num_words=NUM_WORDS, maxlen=MAX_LEN):
    tokenizer = Tokenizer(num_words=num_words, oov_token='<OOV>')
    tokenizer.fit_on_texts(train_sentences)

    train_sequences = tokenizer.texts_to_sequences(train_sentences)
    train_sequences = pad_sequences(
        train_sequences, padding='post', maxlen=maxlen, truncating='post'
    )

    test_sequences = tokenizer.texts_to_sequences(test_sentences)
    test_sequences = pad_sequences(
        test_sequences, padding='post', maxlen=maxlen, truncating='post'
    )

    return train_sequences, test_sequences, tokenizer

def save_tokenizer(tokenizer, filepath):
    with open(filepath, 'wb') as file:
        pickle.dump(tokenizer, file)

def load_tokenizer(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)

def preprocess_text(sentences, tokenizer=None, maxlen=MAX_LEN, num_words=NUM_WORDS, train_mode=False):
    if tokenizer is None and train_mode:
        tokenizer = Tokenizer(num_words=num_words, oov_token='<OOV>')
        tokenizer.fit_on_texts(sentences)
    elif tokenizer is None:
        raise ValueError("Tokenizer must be provided when not in train mode.")
    
    sequences = tokenizer.texts_to_sequences(sentences)
    sequences = pad_sequences(sequences, padding='post', maxlen=maxlen, truncating='post')
    return sequences, tokenizer

def get_class_weights(labels, num_classes=NUM_CLASSES):
    class_counts = [sum(1 for label in labels if label == i) for i in range(num_classes)]
    total = sum(class_counts)
    class_weights = {i: total / (num_classes * class_counts[i]) for i in range(num_classes) if class_counts[i] > 0}
    return class_weights

def split_and_preprocess_data(data, tokenizer=None, train_ratio=0.8, num_words=NUM_WORDS, maxlen=MAX_LEN):
    from sklearn.model_selection import train_test_split
    
    train_data, test_data = train_test_split(data, train_size=train_ratio, stratify=data['character'])
    train_sequences, test_sequences, tokenizer = tokenize_and_sequence(
        train_data['quote'], test_data['quote'], num_words=num_words, maxlen=maxlen
    )
    return train_sequences, train_data['character'], test_sequences, test_data['character'], tokenizer
