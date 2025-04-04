import re


class Cell:
    def __init__(self, default: int | float | str) -> None:
        self.value = default

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
    def __init__(self) -> None:
        super().__init__(0)

class FloatCell(Cell):
    def __init__(self) -> None:
        super().__init__(0.0)

class StringCell(Cell):
    def __init__(self) -> None:
        super().__init__("")