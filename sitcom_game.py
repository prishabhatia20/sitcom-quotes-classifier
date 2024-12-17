import pygame
import re
import numpy as np
import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
import os
import random
from constants import FRAME_WIDTH, FRAME_HEIGHT

DEFAULT_IMAGE_SIZE = (500, 250)
DEFAULT_HEAD_SIZE = (430, 400)

screen = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
clock = pygame.time.Clock()

class GameModel:
    """
    A class containing the game's model, following the MVC format
    """
    total_questions = 7

    def __init__(self):
        self.score = 0
        self.questions_shown = 0
        self.active = True
        self.data = None
        self.show = None
        self.current_quote = ""
        self.current_answer = ""
        self.characters = []
        self.quote_indices = []
        self.model_answer = ""
        self.correct_answer = None
        self.model_correct_answer = None
        self.model_score = 0
        self.classifier = None
        self.vectorizer = None
        self.predictions = []
        self.user_answer = ""
        self.characters_dict = {}
    
    def get_dataset(self, data):
        """
        Once the user selects the show, load the quotes dataset and update the
        characters list

        Args:   
            data: a Pandas dataframe with quotes and their corresponding
            characters
        """
        if data is None or not isinstance(data, pd.DataFrame):
            raise ValueError("Invalid dataset provided. Please pass a valid Pandas DataFrame.")
    
        self.data = data
        # self.characters = self.data['character'].unique() 
        # self.characters.lower()
        self.characters = [character.lower() for character in self.data['character'].unique()]
    
    def get_classifier(self, classifier, vectorizer):
        self.classifier = classifier
        self.vectorizer = vectorizer
    
    def pick_quotes(self):
        """
        From the given dataset, pick 7 quotes to test the user on
        """
        rows, _ = self.data.shape
        for _ in range(self.total_questions):
            self.quote_indices.append(random.randint(0, rows))
        
    def get_quote(self):
        """
        Access a specified row of data and set the current quote and answer to the
        values in that row
        """
                
        row = self.data.iloc[self.quote_indices[self.questions_shown]]
        character = row['character']
        quote = row['quote']

        first_sentence = re.split(r'[.!?]', quote)[0].strip()

        self.current_quote = first_sentence
        self.current_answer = character.lower()
        self.questions_shown += 1
    
    def get_model_results(self):
        """
        Pass a quote into the mdoel and get its prediction
        """
        quote = [self.current_quote]
        quote_vectorized = self.vectorizer.transform(quote)
        prediction = self.classifier.predict(quote_vectorized)
        
        # if isinstance(prediction, np.ndarray):  
        #     prediction = [p.lower() for p in prediction]
        # elif isinstance(prediction, str): 
        #     prediction = prediction.lower()
        # self.model_answer = prediction

        if isinstance(prediction, np.ndarray):  
            if len(prediction) > 0: 
                self.model_answer = prediction[0].lower()
            else:
                self.model_answer = "" 
        elif isinstance(prediction, str): 
            self.model_answer = prediction.lower()
        else:
            raise ValueError(f"Unexpected prediction type: {type(prediction)}")


    def update_score(self):
        """
        Update the user's score
        """
        self.score += 1
    
    def update_active(self):
        """
        Update whether the game is active or not (whether there are questions left)
        """
        if self.questions_shown == self.total_questions:
            self.active = False

    def update_model_score(self):
        self.model_score += 1

    def check_answer(self, x, y):
        """
        Handles user input to determine whether the selected character is correct.
        
        Args:
            x (int): X-coordinate of the mouse click.
            y (int): Y-coordinate of the mouse click.
        """

        # Check if the user clicked within the bounds of the correct character
        for character, pos in self.characters_dict.items():
            if (pos[0] <= x <= pos[0] + DEFAULT_HEAD_SIZE[0] and
                pos[1] <= y <= pos[1] + DEFAULT_HEAD_SIZE[1]
            ):
                self.user_answer = character
                break

        if self.user_answer == self.current_answer:
            self.correct_answer = True
            self.update_score()
        else:
            self.correct_answer = False




        if self.model_answer == self.current_answer:
            self.update_model_score()
            self.model_correct_answer = True
        else:
            self.model_correct_answer = False

        print(f"------------User Answer: {self.user_answer}, Model Answer: {self.model_answer}, Correct Answer: {self.correct_answer}---------------")
    
    def determine_winner(self):
        """
        Compare scores and determine whether the model or the user wins
        """
        if self.model_score > self.score:
            return "model"
        elif self.model_score < self.score:
            return "user"
        else:
            return "tie"

    

