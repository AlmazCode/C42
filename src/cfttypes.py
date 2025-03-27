from dataclasses import dataclass


# class for comfortable cell type working
class CellDataType:
    INTEGER = "0"
    STRING  = "1"
    FLOAT   = "2"

# class for comfortable cell value changing
class UpdateMode:
    WRITE   = "w"
    ADD     = "a"

# class for comfortable working with interpreter
@dataclass
class ExecutionFrame:
    block_name: str     # name of block
    is_looping: bool    # is block looping? (true if only the block's called from a 35 command)
    line_number: int    # current line number 