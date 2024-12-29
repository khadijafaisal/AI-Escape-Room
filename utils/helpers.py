import pygame
from utils.constants import DARK, GRAY

def draw_grid(screen):
    """Drawing the game grid"""
    cell = pygame.Surface([150, 150])
    
    # Drawing black cells
    cell.fill(DARK)
    for cell_pos in [(0, 0), (150, 0), (150, 300)]:  # black cell positions
        screen.blit(cell, cell_pos)
        rect = pygame.Rect(cell_pos[0], cell_pos[1], 150, 150)
        pygame.draw.rect(screen, DARK, rect, 1)
    
    # Drawing white cells
    cell.fill(GRAY)
    white_positions = [
        (0, 150), (150, 150), (300, 150),  # row 1
        (0, 300), (300, 300),              # row 2
        (0, 450), (150, 450), (300, 450)   # row 3
    ]
    for cell_pos in white_positions:
        screen.blit(cell, cell_pos)
        rect = pygame.Rect(cell_pos[0], cell_pos[1], 150, 150)
        pygame.draw.rect(screen, DARK, rect, 1)

def draw_labels(screen):
    """Drawing cell labels"""
    label_font = pygame.font.SysFont('Arial', 20)
    
    # Cell names and their positions
    cells = {
        'o1': (0, 0), 'o2': (150, 0), 'ex': (300, 0),
        'a1': (0, 150), 'b1': (150, 150), 'c1': (300, 150),
        'a2': (0, 300), 'b2': (150, 300), 'c2': (300, 300),
        'a3': (0, 450), 'b3': (150, 450), 'c3': (300, 450)
    }
    
    for name, pos in cells.items():
        label = label_font.render(name, True, DARK if name != 'b2' else (200, 200, 200))
        screen.blit(label, (pos[0] + 5, pos[1] + 5))

def draw_spawns(screen):
    """Draw spawn point numbers"""
    spawn_font = pygame.font.SysFont('Arial', 35)
    
    # Spawn positions
    spawns = [
        (0, 450),  # a3
        (0, 300),  # a2
        (0, 150),  # a1
        (300, 150),  # c1
        (300, 300),  # c2
        (150, 450)   # b3
    ]
    
    for i, pos in enumerate(spawns):
        text = spawn_font.render(f'[{i+1}]', True, (255, 255, 255))
        screen.blit(text, (pos[0] + 60, pos[1] + 60))

def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def all_neighbors(pos):
    """Get all neighboring positions"""
    x, y = pos
    return [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]

def reconstruct_path(came_from, start, goal):
    """Reconstruct path from start to goal"""
    current = goal
    path = []
    
    while current != start:
        path.append(current)
        current = came_from[current]
    
    path.append(start)
    path.reverse()
    return path