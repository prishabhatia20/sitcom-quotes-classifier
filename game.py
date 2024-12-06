import pygame
from constants import WIDTH, HEIGHT
import os
import time
pygame.init()

main_screen = pygame.image.load(
        os.path.join("images", "background.png")
    ).convert()

screen = pygame.display.set_mode((HEIGHT, WIDTH))
clock = pygame.time.Clock()

class Model():
    total_questions = 7
    def __init__(self):
        self.score = 0
        self.num_questions = 0
        self.active = True


class View():
    frame_width = 1370
    frame_height = 1250


    # Create a display window using Pygame
    world = pygame.display.set_mode([frame_width, frame_height])

    # Load the main screen image
    background = pygame.image.load(
        os.path.join("images", "background.png")
    ).convert()

    office_logo = pygame.image.load(
        os.path.join("images", "the_office_logo.png")
    ).convert()

    friends_logo = pygame.image.load(
        os.path.join("images", "friends_logo.png")
    ).convert()

    brooklyn_logo = pygame.image.load(
        os.path.join("images", "brooklyn_logo.png")
    ).convert()

    def __init__(self):

        pass

        def draw_main_screen(self):
            """
            This method draws the score screen onto the pygame window
            """
            self.world.blit(self.background, (0, 0))
            pygame.display.flip()
        