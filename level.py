import pygame
from classes.challenges.caesar_cipher import CaesarCipher
from classes.challenges.quote_challenge import QuoteChallenge
from classes.challenges.riddle import Riddle
from utils.constants import *

class Level:
    def __init__(self, number, challenges, grid, start_positions, exit_position):
        self.number = number
        self.challenges = challenges  # List of challenges (riddles, quotes, ciphers)
        self.grid = grid
        self.start_positions = start_positions if start_positions else []
        self.exit_position = exit_position
        
    def initialize(self, agent):
        agent.reset()
        self.reset_challenges()
        return True

    def reset_challenges(self):
        for challenge in self.challenges:
            challenge.reset()


    def check_completion(self, agent):
        all_challenges_solved = all(challenge.solved for challenge in self.challenges)
        at_exit = agent.cell.name == 'ex'  # Check if agent is at exit cell
        return all_challenges_solved and at_exit

    def draw(self, screen):
        # Draw the base grid
        self.draw_grid(screen)
        
        # Draw current challenge if active
        if self.current_challenge and self.current_challenge.active:
            self.draw_challenge(screen)

    def draw_grid(self, screen):
     # Add exit visualization
     exit_x = self.exit_position[0] * CELL_SIZE
     exit_y = self.exit_position[1] * CELL_SIZE
     pygame.draw.rect(screen, (0, 255, 0), (exit_x, exit_y, CELL_SIZE, CELL_SIZE), 4)

    def draw_challenge(self, screen):
        if isinstance(self.current_challenge, Riddle):
            self.draw_riddle(screen)
        elif isinstance(self.current_challenge, QuoteChallenge):
            self.draw_quote(screen)
        elif isinstance(self.current_challenge, CaesarCipher):
            self.draw_cipher(screen)

    def draw_riddle(self, screen):
        s = pygame.Surface((400, 200))
        s.set_alpha(230)
        s.fill((50, 50, 50))
        screen.blit(s, (25, 200))

        text = RIDDLE_FONT.render(self.current_challenge.question, True, (255, 255, 255))
        screen.blit(text, (35, 220))

        pygame.draw.rect(screen, (200, 200, 200), (35, 300, 380, 30))
        input_text = RIDDLE_FONT.render(self.current_challenge.user_input + "_", True, (0, 0, 0))
        screen.blit(input_text, (40, 307))

    def draw_quote(self, screen):
        s = pygame.Surface((400, 200))
        s.set_alpha(230)
        s.fill((50, 50, 50))
        screen.blit(s, (25, 200))

        text = RIDDLE_FONT.render(self.current_challenge.quote, True, (255, 255, 255))
        screen.blit(text, (35, 220))

        pygame.draw.rect(screen, (200, 200, 200), (35, 300, 380, 30))
        input_text = RIDDLE_FONT.render(self.current_challenge.user_input + "_", True, (0, 0, 0))
        screen.blit(input_text, (40, 307))

    def draw_cipher(self, screen):
        s = pygame.Surface((400, 200))
        s.set_alpha(230)
        s.fill((50, 50, 50))
        screen.blit(s, (25, 200))

        text = RIDDLE_FONT.render(f"Decrypt: {self.current_challenge.message}", True, (255, 255, 255))
        hint = RIDDLE_FONT.render(f"Hint: Caesar cipher with shift {self.current_challenge.shift}", True, (255, 255, 255))
        screen.blit(text, (35, 220))
        screen.blit(hint, (35, 250))

        pygame.draw.rect(screen, (200, 200, 200), (35, 300, 380, 30))
        input_text = RIDDLE_FONT.render(self.current_challenge.user_input + "_", True, (0, 0, 0))
        screen.blit(input_text, (40, 307))