import pygame

class Door:
    def __init__(self):
        self.opened = False
        self.surface = pygame.Surface([150, 20])
        self.rect = pygame.Rect(300, 130, 150, 20)
        self.color = (162, 97, 59)  # Brown door color
        
    def draw(self, screen):
        """Draw the door on the screen if it's not opened"""
        if not self.opened:
            self.surface.fill(self.color)
            screen.blit(self.surface, (self.rect.x, self.rect.y))
    
    def open(self):
        """Open the door"""
        self.opened = True
    
    def close(self):
        """Close the door"""
        self.opened = False
    
    def is_open(self):
        """Check if the door is open"""
        return self.opened