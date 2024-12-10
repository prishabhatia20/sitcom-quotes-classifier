import pygame
import os
from constants import FRAME_WIDTH, FRAME_HEIGHT

DEFAULT_IMAGE_SIZE = (500, 250)


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
    def __init__(self, model):
        # Screen dimensions
        self.frame_width = FRAME_WIDTH
        self.frame_height = FRAME_HEIGHT

        # Create a display window using Pygame
        self.world = pygame.display.set_mode([self.frame_width, self.frame_height])

        # Load the main screen image
        self.background = self.background = pygame.image.load(
            os.path.join("images", "main_background.png")
        ).convert()
        self.background = pygame.transform.scale(self.background, (self.frame_width, self.frame_height))

        self.empty_background = pygame.image.load(
            os.path.join("images", "empty_background.png")
        ).convert()
        self.empty_background = pygame.transform.scale(self.empty_background, (self.frame_width, self.frame_height))

        # Load show logos
        self.office_logo = pygame.image.load(
            os.path.join("images", "the_office_logo.png")
        ).convert()

        self.office_logo.convert_alpha()
        self.office_logo.set_colorkey((255, 255, 255))
        self.office_logo = pygame.transform.scale(self.office_logo, DEFAULT_IMAGE_SIZE)

        self.friends_logo = pygame.image.load(
            os.path.join("images", "friends_logo.png")
        ).convert()
        self.friends_logo.convert_alpha()
        self.friends_logo.set_colorkey((255, 255, 255))

        self.friends_logo = pygame.transform.scale(self.friends_logo, DEFAULT_IMAGE_SIZE)


        self.brooklyn_logo = pygame.image.load(
            os.path.join("images", "brooklyn_logo.png")
        ).convert()
        self.brooklyn_logo.convert_alpha()
        self.brooklyn_logo.set_colorkey((255, 255, 255))

        self.brooklyn_logo = pygame.transform.scale(self.brooklyn_logo, DEFAULT_IMAGE_SIZE)

        # Fonts
        self.font = pygame.font.Font(None, 50)

        self.office_characters = ["michael", "dwight", "jim", "pam"]
        self.friends_characters = ["rachel", "phoebe", "monica", "joey", "chandler", "ross"]

        ########## ADD GINA AND HITCHCOCK ##################
        self.brooklyn_characters = ["jake", "rosa", "amy", "holt", "charles", "scully", "terry"]

        self.office_images = {}
        self.friends_images = {}
        self.brooklyn_images = {}
        self.images = {}

        for character in self.office_characters:
            image = pygame.image.load(
                os.path.join("images", "the-office", character + ".jpg")
            ).convert()
            image.convert_alpha()

            image.set_colorkey((255, 255, 255))
            self.office_images[character] = image

        for character in self.friends_characters:
            image = pygame.image.load(
                os.path.join("images", "friends", character + ".jpg")
            ).convert()
            image.convert_alpha()

            image.set_colorkey((255, 255, 255))
            self.friends_images[character] = image

        for character in self.brooklyn_characters:
            image = pygame.image.load(
                os.path.join("images", "brooklyn-99", character + ".jpg")
            ).convert()
            image.convert_alpha()

            image.set_colorkey((255, 255, 255))
            self.brooklyn_images[character] = image


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
        model.num_questions += 1
    
    def draw_options(self, characters, answer):
        answer_pos = None
        characters_dict = {characters[0]: (300, 100),
                           characters[1]: (700, 100),
                           characters[2]: (700, 700),
                           characters[3]: (300, 700)}
        print("I am here")
        self.world.blit(characters[0], characters_dict.get(characters[0]))
        self.world.blit(characters[1], characters_dict.get(characters[1]))
        self.world.blit(characters[2], characters_dict.get(characters[2]))
        self.world.blit(characters[3], characters_dict.get(characters[3]))


        for character in characters_dict:
            print(f"character: {character}")
            print(f"range: {range}")
            if answer == character:
                answer_pos = characters_dict.get(character)
        pygame.display.flip()
        return answer_pos


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True

    def handle_events(self):
        """
        Handle user inputs.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # Handle show selection
                x, y = event.pos
                # Office logo bounds
                if 100 <= x <= 100 + DEFAULT_IMAGE_SIZE[0] and 300 <= y <= 300 + DEFAULT_IMAGE_SIZE[1]:
                    self.model.selected_show = "The Office"
                    self.view.images = self.view.office_images
                # Friends logo bounds
                elif 500 <= x <= 500 + DEFAULT_IMAGE_SIZE[0] and 700 <= y <= 700 + DEFAULT_IMAGE_SIZE[1]:
                    self.model.selected_show = "Friends"
                    self.view.images = self.view.friends_images
                # Brooklyn logo bounds
                elif 900 <= x <= 900 + DEFAULT_IMAGE_SIZE[0] and 275 <= y <= 275 + DEFAULT_IMAGE_SIZE[1]:
                    self.model.selected_show = "Brooklyn 99"
                    self.view.images = self.view.brooklyn_images
                print(f"You selected the show {self.model.selected_show}")    
    def handle_answer_click(self, answer_pos):
        text_width = 50
        text_height = 30
        x_click = answer_pos[0]
        y_click = answer_pos[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if x_click <= x + text_width and y_click <= y <= y_click + text_height:
                    model.score += 1
        

    def run_game(self):
        """
        Main game loop.
        """
        while self.running:
            self.handle_events()

            if self.model.selected_show is None:
                self.view.draw_main_screen()
            else:
                while self.model.num_questions < 8:
                    self.view.draw_question_screen(
                        quote="Who said this quote?", 
                        score=self.model.score, 
                        num_questions=self.model.num_questions
                    )

                    pos = self.view.draw_options(["Michael", "Dwight", "Andy", "Pam"], "Michael")
                    self.handle_answer_click(pos)


            clock.tick(30)

if __name__ == "__main__":
    model = Model()
    view = View(model)
    controller = Controller(model, view)
    controller.run_game()
