import re, os, sys, time, random, math
import exception

from typing import NoReturn

from constants import *
from cfttypes import *

from cell import *


class Interpreter:
    def __init__(self, source: str):

        self.cells: dict[str, Cell]                 = {}    # dict of all cells of the program
        self.execution_stack: list[ExecutionFrame]  = []    # stack of all executing blocks
        
        self.__current_frame: ExecutionFrame        = None  # metadata of current block 
        self.__will_skip_next_line: bool            = False # if true, the next line'll be skipped (using only in conditions)
        self.__is_return_called: bool               = False # if true, the current executing block'll be finished
        self.__is_executing_new_block: bool         = False # if true, the program will start executing a new block
        self.__cls_command: str                     = "cls" if sys.platform == "win32" else "clear -r" # for 12's command
        self.__current_line: list[str]              = None  # value of current line with command and its args
        self.__current_line_number: int             = None  # value of line number of current command
        self.__current_line_str: str                = None  # value of current command in string version

        self.blocks: dict[str, BlockData] = self.parse(source)
    
    # region Interpretation
    def interpret(self) -> None:

        self.execute_block(ENTER_BLOCK, False, 0)

        while self.execution_stack:
            self.__current_frame = self.execution_stack.pop()
            current_block: BlockData = self.blocks[self.__current_frame.block_name]

            # ------
            if self.__current_frame.block_name not in self.blocks:

                # if enter block doesn't exists
                if self.__current_frame.block_name == ENTER_BLOCK:
                    self.handle_error("CFTE11")

                # else if it's another block called from code and it doesn't exists
                else:
                    self.handle_error("CFTE10", name = self.__current_frame.block_name)
            # ------

            while self.__current_frame.index < len(current_block.data):

                self.__current_line         = current_block.data[self.__current_frame.index][1]
                self.__current_line_number  = current_block.data[self.__current_frame.index][0]
                self.__current_line_str     = " ".join(self.__current_line)

                # if a condition block was called and it returned true, then the next command'll be skipped
                if self.__will_skip_next_line:
                    self.__will_skip_next_line = False
                    self.__current_frame.index += 1
                    continue

                # interpreting a command
                self.interpret_line()
                self.__current_frame.index += 1
                # ------
                
                # if return called (a 42 command) or a new block's started executing, then current block'll break
                if self.__is_return_called or self.__is_executing_new_block:
                    break
            
            # when the block has ended and the block's looped and the return command's not been called, the block'll start again
            if self.__current_frame.is_looping and not self.__is_return_called:
                self.execute_block(self.__current_frame.block_name, self.__current_frame.is_looping, 0)

            # if a new block has started and the current block has not yet finished, the program will add the current block
            # to the execution stack to execute the remaining instruction in the old block after the new one is finished
            elif self.__is_executing_new_block and self.__current_frame.index < len(current_block.data):
                self.execute_block(self.__current_frame.block_name, self.__current_frame.is_looping, self.__current_frame.index)
                self.execution_stack[-1], self.execution_stack[-2] = self.execution_stack[-2], self.execution_stack[-1]

            self.__is_return_called       = False
            self.__is_executing_new_block = False
        
        self.cft_exit()
    #endregion
    
    #region Commands
    def interpret_line(self) -> None:
        _COMMAND = self.get_argument(LineArgument.COMMAND)

        if _COMMAND == EXIT:
            self.cft_exit()
        
        elif _COMMAND == PRINT:
            cell: Cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            formatted_value = str(cell.value).replace("\\n", "\n")
            print(formatted_value, end = "", flush = True)

        elif _COMMAND == INPUT:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            value = input()
            self.update_value(cell, value)

        elif _COMMAND == ASSIGN_VALUE:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            value = self.get_argument(LineArgument.SECOND)
            self.update_value(cell, value)
        
        elif _COMMAND == SUM_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2: Cell = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                result = cell1.value + cell2.value
                self.update_value(cell1, result, False)
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == SUBTRACT_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2: Cell = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value - cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == MULTIPLY_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2: Cell = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value * cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == DIVIDE_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2: Cell = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value / cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == INCREMENT_CELL:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            self.update_value(cell, 1, UpdateMode.ADD)
        
        elif _COMMAND == DECREMENT_CELL:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            self.update_value(cell, -1, UpdateMode.ADD)
        
        elif _COMMAND == MODULO_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2: Cell = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value % cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == CLEAR_CONSOLE:
            os.system(self.__cls_command)
        
        elif _COMMAND == EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if not cell1.value == cell2.value:
                self.__will_skip_next_line = True
        
        elif _COMMAND == NOT_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if not cell1.value != cell2.value:
                self.__will_skip_next_line = True
        
        elif _COMMAND == GREATER_THAN_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if not cell1.value > cell2.value:
                self.__will_skip_next_line = True
        
        elif _COMMAND == LESS_THAN_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if not cell1.value < cell2.value:
                self.__will_skip_next_line = True
        
        elif _COMMAND == GREATER_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if not cell1.value >= cell2.value:
                self.__will_skip_next_line = True

        elif _COMMAND == LESS_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if not cell1.value <= cell2.value:
                self.__will_skip_next_line = True
        
        elif _COMMAND == UPPERCASE_CELL:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))

            if isinstance(cell, StringCell):
                cell.value = cell.value.upper()
            else:
                self.handle_error("CFTE5", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == LOWERCASE_CELL:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))

            if isinstance(cell, StringCell):
                cell.value = cell.value.lower()
            else:
                self.handle_error("CFTE5", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == LENGTH_CELL:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell2, StringCell):
                self.update_value(cell1, len(cell2.value))
            else:
                self.handle_error("CFTE5", self.__current_line_number, self.__current_line_str)

        elif _COMMAND == INVERT_CELL:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))

            if isinstance(cell, StringCell):
                cell.value = cell.value[::-1]
            else:
                cell.value = -cell.value
        
        elif _COMMAND == CALL_BLOCK:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            value = str(cell.value)

            if value in self.blocks:
                self.execute_block(value, False, 0)
                self.__is_executing_new_block = True
            else:
                self.handle_error("CFTE10", name = cell.value)
        
        elif _COMMAND == ADD_CONSTANT:
            value = self.get_argument(LineArgument.SECOND)
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))

            self.update_value(cell, value, UpdateMode.ADD)
        
        elif _COMMAND == SWAP_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                cell1.value, cell2.value = cell2.value, cell1.value
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == COPY_CELL:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                cell1.value = cell2.value
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == DELETE_CHAR:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, StringCell) and isinstance(cell2, IntegerCell):
                cell1.value[:cell2.value] + cell1.value[cell2.value+1:]
            else:
                self.handle_error("CFTE4", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == STRING_TO_INT:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))
            self.update_value(cell1, cell2.value)
        
        elif _COMMAND == INT_TO_STRING:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))
            self.update_value(cell1, str(cell2.value))
        
        elif _COMMAND == BITWISE_AND:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value & cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == BITWISE_OR:
            result = None
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value | cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == BITWISE_XOR:
            result = None
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value ^ cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
            else:
                self.handle_error("CFTE7", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == BITWISE_NOT:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))

            if not isinstance(cell, StringCell):
                cell.value = ~cell.value
            else:
                self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == SLEEP:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))

            if not isinstance(cell, StringCell):
                time.sleep(cell.value)
            else:
                self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == START_LOOP:
            cell = self.get_cell(self.get_argument(LineArgument.FIRST))
            value = cell.value

            if value in self.blocks:
                self.execute_block(value, True, 0)
                self.__is_executing_new_block = True
            else:
                self.handle_error("CFTE10", name = cell.value)
        
        elif _COMMAND == RANDOM_CHAR:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)) and isinstance(cell1, StringCell):
                cell1.value = random.choice(cell2.value)
            else:
                self.handle_error("CFTE5", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == MAX_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = max(cell1.value, cell2.value)
            else:
                self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == MIN_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = min(cell1.value, cell2.value)
            else:
                self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == GCD_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = math.gcd(cell1.value, cell2.value)
            else:
                self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == LCM_CELLS:
            cell1 = self.get_cell(self.get_argument(LineArgument.FIRST))
            cell2 = self.get_cell(self.get_argument(LineArgument.SECOND))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = math.lcm(cell1.value, cell2.value)
            else:
                self.handle_error("CFTE6", self.__current_line_number, self.__current_line_str)
        
        elif _COMMAND == CREATE_CELL:
            name = self.get_argument(LineArgument.FIRST)
            data_type = self.get_argument(LineArgument.SECOND)

            if not Cell.is_name_correct(name):
                self.handle_error("CFTE2", self.__current_line_number, self.__current_line_str, name = name)

            match data_type:
                case CellDataType.INTEGER.value:
                    cell: Cell = IntegerCell()
                case CellDataType.FLOAT.value:
                    cell: Cell = FloatCell()
                case CellDataType.STRING.value:
                    cell: Cell = StringCell()
                case _:
                    self.handle_error("CFTE1", self.__current_line_number, self.__current_line_str, data_type = data_type)
            
            self.cells[name] = cell
        
        elif _COMMAND == RETURN:
            self.__is_return_called = True
        
        # if command isn't defined, then the CFTE3 error will handled
        else:
            self.handle_error("CFTE3", self.__current_line_number, self.__current_line_str, command = _COMMAND)
    
    #endregion

    #region Parser
    def parse(self, source: str) -> dict[str, BlockData]:
        
        """
        Parses the source code
        """
        
        lines = [
            line.split(COMMENT_SYMBOL, 1)[0].rstrip()
            for line in source.splitlines()
        ]

        blocks: dict[str, BlockData] = {}
        block: str = None

        for line_number, line in enumerate(lines, 1):
            if not line:
                continue

            if line.startswith(START_BLOCK):
                _, _, block_name = line.partition(' ')
                block = block_name.strip()
                if block:
                    blocks[block] = BlockData()
            elif line.startswith(END_BLOCK):
                block = None
            elif block:
                tokens = [match.group(1) if match.group(1) else match.group(0)
                        for match in re.finditer(r'"([^"]*)"|\S+', line)]
                if tokens:
                    blocks[block].data.append((line_number, tokens))

        return blocks
    #endregion

    #region Methods
    def get_cell(self, name: str) -> Cell:
        
        """
        Returns a cell from the cells
        """

        if (cell := self.cells.get(name, None)) is not None:
            return cell
        
        self.handle_error("CFTE8", self.__current_line_number, self.__current_line_str, name = name)

    def get_argument(self, index: LineArgument) -> str:
        
        """
        Returns an argument value in the line by index
        """
        
        if 0 <= index.value < len(self.__current_line):
            return self.__current_line[index.value]
        self.handle_error("CFTE12", self.__current_line_number, self.__current_line_str)
    
    def update_value(self, cell: Cell, value: str, mode: UpdateMode = UpdateMode.WRITE) -> None:
        
        """
        Updates a cell's value (only write or add)
        """
        
        if isinstance(cell, IntegerCell):
            if Cell.is_number(value):
                match mode:
                    case UpdateMode.WRITE:
                        cell.value = int(value)
                    case UpdateMode.ADD:
                        cell.value += int(value)
            else:
                self.handle_error("CFTE9", self.__current_line_number, self.__current_line_str, data_type = "int")
        
        elif isinstance(cell, FloatCell):
            if Cell.is_number(value):
                match mode:
                    case UpdateMode.WRITE:
                        cell.value = float(value)
                    case UpdateMode.ADD:
                        cell.value += float(value)
            else:
                self.handle_error("CFTE9", self.__current_line_number, self.__current_line_str, data_type = "float")
        
        # else - it's a string 
        else:
            match mode:
                case UpdateMode.WRITE:
                    cell.value = value
                case UpdateMode.ADD:
                    cell.value += value

    def execute_block(self, name: str, is_looping: bool, index: int) -> None:

        """
        Adds a new execution block to the execution stack
        """

        self.execution_stack.append(ExecutionFrame(name, is_looping, index))
    
    def handle_error(self, error_number: str, line: int | None = None, command_in_string: str | None = None, **kwargs) -> NoReturn:
        
        """
        Main function for error handling
        """
        
        formatted_exception = exception.ERRORS[error_number].format(**kwargs)
        exception.Exception(error_number, formatted_exception, line, command_in_string)
        self.cft_exit()

    def cft_exit(self) -> NoReturn:

        """
        Ends program execution
        """

        print("\n[Program Finished]")
        sys.exit()
    
    #endregion