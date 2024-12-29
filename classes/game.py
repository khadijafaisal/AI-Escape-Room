from queue import PriorityQueue
import pygame
from classes.cell import Cell
from classes.level import Level
from classes.challenges.riddle import Riddle
from classes.challenges.quote_challenge import QuoteChallenge
from classes.challenges.caesar_cipher import CaesarCipher
from utils.constants import *
from utils.helpers import manhattan_distance

pygame.font.init()
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.valid_cells = {
            'a1': 1, 'a2': 2, 'a3': 3,
            'b3': 4, 'c1': 5, 'c2': 6
        }
        pygame.init()
        pygame.font.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Escape Room AI')
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level = 0
        self.game_state = {
            'score': 0,
            'time': 0,
            'completed_challenges': set(),
            'current_level_progress': 0
        }
        
        self.key_img = pygame.image.load('assets/key.png')
        self.key_img = pygame.transform.scale(self.key_img, (60, 60))
        self.agent_img = pygame.image.load('assets/agent.png')
        self.agent_img = pygame.transform.scale(self.agent_img, (80, 80))
        
        self.grid = self._create_grid()
        self.waiting_for_start = True
        self.start_pos = None
        self.exit_position = (2, 0)
        self.current_path = None
        self.current_path_index = 0
        self.visited_cells = set()
        self.key_positions = [(2, 3), (0, 2)]
        self.collected_keys = set()
        self.current_challenge = None
        self.user_input = ""
        self.door_opened = False
        self.collected_keys = set()
        self.current_level = 0
        self.key_positions = [(2, 3), (0, 2)]  
        self.exit_position = (2, 0)
        self.current_path = None
        self.current_path_index = 0
        self.current_challenge = None
        
        self.levels = self.init_levels()
        self.step_delay = 500
        self.last_step_time = 0

    def _create_grid(self):
        grid = []
        for y in range(5):
            row = []
            for x in range(3):
                if y == 0:
                    cell_name = f"{'ex' if x == 2 else f'o{x+1}'}"
                else:
                    cell_name = f"{chr(97 + x)}{y}"
                traversable = cell_name not in ('b2', 'o1', 'o2')
                coords = (x * CELL_SIZE, y * CELL_SIZE)
                cell = Cell(cell_name, y, x, coords, traversable)
                row.append(cell)
            grid.append(row)
        return grid

    def get_cell(self, x, y):
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x]
        return None

    def get_valid_neighbors(self, pos):
        x, y = pos
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            cell = self.get_cell(new_x, new_y)
            if cell and cell.traversable:
                neighbors.append((new_x, new_y))
        return neighbors

    def bfs_search(self, start, goal):
        if start == goal:
            return []
        queue = [(start, [start])]
        visited = {start}
        while queue:
            current, path = queue.pop(0)
            for next_pos in self.get_valid_neighbors(current):
                if next_pos == goal:
                    return path + [next_pos]
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        return None

    def dfs_search(self, start, goal):
        if start == goal:
            return []
        stack = [(start, [start])]
        visited = {start}
        while stack:
            current, path = stack.pop()
            for next_pos in self.get_valid_neighbors(current):
                if next_pos == goal:
                    return path + [next_pos]
                if next_pos not in visited:
                    visited.add(next_pos)
                    stack.append((next_pos, path + [next_pos]))
        return None

    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put((0, start, [start]))
        visited = {start: 0}
        while not frontier.empty():
            current_cost, current, path = frontier.get()
            if current == goal:
                return path
            for next_pos in self.get_valid_neighbors(current):
                new_cost = current_cost + 1
                if next_pos not in visited or new_cost < visited[next_pos]:
                    visited[next_pos] = new_cost
                    priority = new_cost + manhattan_distance(next_pos, goal)
                    frontier.put((priority, next_pos, path + [next_pos]))
        return None
    
    def reset_level_state(self):
        """Reset all necessary game state for a new level"""
        self.waiting_for_start = True
        self.start_pos = None
        self.current_path = None
        self.current_path_index = 0
        self.visited_cells.clear()
        self.collected_keys.clear()
        self.current_challenge = None
        self.user_input = ""
        self.door_opened = False

    def check_level_completion(self):
        if not self.level_completed:  # Checking if level isn't already marked as completed
            current_pos = self.current_path[self.current_path_index - 1]
            if current_pos == self.exit_position:
                if len(self.collected_keys) == len(self.key_positions):
                    print("Level complete! Moving to next level...")
                    self.level_completed = True
                    self.next_level()
                else:
                    print(f"Collect all keys before exiting! {len(self.collected_keys)}/{len(self.key_positions)} keys collected")

    def run(self):
        while self.running:
            self.handle_events()
            current_time = pygame.time.get_ticks()
            
            if not self.waiting_for_start:
                if self.current_path is None:
                    self.current_path = self.find_path()
                    self.current_path_index = 0
                
                if (not self.current_challenge or not self.current_challenge.active) and \
                   current_time - self.last_step_time >= self.step_delay and \
                   self.current_path_index < len(self.current_path):
                    
                    current_pos = self.current_path[self.current_path_index]
                    self.visited_cells.add(current_pos)
                    
                    # Checking if we're at a key position
                    if current_pos in self.key_positions and current_pos not in self.collected_keys:
                        self.trigger_challenge(current_pos)
                    
                    # Checking if we're at exit with all keys
                    if current_pos == self.exit_position and len(self.collected_keys) == len(self.key_positions):
                        print("Level complete!")
                        self.next_level()
                        continue
                    
                    self.current_path_index += 1
                    self.last_step_time = current_time
            
            self.render()
            self.clock.tick(60)
        
        pygame.quit()

    def find_path(self):
        path = []
        current = self.start_pos
        remaining_keys = list(self.key_positions)
        while remaining_keys:
            nearest_key = min(remaining_keys, key=lambda k: manhattan_distance(current, k))
            key_path = self._get_search_path(current, nearest_key)
            path.extend(key_path)
            current = nearest_key
            remaining_keys.remove(nearest_key)
        exit_path = self._get_search_path(current, self.exit_position)
        path.extend(exit_path)
        return path

    def _get_search_path(self, start, goal):
        if self.current_level == 0:
            return self.bfs_search(start, goal)
        elif self.current_level == 1:
            return self.dfs_search(start, goal)
        else:
            return self.a_star_search(start, goal)

    def trigger_challenge(self, pos):
        print(f"Triggering challenge at position: {pos}")
        """Single point of triggering challenges"""
        challenge_index = self.key_positions.index(pos)
        if challenge_index < len(self.levels[self.current_level].challenges):
            self.current_challenge = self.levels[self.current_level].challenges[challenge_index]
            self.current_challenge.active = True
            self.user_input = ""

    def handle_challenge_answer(self):
        if self.current_challenge and self.current_challenge.active:
            print(f"Checking answer: {self.user_input}")
            if isinstance(self.current_challenge, Riddle):
                if self.current_challenge.try_solve(self.user_input.strip().lower()):
                    self.complete_challenge()
            elif isinstance(self.current_challenge, QuoteChallenge):
                if self.current_challenge.try_solve(self.user_input.strip().lower()):
                    self.complete_challenge()
            elif isinstance(self.current_challenge, CaesarCipher):
                if self.current_challenge.try_solve(self.user_input.strip().lower()):
                    self.complete_challenge()


    def complete_challenge(self):
        if self.current_challenge:
            # Marking the challenge as completed
            self.game_state['completed_challenges'].add(self.current_challenge)
            print("Challenge completed!")
            
            # Adding the current position to collected keys
            current_pos = self.current_path[self.current_path_index - 1]
            self.collected_keys.add(current_pos)
            print(f"Key collected at position: {current_pos}")
            print(f"Challenge completed! Keys collected: {len(self.collected_keys)}/{len(self.key_positions)}")
                
            # Updating the score
            self.game_state['score'] += 50
            print(f"Challenge completed! Keys collected: {len(self.collected_keys)}/{len(self.key_positions)}")
            
            # Checking if we should advance to next level
            if len(self.collected_keys) == len(self.key_positions) and current_pos == self.exit_position:
                print("All keys collected and at exit - advancing to next level!")
                self.next_level()
            
            # Reseting challenge state
            self.current_challenge = None
            self.user_input = ""

    def handle_events(self):
        """Single point of handling all events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.waiting_for_start:
                mouse_pos = pygame.mouse.get_pos()
                cell_x = mouse_pos[0] // CELL_SIZE
                cell_y = mouse_pos[1] // CELL_SIZE
                if self.is_valid_start_position(cell_x, cell_y):
                    self.start_pos = (cell_x, cell_y)
                    self.waiting_for_start = False
                    self.current_path = None
            elif event.type == pygame.KEYDOWN:
                if self.current_challenge and self.current_challenge.active:
                    if event.key == pygame.K_RETURN:
                        self.handle_challenge_answer()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        if len(self.user_input) < 20:  
                            self.user_input += event.unicode


    def next_level(self):
        self.current_level += 1
        if self.current_level < len(self.levels):
            print(f"Starting Level {self.current_level + 1}")
            # Reseting all necessary state
            self.waiting_for_start = True
            self.start_pos = None
            self.current_path = None
            self.current_path_index = 0
            self.visited_cells.clear()
            self.collected_keys.clear()
            self.game_state['score'] += 100
        else:
            print("Game Completed!")
            self.running = False
            
    def render(self):
        self.screen.fill((33, 33, 33))
        for y in range(5):
            for x in range(3):
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell = self.grid[y][x]
                if not cell.traversable:
                    color = DARK
                elif cell.name == 'ex':
                    color = (139, 69, 19)
                elif (x, y) in self.visited_cells:
                    color = (128, 0, 128)
                else:
                    color = (101, 67, 33)
                pygame.draw.rect(self.screen, color, cell_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 2)
                if cell.name == 'ex':
                    label = LABEL_FONT.render("EXIT", True, (255, 255, 255))
                else:
                    label = LABEL_FONT.render(cell.name, True, (255, 255, 255))
                self.screen.blit(label, (x * CELL_SIZE + 10, y * CELL_SIZE + 10))
        for key_pos in self.key_positions:
            if key_pos not in self.collected_keys:
                key_x = key_pos[0] * CELL_SIZE + (CELL_SIZE - 60) // 2
                key_y = key_pos[1] * CELL_SIZE + (CELL_SIZE - 60) // 2
                self.screen.blit(self.key_img, (key_x, key_y))
        if self.current_path and self.current_path_index > 0:
            current_pos = self.current_path[self.current_path_index - 1]
            agent_x = current_pos[0] * CELL_SIZE + (CELL_SIZE - 80) // 2
            agent_y = current_pos[1] * CELL_SIZE + (CELL_SIZE - 80) // 2
            self.screen.blit(self.agent_img, (agent_x, agent_y))
        if self.current_challenge:
            self.draw_challenge()
        if self.waiting_for_start:
            font = pygame.font.SysFont('Arial', 24)
            text = font.render('Click a valid starting position', True, (255, 255, 255))
            self.screen.blit(text, (10, WINDOW_HEIGHT - 40))
        score_text = LABEL_FONT.render(f"Score: {self.game_state['score']}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()


    def is_valid_start_position(self, x, y):
        if y == 0:
            return False
        cell_name = f"{chr(97 + x)}{y}"
        return cell_name in ['a1', 'a2', 'a3', 'b3', 'c1', 'c2']

    def init_levels(self):
        levels = []
        start_positions = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 1), (2, 2)]
        exit_position = (2, 0)
        level1 = Level(
            number=1,
            challenges=[
                Riddle("What has keys but no locks, space but no room, and you can enter but not go in?", "keyboard"),
                CaesarCipher("hello world", 3)
            ],
            grid=self.grid,
            start_positions=start_positions,
            exit_position=exit_position
        )
        levels.append(level1)
        level2 = Level(
            number=2,
            challenges=[
                QuoteChallenge("To be or not to be", "shakespeare"),
                Riddle("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "echo")
            ],
            grid=self.grid,
            start_positions=start_positions,
            exit_position=exit_position
        )
        levels.append(level2)
        level3 = Level(
            number=3,
            challenges=[
                CaesarCipher("escape room", 5),
                QuoteChallenge("Elementary, my dear Watson", "sherlock")
            ],
            grid=self.grid,
            start_positions=start_positions,
            exit_position=exit_position
        )
        levels.append(level3)
        return levels

    def draw_challenge(self):
         # Creating asemi-transparent background surface
         s = pygame.Surface((400, 250))  
         s.set_alpha(230)
         s.fill((50, 50, 50))
         self.screen.blit(s, (25, 150)) 
         
         def wrap_text(text, font, max_width):
             words = text.split(' ')
             lines = []
             current_line = []
             current_width = 0
             
             for word in words:
                 word_surface = font.render(word + ' ', True, (255, 255, 255))
                 word_width = word_surface.get_width()
                 
                 if current_width + word_width <= max_width:
                     current_line.append(word)
                     current_width += word_width
                 else:
                     lines.append(' '.join(current_line))
                     current_line = [word]
                     current_width = word_width
                     
             lines.append(' '.join(current_line))
             return lines
    
      
         if isinstance(self.current_challenge, Riddle):
             text_lines = wrap_text(self.current_challenge.question, RIDDLE_FONT, 380)
             y_offset = 170  # Starting y position
             
             for line in text_lines:
                 text = RIDDLE_FONT.render(line, True, (255, 255, 255))
                 self.screen.blit(text, (35, y_offset))
                 y_offset += 25  # Space between lines
                 
         elif isinstance(self.current_challenge, QuoteChallenge):
             text_lines = wrap_text(self.current_challenge.quote, RIDDLE_FONT, 380)
             y_offset = 170
             
             for line in text_lines:
                 text = RIDDLE_FONT.render(line, True, (255, 255, 255))
                 self.screen.blit(text, (35, y_offset))
                 y_offset += 25
                 
         elif isinstance(self.current_challenge, CaesarCipher):
             text_lines = wrap_text(f"Decrypt: {self.current_challenge.message}", RIDDLE_FONT, 380)
             y_offset = 170
             
             for line in text_lines:
                 text = RIDDLE_FONT.render(line, True, (255, 255, 255))
                 self.screen.blit(text, (35, y_offset))
                 y_offset += 25
                 
             hint = RIDDLE_FONT.render(f"Hint: Caesar cipher with shift {self.current_challenge.shift}", 
                                      True, (255, 255, 255))
             self.screen.blit(hint, (35, y_offset))
             y_offset += 25
    
         # Drawing input box at the bottom of the challenge area
         pygame.draw.rect(self.screen, (200, 200, 200), (35, 350, 380, 30))
         input_text = RIDDLE_FONT.render(self.user_input + "_", True, (0, 0, 0))
         self.screen.blit(input_text, (40, 357))

