import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from constants import NUM_WORDS, MAX_LEN, NUM_CLASSES

def tokenize_and_sequence(train_sentences,
                          test_sentences,
                          num_words=NUM_WORDS,
                          maxlen=MAX_LEN):
    tokenizer = Tokenizer(num_words=num_words, oov_token='<OOV>')
    tokenizer.fit_on_texts(train_sentences)

    train_sequences = tokenizer.texts_to_sequences(train_sentences)
    train_sequences = pad_sequences(
        train_sequences,
        padding='post', maxlen=maxlen, truncating='post'
    )

    test_sequences = tokenizer.texts_to_sequences(test_sentences)
    test_sequences = pad_sequences(
        test_sequences,
        padding='post', maxlen=maxlen, truncating='post'
    )

    return train_sequences, test_sequences, tokenizer