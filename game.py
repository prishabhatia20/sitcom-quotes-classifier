import pygame
import os
import random
from constants import FRAME_WIDTH, FRAME_HEIGHT

DEFAULT_IMAGE_SIZE = (500, 250)
DEFAULT_HEAD_SIZE = (400, 400)

pygame.init()
screen = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
clock = pygame.time.Clock()

class Model:
    total_questions = 7

    def __init__(self):
        self.score = 0
        self.num_questions = 0
        self.active = True
        self.selected_show = None
        self.current_quote = ""
        self.current_answer = ""

class View:
    def __init__(self):
        # Screen dimensions
        self.frame_width = FRAME_WIDTH
        self.frame_height = FRAME_HEIGHT

        # Create a display window using Pygame
        self.world = pygame.display.set_mode([self.frame_width, self.frame_height])

        # Load the main screen image
        self.background = pygame.image.load(
            os.path.join("images", "main_background.png")
        ).convert()
        self.background = pygame.transform.scale(self.background, (self.frame_width, self.frame_height))

        self.empty_background = pygame.image.load(
            os.path.join("images", "empty_background.png")
        ).convert()
        self.empty_background = pygame.transform.scale(self.empty_background, (self.frame_width, self.frame_height))

        # Load show logos
        self.office_logo = self.load_and_transform_image("the_office_logo.png")
        self.friends_logo = self.load_and_transform_image("friends_logo.png")
        self.brooklyn_logo = self.load_and_transform_image("brooklyn_logo.png")

        # Fonts
        self.font = pygame.font.Font(None, 50)

        self.office_characters = ["michael", "dwight", "jim", "pam"]
        self.friends_characters = ["rachel", "phoebe", "monica", "joey", "chandler", "ross"]

        ############ ADD GINA AND HITCHCOCK ##################
        self.brooklyn_characters = ["jake", "rosa", "amy", "holt", "charles", "scully", "terry"]

        self.office_images = self.load_character_images("the-office", self.office_characters)
        self.friends_images = self.load_character_images("friends", self.friends_characters)
        self.brooklyn_images = self.load_character_images("brooklyn-99", self.brooklyn_characters)

    def load_and_transform_image(self, filename):
        """
        Load an image, convert it, and apply transparency settings.
        """
        image = pygame.image.load(os.path.join("images", filename)).convert()
        image.set_colorkey((255, 255, 255))  # Set white as transparent
        return pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

    def load_character_images(self, folder, characters):
        """
        Load and process character images for a given folder and character list.
        """
        images = {}
        for character in characters:
            try:
                # Load image with alpha transparency
                image = pygame.image.load(
                    os.path.join("images", folder, character + ".png")
                ).convert()
                image.set_colorkey((255, 255, 255)) 
                images[character.capitalize()] = pygame.transform.scale(image, DEFAULT_HEAD_SIZE)
            except pygame.error as e:
                print(f"Error loading image for {character}: {e}")
        return images


    def draw_main_screen(self):
        """
        Draw the main screen with the show selection logos.
        """
        self.world.blit(self.background, (0, 0))

        # Draw logos for show selection
        self.world.blit(self.office_logo, (100, 300))
        self.world.blit(self.friends_logo, (500, 700))
        self.world.blit(self.brooklyn_logo, (900, 275))

        pygame.display.flip()

    def draw_question_screen(self, quote, score, num_questions):
        """
        Draw the screen for displaying a question and input.
        """
        self.world.blit(self.empty_background, (0, 0))

        # Quote
        quote_text = self.font.render(f"Quote: {quote}", True, (255, 255, 255))
        self.world.blit(quote_text, (50, 150))

        # Score and question count
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        question_text = self.font.render(f"Question: {num_questions}/7", True, (255, 255, 255))
        self.world.blit(score_text, (50, 50))
        self.world.blit(question_text, (FRAME_WIDTH - 300, 50))

        pygame.display.flip()

    def draw_options(self, characters, answer, selected_show):
        """
        Draw the options for characters on the screen.
        """
        answer_pos = None
        characters_dict = {
            characters[0]: (200, 200),
            characters[1]: (900, 200),
            characters[2]: (900, 600),
            characters[3]: (200, 600),
        }

        print(f"Populating images for show: {selected_show}")

        for character in characters:
            image = self.office_images.get(character) if selected_show == "The Office" else \
                    self.friends_images.get(character) if selected_show == "Friends" else \
                    self.brooklyn_images.get(character)
            if image is None:
                print(f"Warning: Image for character '{character}' not found.")
                continue
            self.world.blit(image, characters_dict[character])

        for character, position in characters_dict.items():
            if answer == character:
                answer_pos = position

        pygame.display.flip()
        return answer_pos

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True
        self.question_active = False

    def handle_events(self):
        """
        Handle user inputs.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if not self.question_active:  # Show selection
                    # Office logo bounds
                    if 100 <= x <= 100 + DEFAULT_IMAGE_SIZE[0] and 300 <= y <= 300 + DEFAULT_IMAGE_SIZE[1]:
                        self.model.selected_show = "The Office"
                        self.view.images = self.view.office_images
                    # Friends logo bounds
                    elif 500 <= x <= 500 + DEFAULT_IMAGE_SIZE[0] and 700 <= y <= 700 + DEFAULT_IMAGE_SIZE[1]:
                        self.model.selected_show = "Friends"
                        self.view.images = self.view.friends_images
                    # Brooklyn 99 logo bounds
                    elif 900 <= x <= 900 + DEFAULT_IMAGE_SIZE[0] and 275 <= y <= 275 + DEFAULT_IMAGE_SIZE[1]:
                        self.model.selected_show = "Brooklyn 99"
                        self.view.images = self.view.brooklyn_images
                    print(f"You selected the show {self.model.selected_show}")
                else:  # During question
                    text_width = 200
                    text_height = 200
                    for character, pos in {
                        "Michael": (300, 100),
                        "Dwight": (700, 100),
                        "Jim": (700, 700),
                        "Pam": (300, 700),
                    }.items():
                        if pos[0] <= x <= pos[0] + text_width and pos[1] <= y <= pos[1] + text_height:
                            if character == self.model.current_answer:
                                print(f"Correct! You clicked on {character}.")
                                self.model.score += 1
                            else:
                                print(f"Wrong! You clicked on {character}.")
                            self.model.num_questions += 1

    def run_game(self):
        """
        Main game loop.
        """
        while self.running:
            self.handle_events()

            if self.model.selected_show is None:
                self.view.draw_main_screen()
            else:
                if self.model.num_questions < self.model.total_questions:
                    if not self.question_active:
                        self.model.current_quote = "Who said this quote?"
                        self.model.current_answer = random.choice(["Michael", "Dwight", "Jim", "Pam"])
                        self.question_active = True

                    self.view.draw_question_screen(
                        quote=self.model.current_quote,
                        score=self.model.score,
                        num_questions=self.model.num_questions,
                    )
                    self.view.draw_options(
                        ["Michael", "Dwight", "Jim", "Pam"],
                        self.model.current_answer,
                        self.model.selected_show,  # Pass the selected show
                    )
                else:
                    print(f"Game over! Final Score: {self.model.score}")
                    self.running = False

            clock.tick(30)

if __name__ == "__main__":
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.run_game()
