import tensorflow as tf
from tensorflow.keras import layers
from helpers import preprocess_text, get_class_weights, split_and_preprocess_data, save_tokenizer, load_tokenizer
from constants import NUM_WORDS, MAX_LEN, NUM_CLASSES

class Model(tf.keras.Model):
    def __init__(self, vocab_dim=NUM_WORDS, max_len=MAX_LEN, num_classes=NUM_CLASSES):
        super(Model, self).__init__()
        self.embedding = layers.Embedding(vocab_dim, 128, input_length=max_len)
        self.lstm1 = layers.Bidirectional(layers.LSTM(64, return_sequences=True))
        self.lstm2 = layers.Bidirectional(layers.LSTM(32))
        self.dense = layers.Dense(128, activation='relu')
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


def train_model(data, model_save_path, tokenizer_save_path, train_ratio=0.8, batch_size=64, epochs=20):
    train_sequences, train_labels, test_sequences, test_labels, tokenizer = split_and_preprocess_data(data, train_ratio=train_ratio)
    save_tokenizer(tokenizer, tokenizer_save_path)
    class_weights = get_class_weights(train_labels)
    model = Model()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(
        train_sequences,
        train_labels,
        validation_data=(test_sequences, test_labels),
        class_weight=class_weights,
        batch_size=batch_size,
        epochs=epochs
    )
    model.save(model_save_path)
    return model


def predict_quotes(quotes, model_path, tokenizer_path):
    model = tf.keras.models.load_model(model_path)
    tokenizer = load_tokenizer(tokenizer_path)
    sequences, _ = preprocess_text(quotes, tokenizer=tokenizer, maxlen=MAX_LEN, train_mode=False)
    predictions = model.predict(sequences)
    return predictions.argmax(axis=1)
