from dataclasses import dataclass
from enum import Enum
from typing import Union


class CellDataType(Enum):
    """
    Enum representing possible data types for a cell in memory.
    """

    INTEGER = "0"
    STRING  = "1"
    FLOAT   = "2"

class UpdateMode(Enum):
    """
    Enum defining modes for updating a cell's value.
    """

    WRITE   = "w"   # write mode
    ADD     = "a"   # adding mode

@dataclass
class ExecutionFrame:
    """
    Represents an execution frame, storing metadata about the current block being executed in the interpreter.
    """

    block_name: str     # name of block
    is_looping: bool    # is block looping? (true if only the block's called from a 35 command)
    index: int          # current index in the block

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