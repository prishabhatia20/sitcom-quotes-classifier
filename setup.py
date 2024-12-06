import pandas as pd
import tensorflow as tf
import helpers
from model import Model

from sklearn.metrics import  accuracy_score, confusion_matrix

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

char_to_int = {
        "Michael": 0,
        "Dwight": 1,
        "Jim": 2,
        "Pam": 3
        }
int_to_char = ["Michael", "Dwight", "Jim", "Pam"]
office_data['character'] = office_data['character'].replace(char_to_int).astype('int8')


# Loading Friends dataset

friends_data = pd.read_csv("datasets/friends_quotes.csv.zip", compression='zip')
friends_data.drop(['episode_number', 'episode_title', 'quote_order', 'season'], axis=1, inplace=True)
friends_data.rename(columns={'author': 'character'}, inplace=True)

char_to_int = {
    "Rachel": 0,
    "Phoebe": 1,
    "Monica": 2,
    "Joey": 3,
    "Chandler": 4,
    "Ross": 5
}

int_to_char = ["Rachel", "Phoebe", "Monica", "Joey", "Chandler", "Ross"]
friends_data = friends_data[friends_data['character'].isin(int_to_char)]
friends_data['character'] = friends_data['character'].replace(char_to_int).astype('int8')

# Loading Brooklyn 99 data

brooklyn_data = pd.read_csv("datasets/Brooklyn99_Season1-4_Dataset.csv")
brooklyn_data.rename(columns={'name': 'character', 'line': 'quote'}, inplace=True)

show = "The Office"
data = None

match show:
    case "The Office":
        data = office_data

    case "Friends":
        data = friends_data
    
    case "Brooklyn 99":
        data = brooklyn_data
    
    case _:
        print("Invalid input")


# Split and train The Office 
office_data_game, office_data_training = helpers.split_game_data(office_data)

office_data_X = office_data_training['quote'].values
office_data_y = office_data_training['character'].values

office_X_train, office_X_test, office_y_train, office_y_test = helpers.split_and_preprocess_data(office_data_training, office_data_X, office_data_y)
office_X_train, office_X_test, office_tokenizer = helpers.tokenize_and_sequence(office_X_train, office_X_test)

# Split and train Friends data
friends_data_game, friends_data_training = helpers.split_game_data(friends_data)

friends_data_X = friends_data_training['quote'].values
friends_data_y = friends_data_training['character'].values

friends_X_train, friends_X_test, friends_y_train, friends_y_test = helpers.split_and_preprocess_data(friends_data_training, friends_data_X, friends_data_y)
friends_X_train, friends_X_test, friends_tokenizer = helpers.tokenize_and_sequence(friends_X_train, friends_X_test)

# Split and train Brooklyn 99 data

brooklyn_data_game, brooklyn_data_training = helpers.split_game_data(brooklyn_data)

brooklyn_data_X = brooklyn_data_training['quote'].values
brooklyn_data_y = brooklyn_data_training['character'].values

brooklyn_X_train, brooklyn_X_test, brooklyn_y_train, brooklyn_y_test = helpers.split_and_preprocess_data(brooklyn_data_training, brooklyn_data_X, brooklyn_data_y)
brooklyn_X_train, brooklyn_X_test, tokenizer = helpers.tokenize_and_sequence(brooklyn_X_train, brooklyn_X_test)


# Run Office model

office_model = Model()
office_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)
office_model.fit(
    office_X_train, office_y_train,
    validation_data=(office_X_test, office_y_test),
    batch_size=512,
    epochs=20
)


office_y_pred = office_model.predict(office_X_test, batch_size=512, verbose=1)
office_y_pred = office_y_pred.argmax(axis=1)

office_accuracy = accuracy_score(office_y_test, office_y_pred)
office_cm = confusion_matrix(office_y_test, office_y_pred)
office_cm_recall = confusion_matrix(office_y_test, office_y_pred, normalize='true')
office_cm_precision = confusion_matrix(office_y_test, office_y_pred, normalize='pred')

print(f"Office Accuracy: {office_accuracy:%}")

plt.figure(figsize=(6, 6))
sns.heatmap(office_cm, annot=True, fmt="d", cbar=False)
plt.show()


# Run Friends model

friends_model = Model()
friends_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)
friends_model.fit(
    friends_X_train, friends_y_train,
    validation_data=(friends_X_test, friends_y_test),
    batch_size=512,
    epochs=20
)


friends_y_pred = friends_model.predict(friends_X_test, batch_size=512, verbose=1)
friends_y_pred = friends_y_pred.argmax(axis=1)

friends_accuracy = accuracy_score(friends_y_test, friends_y_pred)
friends_cm = confusion_matrix(friends_y_test, friends_y_pred)
friends_cm_recall = confusion_matrix(friends_y_test, friends_y_pred, normalize='true')
friends_cm_precision = confusion_matrix(friends_y_test, friends_y_pred, normalize='pred')

print(f"Friends Accuracy: {friends_accuracy:%}")

plt.figure(figsize=(6, 6))
sns.heatmap(friends_cm, annot=True, fmt="d", cbar=False)
plt.show()

# Run Brooklyn 99 model

brooklyn_model = Model()
brooklyn_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)
brooklyn_model.fit(
    brooklyn_X_train, brooklyn_y_train,
    validation_data=(brooklyn_X_test, brooklyn_y_test),
    batch_size=512,
    epochs=20
)


brooklyn_y_pred = brooklyn_model.predict(brooklyn_X_test, batch_size=512, verbose=1)
brooklyn_y_pred = brooklyn_y_pred.argmax(axis=1)

brooklyn_accuracy = accuracy_score(brooklyn_y_test, brooklyn_y_pred)
brooklyn_cm = confusion_matrix(brooklyn_y_test, brooklyn_y_pred)
brooklyn_cm_recall = confusion_matrix(brooklyn_y_test, brooklyn_y_pred, normalize='true')
brooklyn_cm_precision = confusion_matrix(brooklyn_y_test, brooklyn_y_pred, normalize='pred')

print(f"Brooklyn 99 Accuracy: {brooklyn_accuracy:%}")

plt.figure(figsize=(6, 6))
sns.heatmap(brooklyn_cm, annot=True, fmt="d", cbar=False)
plt.show()

