import pandas as pd
import tensorflow as tf
import helpers
from model import Model

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

    case "Friends":

        # Loading and cleaning Friends data
        data = pd.read_csv("datasets/friends_quotes.csv.zip", compression='zip')
        data.drop(['episode_number', 'episode_title', 'quote_order', 'season'], axis=1, inplace=True)
        data.rename(columns={'author': 'character'}, inplace=True)
        # print(friends_data)

    case "Brooklyn 99":
        # Load Brooklyn 99 quotes

        data = pd.read_csv("datasets/Brooklyn99_Season1-4_Dataset.csv")
        data.rename(columns={'name': 'character', 'line': 'quote'}, inplace=True)
        # print(brooklyn_data)

    case _:
        print("Invalid input")

data_game, data_training = helpers.split_game_data(data)

print(data_game)
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

