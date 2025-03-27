import re, os, sys, time, random
import exception

from typing import NoReturn

from constants import *
from cfttypes import *

from cell import *


class Interpreter:
    def __init__(self, source: str):

        self.cells: list[Cell]                      = []
        self.current_line_number: int               = 0
        self.current_command_in_string: str         = ""
        self.current_command: list[str]             = None 
        self.will_skip_next_line                    = False
        self.execution_stack: list[ExecutionFrame] = []
        self.is_return_called: bool                 = False

        self.blocks = self.parse(source)
    
    def interpret(self, block_name: str | None = None):

        if block_name is None:
            block_name = ENTER_FUNCTION

        if block_name not in self.blocks:
            if block_name == ENTER_FUNCTION:
                self.handle_error("CFTE11")
            else:
                self.handle_error("CFTE10", name = block_name)
        
        self.execution_stack.append(
            ExecutionFrame(block_name = block_name, is_looping = False, line_number = 0)
        )

        while self.execution_stack:

            frame = self.execution_stack.pop()
            block = self.blocks[frame.block_name]

            while frame.line_number < len(block):
                self.current_line_number, self.current_command = block[frame.line_number]
                self.current_command_in_string = " ".join(self.current_command)

                if self.will_skip_next_line:
                    self.will_skip_next_line = False
                    frame.line_number += 1
                    continue

                next_command = block[frame.line_number + 1] if frame.line_number + 1 < len(block) else None
                force_exit = self.interpret_line(self.current_command, next_command)

                frame.line_number += 1

                if self.is_return_called or force_exit:
                    break

            if frame.is_looping and not self.is_return_called:
                self.execution_stack.append(
                    ExecutionFrame(block_name = frame.block_name, is_looping = frame.is_looping, line_number = 0)
                )
                self.is_return_called = False
            elif force_exit and frame.line_number < len(block):
                self.execution_stack.append(
                    ExecutionFrame(block_name = frame.block_name, is_looping = frame.is_looping,
                                   line_number = frame.line_number)
                )
                self.execution_stack[-1], self.execution_stack[-2] = self.execution_stack[-2], self.execution_stack[-1]
    
    def interpret_line(self, line, next_line):
        command = line[0]

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
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == SUBTRACT_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value - cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
            else:
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == MULTIPLY_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value * cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
            else:
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == DIVIDE_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value / cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
            else:
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
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
                    self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
            else:
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == CLEAR_CONSOLE:
            os.system("cls" if sys.platform == "win32" else "clear -r")
        
        elif command == EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if cell1.value == cell2.value and next_line:
                # Выполняем следующую строку сразу и сигнализируем главному циклу пропустить её
                self.current_line_number = next_line[0]
                self.current_command_in_string = " ".join(next_line[1])
                self.current_command = next_line[1]
                self.interpret_line(next_line[1], None)

            self.will_skip_next_line = True
        
        elif command == NOT_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if cell1.value != cell2.value and next_line:
                self.current_line_number = next_line[0]
                self.current_command_in_string = " ".join(next_line[1])
                self.current_command = next_line[1]
                self.interpret_line(next_line[1], None)

            self.will_skip_next_line = True
        
        elif command == GREATER_THAN_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if cell1.value > cell2.value and next_line:
                self.current_line_number = next_line[0]
                self.current_command_in_string = " ".join(next_line[1])
                self.current_command = next_line[1]
                self.interpret_line(next_line[1], None)

            self.will_skip_next_line = True
        
        elif command == LESS_THAN_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if cell1.value < cell2.value and next_line:
                self.current_line_number = next_line[0]
                self.current_command_in_string = " ".join(next_line[1])
                self.current_command = next_line[1]
                self.interpret_line(next_line[1], None)

            self.will_skip_next_line = True
        
        elif command == GREATER_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if cell1.value >= cell2.value and next_line:
                self.current_line_number = next_line[0]
                self.current_command_in_string = " ".join(next_line[1])
                self.current_command = next_line[1]
                self.interpret_line(next_line[1], None)

            self.will_skip_next_line = True

        elif command == LESS_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if cell1.value <= cell2.value and next_line:
                self.current_line_number = next_line[0]
                self.current_command_in_string = " ".join(next_line[1])
                self.current_command = next_line[1]
                self.interpret_line(next_line[1], None)

            self.will_skip_next_line = True
        
        elif command == UPPERCASE_CELL:
            cell = self.get_cell(self.get_argument(1))

            if isinstance(cell, StringCell):
                cell.value = cell.value.upper()
            else:
                self.handle_error("CFTE5", self.current_line_number, self.current_command_in_string)
        
        elif command == LOWERCASE_CELL:
            cell = self.get_cell(self.get_argument(1))

            if isinstance(cell, StringCell):
                cell.value = cell.value.lower()
            else:
                self.handle_error("CFTE5", self.current_line_number, self.current_command_in_string)
        
        elif command == LENGTH_CELL:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell2, StringCell):
                self.update_value(cell1, len(cell2.value))
            else:
                self.handle_error("CFTE5", self.current_line_number, self.current_command_in_string, cell2.name)

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
                    ExecutionFrame(block_name = str(cell.value), is_looping = False, line_number = 0)
                )
                return True
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
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == COPY_CELL:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                cell1.value = cell2.value
            else:
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == DELETE_CHAR:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, StringCell) and isinstance(cell2, IntegerCell):
                cell1.value[:cell2.value] + cell1.value[cell2.value+1:]
            else:
                self.handle_error("CFTE4", self.current_line_number, self.current_command_in_string)
        
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
                    self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
            else:
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == BITWISE_OR:
            result = None
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value | cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
            else:
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == BITWISE_XOR:
            result = None
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value ^ cell2.value
                    self.update_value(cell1, result)
                else:
                    self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
            else:
                self.handle_error("CFTE7", self.current_line_number, self.current_command_in_string)
        
        elif command == BITWISE_NOT:
            cell = self.get_cell(self.get_argument(1))

            if not isinstance(cell, StringCell):
                cell.value = ~cell.value
            else:
                self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
        
        elif command == SLEEP:
            cell = self.get_cell(self.get_argument(1))

            if not isinstance(cell, StringCell):
                time.sleep(cell.value)
            else:
                self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
        
        elif command == START_LOOP:
            cell = self.get_cell(self.get_argument(1))

            if str(cell.value) in self.blocks:
                self.execution_stack.append(
                    ExecutionFrame(block_name = str(cell.value), is_looping = True, line_number = 0)
                )
                return True
            else:
                self.handle_error("CFTE10", name = cell.value)
        
        elif command == RANDOM_CHAR:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and isinstance(cell1, StringCell):
                cell1.value = random.choice(cell2.value)
            else:
                self.handle_error("CFTE5", self.current_line_number, self.current_command_in_string)
        
        elif command == MAX_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = max(cell1.value, cell2.value)
            else:
                self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
        
        elif command == MIN_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = min(cell1.value, cell2.value)
            else:
                self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
        
        elif command == GCD_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                v1, v2 = cell1.value, cell2.value
                while v2 != 0:
                    v1, v2 = v2, v1 % v2
                cell1.value = v1
            else:
                self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
        
        elif command == LCM_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                v1, v2 = cell1.value, cell2.value
                while v2 != 0:
                    v1, v2 = v2, v1 % v2
                cell1.value = abs(cell1.value * cell2.value) // v1
            else:
                self.handle_error("CFTE6", self.current_line_number, self.current_command_in_string)
        
        elif command == CREATE_CELL:
            name = self.get_argument(1)
            data_type = self.get_argument(2)

            if not Cell.is_name_correct(name):
                self.handle_error("CFTE2", self.current_line_number, self.current_command_in_string, name = name)

            match data_type:
                case CellDataType.INTEGER:
                    self.cells.append(IntegerCell(name))
                case CellDataType.FLOAT:
                    self.cells.append(FloatCell(name))
                case CellDataType.STRING:
                    self.cells.append(StringCell(name))
                case _:
                    self.handle_error("CFTE1", self.current_line_number, self.current_command_in_string, data_type = data_type)
        
        elif command == RETURN:
            self.is_return_called = True
        
        else:
            self.handle_error("CFTE3", self.current_line_number, self.current_command_in_string, command = command)

    def parse(self, source: str) -> dict[str, list[list[int | list[str]]]]:
        lines = source.split('\n')
        blocks: dict[str, list[list[int | list[str]]]] = {}
        block = None

        for line_number, line in enumerate(lines, 1):
            if line.startswith(START_BLOCK):
                _, _, block_name = line.partition(' ')
                if not block_name.strip():
                    block = None
                    continue
                block = block_name.strip()
                blocks[block] = []
            elif line.startswith(END_BLOCK):
                block = None
            elif block is not None and line.strip():
                tokens = [match.group(1) if match.group(1) else match.group(0) 
                        for match in re.finditer(r'"([^"]*)"|\S+', line)]
                
                if COMMENT_SYMBOL in tokens:
                    tokens = tokens[:tokens.index(COMMENT_SYMBOL)]
                
                blocks[block].append((line_number, tokens))

        return blocks
    
    def get_cell(self, name: str) -> Cell:
        cell = Cell.get_cell(name, self.cells)

        if cell != None:
            return cell
        
        self.handle_error("CFTE8", self.current_line_number, self.current_command_in_string, name = name)
    
    def get_argument(self, index: int) -> str:
        if index <= len(self.current_command) - 1:
            return self.current_command[index]
        self.handle_error("CFTE12", self.current_line_number, self.current_command)
    
    def update_value(self, cell: Cell, value: str, mode: UpdateMode = UpdateMode.WRITE) -> NoReturn:
        if isinstance(cell, IntegerCell):
            if Cell.is_number(value):
                match mode:
                    case UpdateMode.WRITE:
                        cell.value = int(value)
                    case UpdateMode.ADD:
                        cell.value += int(value)
            else:
                self.handle_error("CFTE9", self.current_line_number, self.current_command_in_string, data_type = "int")
        
        elif isinstance(cell, FloatCell):
            if Cell.is_number(value):
                match mode:
                    case UpdateMode.WRITE:
                        cell.value = float(value)
                    case UpdateMode.ADD:
                        cell.value += float(value)
            else:
                self.handle_error("CFTE9", self.current_line_number, self.current_command_in_string, data_type = "float")
        
        # else - it's a string 
        else:
            match mode:
                case UpdateMode.WRITE:
                    cell.value = value
                case UpdateMode.ADD:
                    cell.value += value
    
    def handle_error(self, error_number: str, line: int | None = None, command_in_string: str | None = None, **kwargs) -> NoReturn:
        formatted_exception = exception.ERRORS[error_number].format(**kwargs)
        exception.Exception(error_number, formatted_exception, line, command_in_string)
        self.cft_exit()

    def cft_exit(self) -> NoReturn:
        print("\n[Program Finished]")
        sys.exit()