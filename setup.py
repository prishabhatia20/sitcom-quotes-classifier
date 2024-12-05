import pandas as pd
import tensorflow as tf
import helpers
from model import Model

from sklearn.metrics import  accuracy_score, confusion_matrix

import seaborn as sns
from matplotlib import pyplot as plt

# Switch cases for when game is played
show = "The Office"
data = None
match show:
    case "The Office":
        # Load The Office quotes

        office_monologue = pd.read_csv("datasets/talking_head.csv")
        office_response = pd.read_csv("datasets/parent_reply.csv.zip", compression='zip')

        office_monologue.drop(['quote_id'], axis=1, inplace=True)
        office_response.drop(['parent_id', 'parent'], axis=1, inplace=True)
        office_response.rename(columns={'reply': 'quote'}, inplace=True)

        # office_data = pd.concat([office_monologue, office_response]).reset_index(drop=True)
        data = pd.concat([office_monologue, office_response]).reset_index(drop=True)
        char_to_int = {
        "Michael": 0,
        "Dwight": 1,
        "Jim": 2,
        "Pam": 3
        }
        int_to_char = ["Michael", "Dwight", "Jim", "Pam"]
        data['character'] = data['character'].replace(char_to_int).astype('int8')

    case "Friends":

        # Loading and cleaning Friends data
        data = pd.read_csv("datasets/friends_quotes.csv.zip", compression='zip')
        data.drop(['episode_number', 'episode_title', 'quote_order', 'season'], axis=1, inplace=True)
        data.rename(columns={'author': 'character'}, inplace=True)

        char_to_int = {
            "Rachel": 0,
            "Phoebe": 1,
            "Monica": 2,
            "Joey": 3,
            "Chandler": 4,
            "Ross": 5
        }

        int_to_char = ["Rachel", "Phoebe", "Monica", "Joey", "Chandler", "Ross"]
        data = data[data['character'].isin(int_to_char)]
        data['character'] = data['character'].replace(char_to_int).astype('int8')

    case "Brooklyn 99":
        # Load Brooklyn 99 quotes

        data = pd.read_csv("datasets/Brooklyn99_Season1-4_Dataset.csv")
        data.rename(columns={'name': 'character', 'line': 'quote'}, inplace=True)
        # print(brooklyn_data)
        # print(data['character'].unique())

    case _:
        print("Invalid input")

data_game, data_training = helpers.split_game_data(data)

data_X = data_training['quote'].values
data_y = data_training['character'].values

X_train, X_test, y_train, y_test = helpers.split_and_preprocess_data(data_training, data_X, data_y)
X_train, X_test, tokenizer = helpers.tokenize_and_sequence(X_train, X_test)

model = Model()
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)
model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    batch_size=512,
    epochs=20
)


y_pred = model.predict(X_test, batch_size=512, verbose=1)
y_pred = y_pred.argmax(axis=1)

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
cm_recall = confusion_matrix(y_test, y_pred, normalize='true')
cm_precision = confusion_matrix(y_test, y_pred, normalize='pred')

print(f"Accuracy: {accuracy:%}")

plt.figure(figsize=(6, 6))
sns.heatmap(cm, annot=True, fmt="d", cbar=False)
plt.show()
