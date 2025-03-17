import re

class Cell:
    def __init__(self, name: str, default: int | float | str) -> None:

        # cell = Cell.GetCellByName(name)
        # if cell != None:
        #     Cell.CELLS.remove(cell)
        # Cell.CELLS.append(self)

        self.name = name
        self.value = default
    
    @staticmethod
    def get_cell(name: str, cells: list['Cell']) -> 'Cell':
        return next((cell for cell in cells if cell.name == name), None)

    # @staticmethod
    # def isFloat(s):
    #     try: 
    #         float(s)
    #         return True
    #     except:
    #         return False

    @staticmethod
    def is_number(s: str | int) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_name_correct(name: str):
        return bool(re.match(r"^-[1-9][0-9]*$", name))
    
    # @staticmethod
    # def isCorrectDataType(char: str):
    #     return char in ["0", "1", "2"]

class IntegerCell(Cell):
    def __init__(self, name: str) -> None:
        super().__init__(name, 0)

class FloatCell(Cell):
    def __init__(self, name: str) -> None:
        super().__init__(name, 0.0)

class StringCell(Cell):
    def __init__(self, name: str) -> None:
        super().__init__(name, "")