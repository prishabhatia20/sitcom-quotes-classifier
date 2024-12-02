import tensorflow as tf
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers
# import keras
from constants import NUM_WORDS, MAX_LEN, NUM_CLASSES

class Model(tf.keras.Model):
    def __init__(self, vocab_dim=NUM_WORDS, max_len=MAX_LEN, num_classes=NUM_CLASSES):
        super(Model, self).__init__()
        self.embedding = layers.Embedding(vocab_dim, 32, input_length=max_len)
        self.lstm1 = layers.Bidirectional(layers.LSTM(32, return_sequences=True))
        self.lstm2 = layers.Bidirectional(layers.LSTM(16))
        self.dense = layers.Dense(64, activation='relu')
        self.dropout = layers.Dropout(0.5)
        self.classifier = layers.Dense(num_classes, activation='softmax')

    def call(self, inputs, training=False):
        x = self.embedding(inputs)
        x = self.lstm1(x)
        x = self.lstm2(x)
        x = self.dense(x)
        if training:
            x = self.dropout(x, training=training)
        return self.classifier(x)
