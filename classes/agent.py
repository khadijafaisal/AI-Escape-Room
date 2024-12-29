from typing import Optional
from utils.constants import *
from classes.cell import Cell
from classes.challenges.riddle import Riddle
from classes.challenges.quote_challenge import QuoteChallenge
from classes.challenges.caesar_cipher import CaesarCipher

class Agent:
    """
    Represents a game agent that can move around the grid and interact with challenges.
    """
    def __init__(self):
        """Initialize the agent with default values."""
        self.key_count: int = 0
        self.cell: Optional[Cell] = None
        self.search_dist: int = 1
        self.ref_cell: Optional[Cell] = None
        self.state = None  
        self.move: Optional[str] = None
        self.solving_riddle: bool = False
        self.solving_quote: bool = False
        self.solving_cipher: bool = False

    def try_solve_riddle(self, riddle: Riddle, answer: str) -> bool:
        """
        Attempt to solve a riddle challenge.
        
        Args:
            riddle: The riddle challenge to solve
            answer: The proposed answer
            
        Returns:
            bool: True if solved correctly, False otherwise
        """
        if answer.lower().strip() == riddle.answer:
            riddle.solved = True
            self.key_pickup()
            riddle.active = False
            return True
        return False

    def try_solve_quote(self, quote: QuoteChallenge, answer: str) -> bool:
        """
        Attempt to solve a quote challenge.
        
        Args:
            quote: The quote challenge to solve
            answer: The proposed answer
            
        Returns:
            bool: True if solved correctly, False otherwise
        """
        if answer.lower().strip() == quote.missing_word:
            quote.solved = True
            self.key_pickup()
            quote.active = False
            return True
        return False

    def try_solve_cipher(self, cipher: CaesarCipher, answer: str) -> bool:
        """
        Attempt to solve a cipher challenge.
        
        Args:
            cipher: The cipher challenge to solve
            answer: The proposed answer
            
        Returns:
            bool: True if solved correctly, False otherwise
        """
        if answer.lower().strip() == cipher.solution:
            cipher.solved = True
            self.key_pickup()
            cipher.active = False
            return True
        return False

    def cw(self) -> None:
        """Move the agent clockwise based on current position."""
        if self.cell.name in ['a1', 'b1']:
            self.move_right()
            self.move = 'R'
        elif self.cell.name in ['c1', 'c2']:
            self.move_down()
            self.move = 'D'
        elif self.cell.name in ['c3', 'b3']:
            self.move_left()
            self.move = 'L'
        elif self.cell.name in ['a3', 'a2']:
            self.move_up()
            self.move = 'U'

    def ccw(self) -> None:
        """Move the agent counter-clockwise based on current position."""
        if self.cell.name in ['c1', 'b1']:
            self.move_left()
            self.move = 'L'
        elif self.cell.name in ['c3', 'c2']:
            self.move_up()
            self.move = 'U'
        elif self.cell.name in ['a3', 'b3']:
            self.move_right()
            self.move = 'R'
        elif self.cell.name in ['a1', 'a2']:
            self.move_down()
            self.move = 'D'

    def move_up(self) -> None:
        """Move the agent up one cell if possible."""
        next_cell = self.cell.grid[self.cell.y-1][self.cell.x]
        if next_cell.traversable:
            self.cell = next_cell

    def move_down(self) -> None:
        """Move the agent down one cell if possible."""
        next_cell = self.cell.grid[self.cell.y+1][self.cell.x]
        if next_cell.traversable:
            self.cell = next_cell

    def move_left(self) -> None:
        """Move the agent left one cell if possible."""
        next_cell = self.cell.grid[self.cell.y][self.cell.x-1]
        if next_cell.traversable:
            self.cell = next_cell

    def move_right(self) -> None:
        """Move the agent right one cell if possible."""
        next_cell = self.cell.grid[self.cell.y][self.cell.x+1]
        if next_cell.traversable:
            self.cell = next_cell

    def key_pickup(self) -> None:
        """Pick up a key from the current cell."""
        self.key_count += 1
        self.cell.key.taken = True
        self.cell.set_key(None)

    def reset(self) -> None:
        """Reset the agent to initial state."""
        self.key_count = 0
        self.cell = None
        self.state = None
        self.move = None
        self.solving_riddle = False
        self.solving_quote = False
        self.solving_cipher = False