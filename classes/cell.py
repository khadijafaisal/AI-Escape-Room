from typing import Optional, Tuple
from classes.key import Key

class Cell:
    """
    Represents a cell in the game grid.
    """
    def __init__(self, name: str, y: int, x: int, coords: Tuple[int, int], traversable: bool):
        """
        Initialize a cell.
        
        Args:
            name: Cell identifier
            y: Y coordinate in grid
            x: X coordinate in grid
            coords: Display coordinates (x, y)
            traversable: Whether the agent can move to this cell
        """
        self.name = name
        self.x = x
        self.y = y
        self.coords = coords
        self.traversable = traversable
        self.traversed = False
        self.key: Optional[Key] = None

    def set_key(self, key: Optional[Key]) -> None:
        """Set or remove a key from the cell."""
        self.key = key

    def get_key(self) -> Optional[Key]:
        """Get the key in the cell if any."""
        return self.key