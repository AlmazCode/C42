import re, os, sys, time, random

from constants import *
from exception import *

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
    
    def interpret(self, block_id: str = "1"):
        if block_id not in self.blocks:
            raise BlockNotFound(block_id)
        
        self.execution_stack.append(
            ExecutionFrame(block_name = block_id, is_looping = False, line_index = 0)
        )

        while self.execution_stack:

            frame = self.execution_stack.pop()
            block = self.blocks[frame.block_name]

            while frame.line_index < len(block):
                self.current_line_number, self.current_command = block[frame.line_index]
                self.current_command_in_string = " ".join(self.current_command)

                if self.will_skip_next_line:
                    self.will_skip_next_line = False
                    frame.line_index += 1
                    continue

                next_command = block[frame.line_index + 1] if frame.line_index + 1 < len(block) else None
                force_exit = self.interpret_line(self.current_command, next_command)

                frame.line_index += 1

                if self.is_return_called or force_exit:
                    break

            if frame.is_looping and not self.is_return_called:
                self.execution_stack.append(
                    ExecutionFrame(block_name = frame.block_name, is_looping = frame.is_looping, line_index = 0)
                )
                self.is_return_called = False
            elif force_exit and frame.line_index < len(block):
                self.execution_stack.append(
                    ExecutionFrame(block_name = frame.block_name, is_looping = frame.is_looping,
                                   line_index = frame.line_index)
                )
                self.execution_stack[-1], self.execution_stack[-2] = self.execution_stack[-2], self.execution_stack[-1]
    
    def interpret_line(self, line, next_line):
        command = line[0]

        if command == EXIT:
            exit(1)
        
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
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
        elif command == SUBTRACT_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value - cell2.value
                    self.update_value(cell1, result)
                else:
                    NoString(self.current_line_number, self.current_command_in_string)
            else:
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
        elif command == MULTIPLY_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value * cell2.value
                    self.update_value(cell1, result)
                else:
                    NoString(self.current_line_number, self.current_command_in_string)
            else:
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
        elif command == DIVIDE_CELLS:
            cell1: Cell = self.get_cell(self.get_argument(1))
            cell2: Cell = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value / cell2.value
                    self.update_value(cell1, result)
                else:
                    NoString(self.current_line_number, self.current_command_in_string)
            else:
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
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
                    NoString(self.current_line_number, self.current_command_in_string)
            else:
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
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
            #else:
            self.will_skip_next_line = True
        
        elif command == NOT_EQUAL_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if cell1.value != cell2.value and next_line:
                self.current_line_number = next_line[0]
                self.current_command_in_string = " ".join(next_line[1])
                self.current_command = next_line[1]
                self.interpret_line(next_line[1], None)
            #else:
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
                TypeIsNotString(self.current_line_number, self.current_command_in_string)
        
        elif command == LOWERCASE_CELL:
            cell = self.get_cell(self.get_argument(1))

            if isinstance(cell, StringCell):
                cell.value = cell.value.lower()
            else:
                TypeIsNotString(self.current_line_number, self.current_command_in_string)
        
        elif command == LENGTH_CELL:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell2, StringCell):
                self.update_value(cell1, len(cell2.value))
            else:
                TypeIsNotString(self.current_line_number, self.current_command_in_string, cell2.name)

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
                    ExecutionFrame(block_name = str(cell.value), is_looping = False, line_index = 0)
                )
                return True
            else:
                BlockNotFound(cell.value)
        
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
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
        elif command == COPY_CELL:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                cell1.value = cell2.value
            else:
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
        elif command == DELETE_CHAR:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, StringCell) and isinstance(cell2, IntegerCell):
                cell1.value[:cell2.value] + cell1.value[cell2.value+1:]
            else:
                StringAndInt(self.current_line_number, self.current_command_in_string)
        
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
                    NoString(self.current_line_number, self.current_command_in_string)
            else:
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
        elif command == BITWISE_OR:
            result = None
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value | cell2.value
                    self.update_value(cell1, result)
                else:
                    NoString(self.current_line_number, self.current_command_in_string)
            else:
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
        elif command == BITWISE_XOR:
            result = None
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)):
                if not isinstance(cell1, StringCell):
                    result = cell1.value ^ cell2.value
                    self.update_value(cell1, result)
                else:
                    NoString(self.current_line_number, self.current_command_in_string)
            else:
                DifferentTypes(self.current_line_number, self.current_command_in_string)
        
        elif command == BITWISE_NOT:
            cell = self.get_cell(self.get_argument(1))

            if not isinstance(cell, StringCell):
                cell.value = ~cell.value
            else:
                NoString(self.current_line_number, self.current_command_in_string)
        
        elif command == SLEEP:
            cell = self.get_cell(self.get_argument(1))

            if not isinstance(cell, StringCell):
                time.sleep(cell.value)
            else:
                NoString(self.current_line_number, self.current_command_in_string)
        
        elif command == START_LOOP:
            cell = self.get_cell(self.get_argument(1))

            if str(cell.value) in self.blocks:
                self.execution_stack.append(
                    ExecutionFrame(block_name = str(cell.value), is_looping = True, line_index = 0)
                )
                return True
            else:
                BlockNotFound(cell.value)
        
        elif command == RANDOM_CHAR:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and isinstance(cell1, StringCell):
                cell1.value = random.choice(cell2.value)
            else:
                TypeIsNotString(self.current_line_number, self.current_command_in_string)
        
        elif command == MAX_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = max(cell1.value, cell2.value)
            else:
                NoString(self.current_line_number, self.current_command_in_string)
        
        elif command == MIN_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                cell1.value = min(cell1.value, cell2.value)
            else:
                NoString(self.current_line_number, self.current_command_in_string)
        
        elif command == GCD_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                v1, v2 = cell1.value, cell2.value
                while v2 != 0:
                    v1, v2 = v2, v1 % v2
                cell1.value = v1
            else:
                NoString(self.current_line_number, self.current_command_in_string)
        
        elif command == LCM_CELLS:
            cell1 = self.get_cell(self.get_argument(1))
            cell2 = self.get_cell(self.get_argument(2))

            if isinstance(cell1, type(cell2)) and not isinstance(cell1, StringCell):
                v1, v2 = cell1.value, cell2.value
                while v2 != 0:
                    v1, v2 = v2, v1 % v2
                cell1.value = abs(cell1.value * cell2.value) // v1
            else:
                NoString(self.current_line_number, self.current_command_in_string)
        
        elif command == CREATE_CELL:
            name = self.get_argument(1)
            data_type = self.get_argument(2)

            if not Cell.is_name_correct(name):
                IncorrectCellName(self.current_line_number, self.current_command_in_string, name)

            match data_type:
                case CellDataType.INTEGER:
                    self.cells.append(IntegerCell(name))
                case CellDataType.FLOAT:
                    self.cells.append(FloatCell(name))
                case CellDataType.STRING:
                    self.cells.append(StringCell(name))
                case _:
                    IncorrectDataType(self.current_line_number, self.current_command_in_string, data_type)
        
        elif command == RETURN:
            self.is_return_called = True
        
        else:
            InvalidSyntax(self.current_line_number, self.current_command_in_string)

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
                
                if '$' in tokens:
                    tokens = tokens[:tokens.index('$')]
                
                blocks[block].append((line_number, tokens))

        return blocks
    
    def get_cell(self, name: str) -> Cell:
        cell = Cell.get_cell(name, self.cells)

        if cell != None:
            return cell
        
        CellNotFound(self.current_line_number, self.current_command_in_string, name)
    
    def get_argument(self, index: int) -> str:
        if index <= len(self.current_command) - 1:
            return self.current_command[index]
        InvalidSyntax(self.current_line_number, self.current_command)
    
    # def get_arguments(self, *indexes: list[int]) -> str:
    #     arguments: list[]
        
    #     for index in indexes:
    #         if index <= len(self.current_command) - 1:
    #             return self.current_command[index]
    #         else:
    #             InvalidSyntax(self.current_line_index, self.current_command)
    
    def update_value(self, cell: Cell, value: str, mode: UpdateMode = UpdateMode.WRITE) -> bool:
        if isinstance(cell, IntegerCell):
            if Cell.is_number(value):
                match mode:
                    case UpdateMode.WRITE:
                        cell.value = int(value)
                    case UpdateMode.ADD:
                        cell.value += int(value)
            else:
                IncorrectValue(self.current_line_number, self.current_command_in_string, "int")
        
        elif isinstance(cell, FloatCell):
            if Cell.is_number(value):
                match mode:
                    case UpdateMode.WRITE:
                        cell.value = float(value)
                    case UpdateMode.ADD:
                        cell.value += float(value)
            else:
                IncorrectValue(self.current_line_number, self.current_command_in_string, "float")
        
        # else - it's a string 
        else:
            match mode:
                case UpdateMode.WRITE:
                    cell.value = value
                case UpdateMode.ADD:
                    cell.value += value