# setup.py
import pandas as pd
import tensorflow as tf
import helpers
from model import Model

from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
from matplotlib import pyplot as plt

# Whether the model for The Office, Friends, and Brooklyn 99 has been trained 
model_trained = [False, False, False]

# Loading The Office dataset
office_monologue = pd.read_csv("datasets/talking_head.csv")
office_response = pd.read_csv("datasets/parent_reply.csv.zip", compression='zip')

office_monologue.drop(['quote_id'], axis=1, inplace=True)
office_response.drop(['parent_id', 'parent'], axis=1, inplace=True)
office_response.rename(columns={'reply': 'quote'}, inplace=True)
office_data = pd.concat([office_monologue, office_response]).reset_index(drop=True)

office_char_to_int = {
    "Michael": 0,
    "Dwight": 1,
    "Jim": 2,
    "Pam": 3
}
office_int_to_char = ["Michael", "Dwight", "Jim", "Pam"]
office_data['character'] = office_data['character'].replace(office_char_to_int).astype('int8')
office_data['quote'], _ = helpers.preprocess_text(office_data['quote'], train_mode=True)

# Splitting and preprocessing data
office_data_game, office_data_training = helpers.split_game_data(office_data)
office_data_X = office_data_training['quote'].values
office_data_y = office_data_training['character'].values
office_X_train, office_X_test, office_y_train, office_y_test = helpers.split_and_preprocess_data(office_data_training, office_data_X, office_data_y)

# Run Office model
office_model = Model()
office_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)
office_model.fit(
    office_X_train, office_y_train,
    validation_data=(office_X_test, office_y_test),
    batch_size=512,
    epochs=50
)
office_y_pred = office_model.predict(office_X_test, batch_size=512, verbose=1)
office_y_pred = office_y_pred.argmax(axis=1)
office_accuracy = accuracy_score(office_y_test, office_y_pred)
office_cm = confusion_matrix(office_y_test, office_y_pred)
print(f"Office Accuracy: {office_accuracy:%}")
plt.figure(figsize=(6, 6))
sns.heatmap(office_cm, annot=True, fmt="d", cbar=False)
plt.show()

# Similar blocks for Friends and Brooklyn 99 datasets can be added following this pattern.
