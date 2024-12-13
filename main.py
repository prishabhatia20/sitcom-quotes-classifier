
import pandas as pd
import pygame

from sitcom_game import GameModel, GameController, GameView
from helpers import split_game_data
from constants import ACCURACY_CRITERIA
import run_model
import helpers

######################### THE OFFICE #########################

office_monologue = pd.read_csv("datasets/talking_head.csv")
office_response = pd.read_csv("datasets/parent_reply.csv.zip", compression='zip')

office_monologue.drop(['quote_id'], axis=1, inplace=True)
office_response.drop(['parent_id', 'parent'], axis=1, inplace=True)
office_response.rename(columns={'reply': 'quote'}, inplace=True)
office_data = pd.concat([office_monologue, office_response]).reset_index(drop=True)


office_data_filtered = run_model.filter_data(office_data, ACCURACY_CRITERIA)

office_data_game, office_data_training = split_game_data(office_data_filtered)


office_model, office_vectorizer = run_model.run_model(office_data_training)


######################### FRIENDS #########################

# Loading Friends dataset

friends_data = pd.read_csv("datasets/friends_quotes.csv.zip", compression='zip')
friends_data.drop(['episode_number', 'episode_title', 'quote_order', 'season'], axis=1, inplace=True)
friends_data.rename(columns={'author': 'character'}, inplace=True)
friends_data['character'] = friends_data['character'].str.title().str.strip()
friends_characters = ["Rachel", "Phoebe", "Monica", "Joey", "Chandler", "Ross"]
friends_data = friends_data[friends_data['character'].isin(friends_characters)]

print(friends_data['character'].unique())


friends_data_filtered = run_model.filter_data(friends_data, ACCURACY_CRITERIA)
friends_data_game, friends_data_training = split_game_data(friends_data_filtered)

friends_model, friends_vectorizer = run_model.run_model(friends_data_training)

######################### BROOKLYN 99 #########################

# Loading Brooklyn 99 data

brooklyn_data = pd.read_csv("datasets/Brooklyn99_Season1-4_Dataset.csv")
brooklyn_data.rename(columns={'name': 'character', 'line': 'quote'}, inplace=True)
brooklyn_data['character'] = brooklyn_data['character'].str.title().str.strip()

# Identify rows where multiple characters are mentioned
multi_character_rows = brooklyn_data[brooklyn_data['character'].str.contains(" AND ")]

# Split rows with multiple characters
split_rows = multi_character_rows['character'].str.split(" AND ", expand=True)


# Create a new DataFrame with split rows
split_data = pd.DataFrame({
    'character': split_rows.stack(),
    'quote': multi_character_rows['quote'].repeat(split_rows.shape[1]).values
})

# Remove the old rows with "AND" and append the new rows
brooklyn_data = pd.concat([
    brooklyn_data[~brooklyn_data['character'].str.contains(" And ")],
    split_data
], ignore_index=True)

typos = {"Charles": ["Boyle", "Kid Charles", "Charles On The Pole"],
         "Holt": ["Captain Holt", "Young Holt"],
         "Amy": ["Santiago", "Any"],
         "Jake": ["Peralta", "Jakes", "Jaek", "Young Jake", "Kake", "Jakw",
                  "Peralta Breaks The Glass Of The Interrogation Room Jake",
                  "Jake Laying On The Floor",
                  "Jake Leaves",
                  "Jake Sighs",
                  "Jake Chasing The Birds With A Bag",
                  "Jake Snaps His Fingers", "Jake Going Down The Pole",
                  "Jake Walks Into The Bullpen", "Jake Tries Them On",
                  "Jake Reads The Shirt", "Jake With A Guitar",
                  "Jake Walks In The Briefing Room Handing Terry The Guitar"],
         "Rosa": ["Diaz", "Rosa Walks In With A Vic Wearing A Nun Costume",
                  "Rosa On The Stand"],
         "Terry": ["Terey", "Sarge", "Teery"],
         "Hitchcock": ["Hitchock"],
         "Gina": ["Gina Moves The Gun To Scratch Her Nose", "Gina Flossing Her Teeth Says"], 
         "Scully": ["Scully Panicked"]}

brooklyn_data['character'] = brooklyn_data['character'].apply(lambda x: helpers.clean_character_names(x, typos))
brooklyn_characters = ["Jake", "Rosa", "Gina", "Amy", "Holt", "Charles", "Scully", "Hitchcock", "Terry"]

brooklyn_data = brooklyn_data[brooklyn_data['character'].isin(brooklyn_characters)]

brooklyn_data_filtered = run_model.filter_data(brooklyn_data, ACCURACY_CRITERIA)

brooklyn_data_game, brooklyn_data_training = split_game_data(brooklyn_data_filtered)

brooklyn_model, brooklyn_vectorizer = run_model.run_model(brooklyn_data_training)

while True:
    pygame.init()

    model = GameModel()
    view = GameView(model)
    controller = GameController(model)

    view.draw_main_screen()
    waiting_for_click = True
    show = ""
    while waiting_for_click:
        # Handle events like quitting the game
        show = controller.handle_main_screen_click()
        if show in ["The Office", "Friends", "Brooklyn 99"]:
            waiting_for_click = False  # Exit the loop after the click
    # show = controller.handle_main_screen_click()
    data = None
    classifier = None
    vectorizer = None
    if show == "The Office":
        data = office_data_game
        classifier = office_model
        vectorizer = office_vectorizer
    elif show == "Friends":
        data = friends_data_game
        classifier = friends_model
        vectorizer = friends_vectorizer
    elif show == "Brooklyn 99":
        data = brooklyn_data_game
        classifier = brooklyn_model
        vectorizer = brooklyn_vectorizer
    else:
        print("Please enter a valid show")
    print(data)
    
    # model.get_dataset(data)
    # model.get_classifier(classifier, vectorizer)
    # model.pick_quotes()
    if data is not None and isinstance(data, pd.DataFrame):
        model.get_dataset(data)
        model.get_classifier(classifier, vectorizer)
        model.pick_quotes()




    while model.active:
        model.get_quote()
        model.get_model_results()
        view.draw_question_screen()
        view.draw_characters()
        waiting_for_click = True
        while waiting_for_click:
            # Handle events like quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    model.active = False
                    waiting_for_click = False  # Exit the loop if the user quits

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicks, handle the click and stop waiting
                    controller.handle_answer_click()
                    waiting_for_click = False  # Exit the loop after the click
        model.check_answer()
        view.draw_result_screen()
        model.update_active()
    
    view.draw_final_screen()
    pygame.time.wait(5000)
