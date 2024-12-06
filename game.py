import pygame
import os

# Constants for screen dimensions
FRAME_WIDTH = 1370
FRAME_HEIGHT = 1250

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
            os.path.join("images", "background.png")
        ).convert()

        # Load show logos
        self.office_logo = pygame.image.load(
            os.path.join("images", "the_office_logo.png")
        ).convert()

        self.friends_logo = pygame.image.load(
            os.path.join("images", "friends_logo.png")
        ).convert()

        self.brooklyn_logo = pygame.image.load(
            os.path.join("images", "brooklyn_nine-nine_logo.png")
        ).convert()

        # Fonts
        self.font = pygame.font.Font(None, 50)

    def draw_main_screen(self):
        """
        Draw the main screen with the show selection logos.
        """
        self.world.blit(self.background, (0, 0))

        # Draw logos for show selection
        self.world.blit(self.office_logo, (100, 100))
        self.world.blit(self.friends_logo, (500, 100))
        self.world.blit(self.brooklyn_logo, (900, 100))

        # Title
        title_text = self.font.render("Select a Show to Start the Trivia", True, (255, 255, 255))
        self.world.blit(title_text, (FRAME_WIDTH // 2 - title_text.get_width() // 2, 50))

        pygame.display.flip()

    def draw_question_screen(self, quote, score, num_questions):
        """
        Draw the screen for displaying a question and input.
        """
        self.world.fill((0, 0, 0))

        # Quote
        quote_text = self.font.render(f"Quote: {quote}", True, (255, 255, 255))
        self.world.blit(quote_text, (50, 150))

        # Score and question count
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        question_text = self.font.render(f"Question: {num_questions}/7", True, (255, 255, 255))
        self.world.blit(score_text, (50, 50))
        self.world.blit(question_text, (FRAME_WIDTH - 300, 50))

        pygame.display.flip()

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
                if 100 < x < 300 and 100 < y < 300:  # Office logo bounds
                    self.model.selected_show = "The Office"
                elif 500 < x < 700 and 100 < y < 300:  # Friends logo bounds
                    self.model.selected_show = "Friends"
                elif 900 < x < 1100 and 100 < y < 300:  # Brooklyn logo bounds
                    self.model.selected_show = "Brooklyn 99"

    def run_game(self):
        """
        Main game loop.
        """
        while self.running:
            self.handle_events()

            if self.model.selected_show is None:
                self.view.draw_main_screen()
            else:
                # Display question screen (placeholder quote)
                self.view.draw_question_screen(
                    quote="Who said this quote?", 
                    score=self.model.score, 
                    num_questions=self.model.num_questions
                )

            clock.tick(30)

if __name__ == "__main__":
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.run_game()
