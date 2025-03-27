from typing import NoReturn, Union

import re


class Cell:
    def __init__(self, name: str, default: int | float | str) -> NoReturn:
        self.name = name
        self.value = default
    
    @staticmethod
    def get_cell(name: str, cells: list['Cell']) -> Union['Cell', None]:
        return next((cell for cell in cells if cell.name == name), None)

    @staticmethod
    def is_number(s: str | int | float) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_name_correct(name: str) -> bool:
        return bool(re.match(r"^-[1-9][0-9]*$", name))

class IntegerCell(Cell):
    def __init__(self, name: str) -> NoReturn:
        super().__init__(name, 0)

class FloatCell(Cell):
    def __init__(self, name: str) -> NoReturn:
        super().__init__(name, 0.0)

class StringCell(Cell):
    def __init__(self, name: str) -> NoReturn:
        super().__init__(name, "")