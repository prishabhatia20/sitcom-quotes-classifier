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