class GameView:
    """
    A class containing the game view, following the MVC format
    """
    def __init__(self, model):
        """
        Initialize the model and load all necessary images
        """
        self.model = model
        self.frame_width = FRAME_WIDTH
        self.frame_height = FRAME_HEIGHT

        self.world = pygame.display.set_mode([self.frame_width, self.frame_height])

        # Load start background image

        self.start_background = pygame.image.load(
            os.path.join("images", "main_background.png")
        ).convert()
        self.start_background = pygame.transform.scale(self.start_background, (self.frame_width, self.frame_height))

        # Load the main background image
        self.empty_background = pygame.image.load(
            os.path.join("images", "empty_background.png")
        ).convert()
        self.empty_background = pygame.transform.scale(self.empty_background, (self.frame_width, self.frame_height))

        # Load win image
        self.win_image = pygame.image.load(
            os.path.join("images", "win.png")
        ).convert()
        self.win_image = pygame.transform.scale(self.win_image, (self.frame_width, self.frame_height))

        # Load lose image
        self.lose_image = pygame.image.load(
            os.path.join("images", "lose.png")
        ).convert()
        self.lose_image = pygame.transform.scale(self.lose_image, (self.frame_width, self.frame_height))

        # Load tie image
        self.tie_image = pygame.image.load(
            os.path.join("images", "tie.png")
        ).convert()
        self.tie_image = pygame.transform.scale(self.tie_image, (self.frame_width, self.frame_height))



        # Load show logos
        self.office_logo = self.load_and_transform_image("the_office_logo.png")
        self.friends_logo = self.load_and_transform_image("friends_logo.png")
        self.brooklyn_logo = self.load_and_transform_image("brooklyn_logo.png")

        self.font = pygame.font.Font(None, 50)

        self.images = {}
    
    def load_and_transform_image(self, filename):
        """
        Load an image, convert it, and apply transparency settings

        Args:
            filename: a String containing the name of the image to load
        """

        image = pygame.image.load(os.path.join("images", filename)).convert()
        image.set_colorkey((255, 255, 255))

        return pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

    def load_character_images(self, folder):
        """
        Given a folder and character list, load and process character head images

        Args:
            folder: a String representing the folder the images are stored in
        
            characters: a list of the characters to load
        
        Returns:
            images: a dict where the character name maps to their loaded in image
        """

        for character in self.model.characters:
            character_lower = character.lower()
            file_path = os.path.join("images", folder, character_lower + ".png")
            
            if not os.path.exists(file_path):
                print(f"Image file not found for {character}: {file_path}")
                continue

            try:
                image = pygame.image.load(file_path).convert()
                image.set_colorkey((255, 255, 255))
                image = pygame.transform.scale(image, DEFAULT_HEAD_SIZE)
                # Store using `character_lower` as key
                self.images[character_lower] = image
            except Exception as e:
                print(f"Error loading image for {character}: {e}")
        
    def draw_main_screen(self):
        """
        Draw the main screen with the show selection logos
        """ 

        self.world.blit(self.start_background, (0, 0))

        # Draw logos for show selection
        self.world.blit(self.office_logo, (100, 300))
        self.world.blit(self.friends_logo, (500, 700))
        self.world.blit(self.brooklyn_logo, (900, 275))

        pygame.display.flip()

    def draw_question_screen(self):
        """
        Draw the screen for displaying a question and input.
        """
        self.world.blit(self.empty_background, (0, 0))

        # Quote
        self.render_text(f"Quote: {self.model.current_quote}", (50, 150))

        self.render_text(f"Score: {self.model.score}", (50, 50))
        self.render_text(f"Question: {self.model.questions_shown}/7", (FRAME_WIDTH - 300, 50))

        pygame.display.flip()
    
    def draw_characters(self):
        """
        Randomly pick three other characters and draw the random characters + the
        answer character on the screen
        """

        # Create a copy of the characters list
        temp_characters_list = list(self.model.characters)

        # Remove the correct character from the list & randomly select 3 others
        temp_characters_list.remove(self.model.current_answer)
        other_characters = random.sample(temp_characters_list, 3)
        # Append the current answer to the list & shuffle
        other_characters.append(self.model.current_answer)

        other_characters = [character.lower() for character in other_characters]
        random.shuffle(other_characters)

        # Assign positions to the characters
        self.model.characters_dict = {
            other_characters[0]: (200, 200),
            other_characters[1]: (900, 200),
            other_characters[2]: (900, 600),
            other_characters[3]: (200, 600),
        }

        for character in other_characters:
            character_lower = character.lower()
            image = self.images.get(character_lower)

            if image is None:
                print(f"Image for {character} not found in self.images.")
                continue

            self.world.blit(image, self.model.characters_dict[character])


        pygame.display.flip()

    
    def draw_result_screen(self):
        """
        Draw the screen showing whether the answer was correct or not
        """
        self.world.blit(self.empty_background, (0, 0))


        self.render_text(f"Quote: {self.model.current_quote}", (50, 150))

        self.render_text(f"Your Score: {self.model.score}/7", (FRAME_WIDTH - 300, 250))
        self.render_text(f"Model's Score: {self.model.model_score}/7", (50, 250))
        self.render_text(f"Question: {self.model.questions_shown}/7", (FRAME_WIDTH - 300, 50))

    

        self.world.blit(self.images.get(self.model.user_answer), (1000, 500))
        self.world.blit(self.images.get(self.model.model_answer), (200, 500))
        if self.model.correct_answer:
            self.render_text("Correct!", (FRAME_WIDTH - 400, 700), color=(193, 225, 193))
        else:
            self.render_text("Incorrect", (FRAME_WIDTH - 400, 700), color=(250, 160, 160))
        

        if self.model.model_correct_answer:
            self.render_text("Correct!", (400, 700), color=(193, 255, 193))
        else:
            self.render_text("Incorrect", (400, 700), color=(250, 160, 160))
        
        if not (self.model.model_correct_answer or self.model.correct_answer):
            self.render_text(f"Correct Answer: {self.model.current_answer.title()}", (500, 900))

        pygame.display.flip()
            

    def render_text(self, text, position, color=(255, 255, 255)):
        """
        Render any text on the screen

        Args:
            text: a String that is the text to be rendered
            position: a tuple representing where the text should be rendered
            color: a tuple determining the text's color (defaults to white)
        """
        rendered_text = self.font.render(text, True, color)
        self.world.blit(rendered_text, position)

    def draw_final_screen(self):
        """
        Draw the final screen showing whether the user won, the model won, or there was
        a tie
        """
        result = self.model.determine_winner()
        if result == "model":
            self.world.blit(self.lose_image, (0, 0))
        elif result == "tie":
            self.world.blit(self.tie_image, (0, 0))
        else:
            self.world.blit(self.win_image, (0, 0))
        
        self.render_text(f"Your Score: {self.model.score}/7", (1000, 100))
        self.render_text(f"Model Score: {self.model.model_score}/7", (200, 100))
        pygame.display.flip()


            



class GameController:
    """
    A class containing the game controller, following the MVC format
    """
    def __init__(self, model):
        """
        Initialize the model
        """
        self.model = model

    def handle_main_screen_click(self):
        """
        Handle the event when the user selects which show they want to play
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.active = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Office logo bounds
                if 100 <= x <= 100 + DEFAULT_IMAGE_SIZE[0] and 300 <= y <= 300 + DEFAULT_IMAGE_SIZE[1]:
                    return "the-office"                
                # Friends logo bounds
                elif 500 <= x <= 500 + DEFAULT_IMAGE_SIZE[0] and 700 <= y <= 700 + DEFAULT_IMAGE_SIZE[1]:
                    return "friends"                
                # Brooklyn 99 logo bounds
                elif 900 <= x <= 900 + DEFAULT_IMAGE_SIZE[0] and 275 <= y <= 275 + DEFAULT_IMAGE_SIZE[1]:
                    return "brooklyn-99"


    def handle_answer_click(self):
        """
        Handle the event where the user selects their answer
        """
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.model.active = False
                    waiting_for_click = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.model.check_answer(x, y)
                    waiting_for_click = False

