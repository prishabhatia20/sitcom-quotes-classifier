import os
import tensorflow as tf
from tensorflow.keras import layers
from helpers import preprocess_text, get_class_weights, balance_data
from constants import NUM_WORDS, MAX_LEN, NUM_CLASSES

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class Model(tf.keras.Model):
    def __init__(self, vocab_dim=NUM_WORDS, max_len=MAX_LEN, num_classes=NUM_CLASSES):
        super(Model, self).__init__()
        # Embedding and LSTM layers
        self.embedding = layers.Embedding(vocab_dim, 256, input_length=max_len)
        self.lstm1 = layers.Bidirectional(layers.LSTM(128, return_sequences=True))
        self.attention = layers.MultiHeadAttention(num_heads=4, key_dim=128)
        self.norm = layers.LayerNormalization()
        self.lstm2 = layers.Bidirectional(layers.LSTM(64))
        self.dense = layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))
        self.dropout = layers.Dropout(0.5)
        self.classifier = layers.Dense(num_classes, activation='softmax')

    @tf.function
    def call(self, inputs, training=False):
        x = self.embedding(inputs)
        x = self.lstm1(x)
        attn_out = self.attention(x, x)
        x = self.norm(x + attn_out)  # Residual connection with normalization
        x = self.lstm2(x)
        x = self.dense(x)
        if training:
            x = self.dropout(x, training=training)
        return self.classifier(x)

def train_model(data_X, data_y, model_save_path, tokenizer_save_path, batch_size=64, epochs=50):
    """
    Train the model with the given dataset.
    """
    # Balance dataset
    data_X, data_y = balance_data(data_X, data_y)

    # Tokenization and sequencing
    train_sequences, test_sequences, tokenizer = tokenize_and_sequence(data_X, data_X)

    # Calculate class weights
    class_weights = get_class_weights(data_y)

    # Initialize and compile model
    model = Model()
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(
        train_sequences,
        data_y,
        validation_split=0.2,
        batch_size=batch_size,
        epochs=epochs,
        class_weight=class_weights
    )

    # Save the tokenizer and model
    save_tokenizer(tokenizer, tokenizer_save_path)
    model.save(model_save_path, save_format='tf')
    return model
