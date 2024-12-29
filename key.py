from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.cell import Cell

class Key:
    """
    Represents a key that can be collected by the agent.
    """
    def __init__(self, cell: 'Cell'):
        """
        Initialize a key.
        
        Args:
            cell: The cell where the key is located
        """
        self.cell = cell
        self.taken = False

    def get_cell(self) -> 'Cell':
        """Get the cell where the key is located."""
        return self.cell