import re
import sys
import os
import platform
import time
import random

from constants import *
from typing import Union
from exception import (
    BlockNotFound,
    IncorrectValue,
    CellNotFound,
    DifferentTypes,
    TypeIsNotString,
    StringAndInt,
    NoString,
    InvalidSyntax
)

usingOS = platform.system()

class Cell:

    CELLS: list['Cell'] = []

    def __init__(self, name, defaultValue: int | float | str, valueType: str):

        Cell.CELLS.append(self)

        self.name = name
        self.defaultValue = defaultValue
        self.value = defaultValue
        self.valueType = valueType
    
    @staticmethod
    def GetCellByName(name: str) -> 'Cell':
        return next((cell for cell in Cell.CELLS if cell.name == name), None)

    @staticmethod
    def isFloat(s):
        try: 
            float(s)
            return True
        except:
            return False

    @staticmethod
    def isInt(s):
        try: 
            int(s)
            return True
        except:
            return False

    @staticmethod
    def isString(s):
        return s[0] == "\"" and s[-1] == "\""

class Interpreter:
    def __init__(self, code: str):

        self.cells: list[Cell] = [
            Cell("-1", 0, INT),
            Cell("-2", 0, INT),
            Cell("-3", 0, INT),
            Cell("-4", 0, INT),
            Cell("-5", "", INT),
            Cell("-6", "", STRING),
            Cell("-7", "", STRING),
            Cell("-8", "", STRING),
            Cell("-9", 0, STRING),
            Cell("-10", 0, STRING),
            Cell("-11", 0, FLOAT),
            Cell("-12", 0, FLOAT),
            Cell("-13", 0, FLOAT),
            Cell("-14", 0, FLOAT),
            Cell("-15", 0, FLOAT)
        ]

        self.code = code
        self.blocks: dict[list[list[str]]] = {}
        self.currentLine = 0
        self.currentCommand = ""
        self.skipNextCommand = False
        self.executionStack = []
        self.returnCalled = False
        self.loopCalled = False

        self.Parse()
    
    def Interpret(self, blockId: str = "1"):
        if blockId not in self.blocks:
            BlockNotFound(blockId)
        
        self.executionStack.append([blockId, False])
        idx = {block: -1 for block in self.blocks}

        while self.executionStack:
            currentBlock = self.executionStack.pop()
            commands = self.blocks[currentBlock[0]]
            blockName = currentBlock[0]
            blockIsLoop = currentBlock[1]

            while 1:
                idx[blockName] += 1 if not idx[blockName] + 1 > len(commands) - 1 else 0
                self.currentLine = commands[idx[blockName]][0]
                self.currentCommand = " ".join(commands[idx[blockName]][1])

                if self.skipNextCommand:
                    self.skipNextCommand = False
                    continue

                nextCommand = None if idx[blockName] + 1 > len(commands) - 1 else commands[idx[blockName] + 1]
                forceExit = self.ExecuteCommand(commands[idx[blockName]][1], nextCommand)

                if self.returnCalled:
                    break
                elif forceExit:
                    break
                elif idx[blockName] >= len(commands) - 1:
                    idx[blockName] = -1
                    break

            if not self.returnCalled and blockIsLoop:
                self.executionStack.append(currentBlock)
                self.returnCalled = False
            elif forceExit and not idx[blockName] >= len(commands) - 1:
                self.executionStack.append(currentBlock)
                self.executionStack[-1], self.executionStack[-2] = self.executionStack[-2], self.executionStack[-1]

    def ExecuteCommand(self, command, nextCommand):
        CMD = command[0]

        if CMD == EXIT:
            sys.exit(1)
        
        elif CMD == PRINT:
            cell = self.GetCell(self.GetArgument(1, command))
            print(str(cell.value).replace("\\n", "\n"), end = "", flush = True)
    
        elif CMD == INPUT:
            cell = self.GetCell(self.GetArgument(1, command))
            value = input()
            self.ChangeValue(cell, value, True)

        elif CMD == ASSIGN_VALUE:
            value = self.GetArgument(2, command)
            cell = self.GetCell(self.GetArgument(1, command))
            self.ChangeValue(cell, value)
        
        elif CMD == SUM_CELLS:
            result = None
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                result = cell1.value + cell2.value
            else:
                DifferentTypes(self.currentLine, self.currentCommand)

            self.ChangeValue(cell1, result, True)
        
        elif CMD == SUBTRACT_CELLS:
            result = None
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                if cell1.valueType != STRING:
                    result = cell1.value - cell2.value
                else:
                    NoString(self.currentLine, self.currentCommand)
            else:
                DifferentTypes(self.currentLine, self.currentCommand)

            self.ChangeValue(cell1, result)
        
        elif CMD == MULTIPLY_CELLS:
            result = None
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                if cell1.valueType != STRING:
                    result = cell1.value * cell2.value
                else:
                    NoString(self.currentLine, self.currentCommand)
            else:
                DifferentTypes(self.currentLine, self.currentCommand)

            self.ChangeValue(cell1, result)
        
        elif CMD == DIVIDE_CELLS:
            result = None
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                if cell1.valueType != STRING:
                    result = cell1.value / cell2.value if cell1.valueType == FLOAT else cell1.value // cell2.value
                else:
                    NoString(self.currentLine, self.currentCommand)
            else:
                DifferentTypes(self.currentLine, self.currentCommand)

            self.ChangeValue(cell1, result)
        
        elif CMD == INCREMENT_CELL:
            result = None
            cell = self.GetCell(self.GetArgument(1, command))
            self.ChangeValue(cell, 1, mode = "add")
        
        elif CMD == DECREMENT_CELL:
            result = None
            cell = self.GetCell(self.GetArgument(1, command))
            self.ChangeValue(cell, -1, mode = "add")
        
        elif CMD == MODULO_CELLS:
            result = None
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                if cell1.valueType != STRING:
                    result = cell1.value % cell2.value
                else:
                    NoString(self.currentLine, self.currentCommand)
            else:
                DifferentTypes(self.currentLine, self.currentCommand)
        
        elif CMD == CLEAR_CONSOLE:
            if usingOS == "Windows":
                os.system("cls")
            elif usingOS == "Linux":
                os.system("clear -r")
        
        elif CMD == EQUAL_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.value == cell2.value and nextCommand:
                self.currentLine = nextCommand[0]
                self.currentCommand = " ".join(nextCommand[1])
                self.ExecuteCommand(nextCommand[1], None)
            else:
                self.skipNextCommand = True
        
        elif CMD == NOT_EQUAL_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.value != cell2.value and nextCommand:
                self.currentLine = nextCommand[0]
                self.currentCommand = " ".join(nextCommand[1])
                self.ExecuteCommand(nextCommand[1], None)
            else:
                self.skipNextCommand = True
        
        elif CMD == GREATER_THAN_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.value > cell2.value and nextCommand:
                self.currentLine = nextCommand[0]
                self.currentCommand = " ".join(nextCommand[1])
                self.ExecuteCommand(nextCommand[1], None)
            else:
                self.skipNextCommand = True
        
        elif CMD == LESS_THAN_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.value < cell2.value and nextCommand:
                self.currentLine = nextCommand[0]
                self.currentCommand = " ".join(nextCommand[1])
                self.ExecuteCommand(nextCommand[1], None)
            else:
                self.skipNextCommand = True
        
        elif CMD == GREATER_EQUAL_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.value >= cell2.value and nextCommand:
                self.currentLine = nextCommand[0]
                self.currentCommand = " ".join(nextCommand[1])
                self.ExecuteCommand(nextCommand[1], None)
            else:
                self.skipNextCommand = True

        elif CMD == LESS_EQUAL_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.value <= cell2.value and nextCommand:
                self.currentLine = nextCommand[0]
                self.currentCommand = " ".join(nextCommand[1])
                self.ExecuteCommand(nextCommand[1], None)
            else:
                self.skipNextCommand = True
        
        elif CMD == UPPERCASE_CELL:
            cell = self.GetCell(self.GetArgument(1, command))

            if cell.valueType == STRING:
                cell.value = cell.value.upper()
            else:
                TypeIsNotString(self.currentLine, self.currentCommand)
        
        elif CMD == LOWERCASE_CELL:
            cell = self.GetCell(self.GetArgument(1, command))

            if cell.valueType == STRING:
                cell.value = cell.value.lower()
            else:
                TypeIsNotString(self.currentLine, self.currentCommand)
        
        elif CMD == LENGTH_CELL:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell2.valueType == STRING:
                self.ChangeValue(cell1, len(cell2.value))
            else:
                TypeIsNotString(self.currentLine, self.currentCommand, cell2.name)

        elif CMD == INVERT_CELL:
            cell = self.GetCell(self.GetArgument(1, command))

            if cell.valueType == STRING:
                cell.value = cell.value[::-1]
            else:
                cell.value = -cell.value
        
        elif CMD == CALL_BLOCK:
            cell = self.GetCell(self.GetArgument(1, command))

            if str(cell.value) in self.blocks:
                self.executionStack.append([str(cell.value), False])
                return True
            else:
                BlockNotFound(cell.value)
        
        elif CMD == ADD_CONSTANT:
            value = self.GetArgument(2, command)
            cell = self.GetCell(self.GetArgument(1, command))

            self.ChangeValue(cell, value, mode = "add")
        
        elif CMD == SWAP_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                cell1.value, cell2.value = cell2.value, cell1.value
            else:
                DifferentTypes(self.currentLine, self.currentCommand)
        
        elif CMD == COPY_CELL:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                cell1.value = cell2.value
            else:
                DifferentTypes(self.currentLine, self.currentCommand)
        
        elif CMD == DELETE_CHAR:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == STRING and cell2.valueType == INT:
                cell1.value[:cell2.value] + cell1.value[cell2.value+1:]
            else:
                StringAndInt(self.currentLine, self.currentCommand)
        
        elif CMD == STRING_TO_INT:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            self.ChangeValue(cell1, cell2.value)
        
        elif CMD == INT_TO_STRING:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))
            self.ChangeValue(cell1, cell2.value, True)
        
        elif CMD == BITWISE_AND:
            result = None
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                if cell1.valueType != STRING:
                    result = cell1.value & cell2.value
                else:
                    NoString(self.currentLine, self.currentCommand)
            else:
                DifferentTypes(self.currentLine, self.currentCommand)

            self.ChangeValue(cell1, result)
        
        elif CMD == BITWISE_OR:
            result = None
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                if cell1.valueType != STRING:
                    result = cell1.value | cell2.value
                else:
                    NoString(self.currentLine, self.currentCommand)
            else:
                DifferentTypes(self.currentLine, self.currentCommand)

            self.ChangeValue(cell1, result)
        
        elif CMD == BITWISE_XOR:
            result = None
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType:
                if cell1.valueType != STRING:
                    result = cell1.value ^ cell2.value
                else:
                    NoString(self.currentLine, self.currentCommand)
            else:
                DifferentTypes(self.currentLine, self.currentCommand)

            self.ChangeValue(cell1, result)
        
        elif CMD == BITWISE_NOT:
            cell = self.GetCell(self.GetArgument(1, command))

            if cell.valueType != STRING:
                cell.value = ~cell.value
            else:
                NoString(self.currentLine, self.currentCommand)
        
        elif CMD == SLEEP:
            cell = self.GetCell(self.GetArgument(1, command))

            if cell.valueType != STRING:
                time.sleep(cell.value)
            else:
                NoString(self.currentLine, self.currentCommand)
        
        elif CMD == START_LOOP:
            cell = self.GetCell(self.GetArgument(1, command))

            if str(cell.value) in self.blocks:
                self.executionStack.append([str(cell.value), True])
                return True
            else:
                BlockNotFound(cell.value)
        
        elif CMD == RANDOM_CHAR:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType and cell1.valueType == STRING:
                cell1.value = random.choice(cell2.value)
            else:
                TypeIsNotString(self.currentLine, self.currentCommand)
        
        elif CMD == MAX_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType and cell1.value != STRING:
                cell1.value = max(cell1.value, cell2.value)
            else:
                NoString(self.currentLine, self.currentCommand)
        
        elif CMD == MIN_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType and cell1.value != STRING:
                cell1.value = min(cell1.value, cell2.value)
            else:
                NoString(self.currentLine, self.currentCommand)
        
        elif CMD == GCD_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType and cell1.value != STRING:
                v1, v2 = cell1.value, cell2.value
                while v2 != 0:
                    v1, v2 = v2, v1 % v2
                cell1.value = v1
            else:
                NoString(self.currentLine, self.currentCommand)
        
        elif CMD == LCM_CELLS:
            cell1 = self.GetCell(self.GetArgument(1, command))
            cell2 = self.GetCell(self.GetArgument(2, command))

            if cell1.valueType == cell2.valueType and cell1.value != STRING:
                v1, v2 = cell1.value, cell2.value
                while v2 != 0:
                    v1, v2 = v2, v1 % v2
                cell1.value = abs(cell1.value * cell2.value) // v1
            else:
                NoString(self.currentLine, self.currentCommand)
        
        elif CMD == CLEAR_CELLS:
            for cell in self.cells:
                cell.value = cell.defaultValue
        
        elif CMD == RETURN:
            self.returnCalled = True
        
        else:
            InvalidSyntax(self.currentLine, self.currentCommand)

    def Parse(self):
        lines = self.code.split('\n')
        result = {}
        block = None
        line_number = 1

        for line in lines:
            if line.startswith(START_BLOCK):
                if block != None:
                    del result[block]
                if len(line.split()) <= 1 or len(line.split()) > 2:
                    block = None
                    continue
                block = line.split()[1]
                result[block] = []
            elif line.startswith(END_BLOCK):
                block = None
            elif block is not None and line.strip():
                parsed_line = (line_number, re.findall(r'(?:"[^"]*"|[^"\s]+)', line))
                if '$' in parsed_line[1]:
                    parsed_line = (parsed_line[0], parsed_line[1][:parsed_line[1].index('$')])
                if parsed_line[1]:
                    result[block].append(parsed_line)

            line_number += 1

        self.blocks = result
    
    def GetCell(self, name: str) -> Cell:
        cell = Cell.GetCellByName(name)

        if cell != None:
            return cell
        CellNotFound(self.currentLine, self.currentCommand, name)
    
    def GetArgument(self, index: int, command: list[str]) -> str:
        if index <= len(command) - 1:
            return command[index]
        InvalidSyntax(self.currentLine, self.currentCommand)
    
    def ChangeValue(self, cell: Cell, value: str, fromInput = False, mode = "set") -> bool:

        if value != str:
            value = str(value)

        if cell.valueType == INT:
            if Cell.isInt(value):
                if mode == "set":
                    cell.value = int(value)
                elif mode == "add":
                    cell.value += int(value)
            else:
                IncorrectValue(self.currentLine, self.currentCommand, "int")
        
        elif cell.valueType == FLOAT:
            if Cell.isFloat(value):
                if mode == "set":
                    cell.value = float(value)
                elif mode == "add":
                    cell.value += float(value)
            else:
                IncorrectValue(self.currentLine, self.currentCommand, "float")
            
        elif cell.valueType == STRING:
            if Cell.isString(value) or fromInput:
                if mode == "set":
                    cell.value = value[1:-1] if not fromInput else value
                elif mode == "add":
                    cell.value += value[1:-1]
            else:
                IncorrectValue(self.currentLine, self.currentCommand, "string")