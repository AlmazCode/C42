import re, os, sys, time, random
import exception

from typing import NoReturn

from constants import *
from cfttypes import *

from cell import *


class Interpreter:
    def __init__(self, source: str):

        self.cells: list[Cell]                      = []    # list of all cells of the program
        self.current_frame: ExecutionFrame          = None  # metadata of current block 
        self.will_skip_next_line                    = False # if true, the next line'll be skipped (using only in conditions)
        self.execution_stack: list[ExecutionFrame]  = []    # stack of all executing blocks
        self.is_return_called: bool                 = False # if true, the current executing block'll be finished
        self.is_executing_new_block                 = False # if true, the program will start executing a new block

        self.blocks = self.parse(source)
    
    # returns current line number in executing block
    @property
    def current_line(self) -> int:
        return self.current_block.data[self.current_frame.index][0]

    # returns current command in executing block
    @property
    def current_command(self) -> list[str]:
        return self.current_block.data[self.current_frame.index][1]
    
    # returns current command (string version) in executing block
    @property
    def current_command_str(self) -> str:
        return " ".join(self.current_block.data[self.current_frame.index][1])
    
    # returns current executing block
    @property
    def current_block(self) -> BlockData:
        return self.blocks[self.current_frame.block_name]
    
    def interpret(self) -> NoReturn:
        
        self.execution_stack.append(
            ExecutionFrame(block_name = ENTER_BLOCK, is_looping = False, index = 0)
        )

        while self.execution_stack:
            self.current_frame = self.execution_stack.pop()
            block = self.current_block

            if self.current_frame.block_name not in self.blocks:

                # if enter block doesn't exists
                if self.current_frame.block_name == ENTER_BLOCK:
                    self.handle_error("CFTE11")

                # else if it's another block called from code and it doesn't exists
                else:
                    self.handle_error("CFTE10", name = self.current_frame.block_name)

            while self.current_frame.index < len(block.data):

                if self.will_skip_next_line:
                    self.will_skip_next_line = False
                    self.current_frame.index += 1
                    continue

                next_command = block.data[self.current_frame.index + 1][1] if self.current_frame.index + 1 < len(block.data) else None
                self.interpret_line(self.current_command, next_command)

                if self.is_return_called or self.is_executing_new_block:
                    break

            if self.current_frame.is_looping and not self.is_return_called:
                self.execution_stack.append(
                    ExecutionFrame(block_name = self.current_frame.block_name, is_looping = self.current_frame.is_looping, index = 0)
                )
            elif self.is_executing_new_block and self.current_frame.index < len(block.data):
                self.execution_stack.append(
                    ExecutionFrame(block_name = self.current_frame.block_name, is_looping = self.current_frame.is_looping,
                                   index = self.current_frame.index)
                )
                self.execution_stack[-1], self.execution_stack[-2] = self.execution_stack[-2], self.execution_stack[-1]

            self.is_return_called       = False
            self.is_executing_new_block = False
        
        self.cft_exit()
    
    def interpret_line(self, line: list[str], next_line: list[str], force_update_line: bool = False) -> NoReturn:
        command = line[0]

        if force_update_line:
            self.current_frame.index += 1

        if command == EXIT:
            self.cft_exit()
        
        # PRINT command realization
        elif command == PRINT:
            cell: Cell = self.get_cell(self.get_argument(1))
            formatted_value = str(cell.value).replace("\\n", "\n")
            print(formatted_value, end = "", flush = True)
    
        elif command == INPUT:
            cell = self.get_cell(self.get_argument(1))
            value = input()
            self.update_value(cell, value)

        elif command == ASSIGN_VALUE:
            cell = self.get_cell(self.get_argument(1))
            value = self.get_argument(2)
            self.update_value(cell, value)
        
        elif command == SUM_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                result = cell1.value + cell2.value
                self.update_value(cell1, result, False)
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == SUBTRACT_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value - cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line, self.current_command_str)
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == MULTIPLY_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value * cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line, self.current_command_str)
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == DIVIDE_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value / cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line, self.current_command_str)
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == INCREMENT_CELL:
            cell = self.get_cell(self.get_argument(1))
            self.update_value(cell, 1, UpdateMode.ADD)
        
        elif command == DECREMENT_CELL:
            cell = self.get_cell(self.get_argument(1))
            self.update_value(cell, -1, UpdateMode.ADD)
        
        elif command == MODULO_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value % cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line, self.current_command_str)
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == CLEAR_CONSOLE:
            os.system("cls" if sys.platform == "win32" else "clear -r")
        
        elif command == EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            force_update_line = self.execute_condition(cell1.value == cell2.value, next_line)
            self.will_skip_next_line = True
        
        elif command == NOT_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            force_update_line = self.execute_condition(cell1.value != cell2.value, next_line)
            self.will_skip_next_line = True
        
        elif command == GREATER_THAN_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            force_update_line = self.execute_condition(cell1.value > cell2.value, next_line)
            self.will_skip_next_line = True
        
        elif command == LESS_THAN_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            force_update_line = self.execute_condition(cell1.value < cell2.value, next_line)
            self.will_skip_next_line = True
        
        elif command == GREATER_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            force_update_line = self.execute_condition(cell1.value >= cell2.value, next_line)
            self.will_skip_next_line = True

        elif command == LESS_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            force_update_line = self.execute_condition(cell1.value <= cell2.value, next_line)
            self.will_skip_next_line = True
        
        elif command == UPPERCASE_CELL:
            cell = self.get_cell(self.get_argument(1))

            if isinstance(cell, StringCell):
                cell.value = cell.value.upper()
            else:
                self.handle_error("CFTE5", self.current_line, self.current_command_str)
        
        elif command == LOWERCASE_CELL:
            cell = self.get_cell(self.get_argument(1))

            if isinstance(cell, StringCell):
                cell.value = cell.value.lower()
            else:
                self.handle_error("CFTE5", self.current_line, self.current_command_str)
        
        elif command == LENGTH_CELL:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell2, StringCell):
                self.update_value(cell1, len(cell2.value))
            else:
                self.handle_error("CFTE5", self.current_line, self.current_command_str, cell2.name)

        elif command == INVERT_CELL:
            cell = self.get_cell(self.get_argument(1))

            if isinstance(cell, StringCell):
                cell.value = cell.value[::-1]
            else:
                cell.value = -cell.value
        
        elif command == CALL_BLOCK:
            cell = self.get_cell(self.get_argument(1))

            if str(cell.value) in self.blocks:
                self.execution_stack.append(
                    ExecutionFrame(block_name = str(cell.value), is_looping = False, index = 0)
                )
                self.is_executing_new_block = True
            else:
                self.handle_error("CFTE10", name = cell.value)
        
        elif command == ADD_CONSTANT:
            value = self.get_argument(2)
            cell = self.get_cell(self.get_argument(1))

            self.update_value(cell, value, UpdateMode.ADD)
        
        elif command == SWAP_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                cell1.value, cell2.value = cell2.value, cell1.value
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == COPY_CELL:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                cell1.value = cell2.value
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == DELETE_CHAR:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, StringCell) and isinstance(cell2, IntegerCell):
                cell1.value[:cell2.value] + cell1.value[cell2.value+1:]
            else:
                self.handle_error("CFTE4", self.current_line, self.current_command_str)
        
        elif command == STRING_TO_INT:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))
            self.update_value(cell1, cell2.value)
        
        elif command == INT_TO_STRING:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))
            self.update_value(cell1, cell2.value)
        
        elif command == BITWISE_AND:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value & cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line, self.current_command_str)
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == BITWISE_OR:
            result = None
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value | cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line, self.current_command_str)
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == BITWISE_XOR:
            result = None
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value ^ cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line, self.current_command_str)
            else:
                self.handle_error("CFTE7", self.current_line, self.current_command_str)
        
        elif command == BITWISE_NOT:
            cell = self.get_cell(self.get_argument(1))

            if not isinstance(cell, StringCell):
                cell.value = ~cell.value
            else:
                self.handle_error("CFTE6", self.current_line, self.current_command_str)
        
        elif command == SLEEP:
            cell = self.get_cell(self.get_argument(1))

            if not isinstance(cell, StringCell):
                time.sleep(cell.value)
            else:
                self.handle_error("CFTE6", self.current_line, self.current_command_str)
        
        elif command == START_LOOP:
            cell = self.get_cell(self.get_argument(1))

            if str(cell.value) in self.blocks:
                self.execution_stack.append(
                    ExecutionFrame(block_name = str(cell.value), is_looping = True, index = 0)
                )
                self.is_executing_new_block = True
            else:
                self.handle_error("CFTE10", name = cell.value)
        
        elif command == RANDOM_CHAR:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and isinstance(cell1, StringCell):
                cell1.value = random.choice(cell2.value)
            else:
                self.handle_error("CFTE5", self.current_line, self.current_command_str)
        
        elif command == MAX_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = max(cell1.value, cell2.value)
            else:
                self.handle_error("CFTE6", self.current_line, self.current_command_str)
        
        elif command == MIN_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = min(cell1.value, cell2.value)
            else:
                self.handle_error("CFTE6", self.current_line, self.current_command_str)
        
        elif command == GCD_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                v1, v2 = cell1.value, cell2.value
                while v2 != 0:
                    v1, v2 = v2, v1 % v2
                cell1.value = v1
            else:
                self.handle_error("CFTE6", self.current_line, self.current_command_str)
        
        elif command == LCM_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                v1, v2 = cell1.value, cell2.value
                while v2 != 0:
                    v1, v2 = v2, v1 % v2
                cell1.value = abs(cell1.value * cell2.value) // v1
            else:
                self.handle_error("CFTE6", self.current_line, self.current_command_str)
        
        elif command == CREATE_CELL:
            name = self.get_argument(1)
            data_type = self.get_argument(2)

            if not Cell.is_name_correct(name):
                self.handle_error("CFTE2", self.current_line, self.current_command_str, name = name)

            match data_type:
                case CellDataType.INTEGER.value:
                    self.cells.append(IntegerCell(name))
                case CellDataType.FLOAT.value:
                    self.cells.append(FloatCell(name))
                case CellDataType.STRING.value:
                    self.cells.append(StringCell(name))
                case _:
                    self.handle_error("CFTE1", self.current_line, self.current_command_str, data_type = data_type)
        
        elif command == RETURN:
            self.is_return_called = True
        
        else:
            self.handle_error("CFTE3", self.current_line, self.current_command_str, command = command)
        
        if not force_update_line:
            self.current_frame.index += 1

    def parse(self, source: str) -> dict[str, BlockData]:
        lines = source.split('\n')
        blocks: dict[str, BlockData] = {}
        block = None

        for line_number, line in enumerate(lines, 1):
            if line.startswith(START_BLOCK):
                _, _, block_name = line.partition(' ')
                if not block_name.strip():
                    block = None
                    continue
                block = block_name.strip()
                blocks[block] = BlockData()
            elif line.startswith(END_BLOCK):
                block = None
            elif block is not None and line.strip():
                tokens = [match.group(1) if match.group(1) else match.group(0) 
                        for match in re.finditer(r'"([^"]*)"|\S+', line)]
                
                if COMMENT_SYMBOL in tokens:
                    tokens = tokens[:tokens.index(COMMENT_SYMBOL)]
                
                blocks[block].data.append([line_number, tokens])

        return blocks
    
    def get_cell(self, name: str) -> Cell:
        cell = Cell.get_cell(name, self.cells)

        if cell != None:
            return cell
        
        self.handle_error("CFTE8", self.current_line, self.current_command_str, name = name)
    
    def get_argument(self, index: int) -> str:
        if index <= len(self.current_command) - 1:
            return self.current_command[index]
        self.handle_error("CFTE12", self.current_line, self.current_command)
    
    def update_value(self, cell: Cell, value: str, mode: str = UpdateMode.WRITE) -> NoReturn:
        if isinstance(cell, IntegerCell):
            if Cell.is_number(value):
                match mode:
                    case UpdateMode.WRITE:
                        cell.value = int(value)
                    case UpdateMode.ADD:
                        cell.value += int(value)
            else:
                self.handle_error("CFTE9", self.current_line, self.current_command_str, data_type = "int")
        
        elif isinstance(cell, FloatCell):
            if Cell.is_number(value):
                match mode:
                    case UpdateMode.WRITE:
                        cell.value = float(value)
                    case UpdateMode.ADD:
                        cell.value += float(value)
            else:
                self.handle_error("CFTE9", self.current_line, self.current_command_str, data_type = "float")
        
        # else - it's a string 
        else:
            match mode:
                case UpdateMode.WRITE:
                    cell.value = value
                case UpdateMode.ADD:
                    cell.value += value
        
    def execute_condition(self, condition: bool, next_line: list[str]) -> bool:

        if condition and next_line:
            self.interpret_line(next_line, None, True)
        
        return condition and next_line
    
    def handle_error(self, error_number: str, line: int | None = None, command_in_string: str | None = None, **kwargs) -> NoReturn:
        formatted_exception = exception.ERRORS[error_number].format(**kwargs)
        exception.Exception(error_number, formatted_exception, line, command_in_string)
        self.cft_exit()

    def cft_exit(self) -> NoReturn:
        print("\n[Program Finished]")
        sys.exit()