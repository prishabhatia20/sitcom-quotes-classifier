import pandas as pd


# Loading and cleaning Friends data
friends_data = pd.read_csv("datasets/friends_quotes.csv.zip", compression='zip')
friends_data.drop(['episode_number', 'episode_title', 'quote_order', 'season'], axis=1, inplace=True)
friends_data.rename(columns={'author': 'character'}, inplace=True)
print(friends_data)

# Load The Office quotes

office_monologue = pd.read_csv("datasets/talking_head.csv")
office_response = pd.read_csv("datasets/parent_reply.csv.zip", compression='zip')

office_monologue.drop(['quote_id'], axis=1, inplace=True)
office_response.drop(['parent_id', 'parent'], axis=1, inplace=True)
office_response.rename(columns={'reply': 'quote'}, inplace=True)

office_data = pd.concat([office_monologue, office_response]).reset_index(drop=True)
print(office_data)
# Load Brooklyn 99 quotes

brooklyn_data = pd.read_csv("datasets/Brooklyn99_Season1-4_Dataset.csv")
brooklyn_data.rename(columns={'name': 'character', 'line': 'quote'}, inplace=True)
print(brooklyn_data)