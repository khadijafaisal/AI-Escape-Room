import pygame
import os

# Window settings
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 600
FPS = 60

# Cell settings
CELL_SIZE = 150  

# Colors
DARK = (33, 33, 33)
GRAY = (100, 100, 100)
DARK_BROWN = (101, 67, 33)    # Available cells
PURPLE = (128, 0, 128)        # Traversed path
EXIT_BROWN = (139, 69, 19)    # Exit cell color

# Game objects
CELL = pygame.Surface([CELL_SIZE, CELL_SIZE])
DOOR = pygame.Surface([CELL_SIZE, 20])

# Fonts
pygame.font.init()
LABEL_FONT = pygame.font.SysFont('Arial', 20)
SPAWN_FONT = pygame.font.SysFont('Arial', 35)
RIDDLE_FONT = pygame.font.SysFont('Arial', 16)

# Assets
KEY_IMG = pygame.image.load(os.path.join('assets', 'key.png'))
KEY = pygame.transform.scale(KEY_IMG, (60, 60))
AGENT_IMG = pygame.image.load(os.path.join('assets', 'agent.png'))
AGENT = pygame.transform.scale(AGENT_IMG, (80, 80))