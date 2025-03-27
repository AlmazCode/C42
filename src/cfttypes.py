from dataclasses import dataclass
from enum import Enum
from typing import Union

# enum for comfortable cell type working
class CellDataType(Enum):
    INTEGER = "0"
    STRING  = "1"
    FLOAT   = "2"

# enum for comfortable cell value changing
class UpdateMode(Enum):
    WRITE   = "w"
    ADD     = "a"

# class for comfortable working with interpreter
@dataclass
class ExecutionFrame:
    block_name: str     # name of block
    is_looping: bool    # is block looping? (true if only the block's called from a 35 command)
    line_number: int    # current line number

class BlockData:
    """
    Represents a structured data block containing nested lists of integers and string lists.
    """

    def __init__(self, data: list[list[Union[int, list[str]]]] = None):
        """
        Initializes a BlockData object with the given nested list structure.
        """
        self.data = data if data is not None else []

    def __repr__(self) -> str:
        """
        Returns a string representation of the BlockData object.
        """
        return f"BlockData({self.data})"