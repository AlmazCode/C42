from colorama import Fore
from typing import NoReturn

class Exception:
    def __init__(
            self,
            error_number: str,
            message: str,
            line: int | None = None,
            command_in_string: str | None = None) -> NoReturn:

        if command_in_string is not None:
            print(f"\n\n  -> {command_in_string}")
        if line is not None:
            print(f"{Fore.CYAN}[{line}] {Fore.RESET}{error_number} : {Fore.RED}{message}{Fore.RESET}")
        else:
            print(f"{error_number} : {Fore.RED}{message}{Fore.RESET}")


ERRORS: dict[str, str] = {
    # INVALID SYNTAX
    "CFTE12": "Недопустимый синтаксис",

    # ENTER FUNCTION NOT FOUND
    "CFTE11": "Не удалось найти точку входа",
    
    # BLOCK NOT FOUND
    "CFTE10": "Не удалось найти блок под именем `{name}`",
    
    # INCCORECT VALUE
    "CFTE9": "Некорректное значение для типа `{data_type}`",
    
    # CELL NOT FOUND
    "CFTE8": "Не удалось найти ячейку под именем `{name}`",
    
    # CELLS HAVE DIFFERENT TYPES
    "CFTE7": "Ячейки имеют разные типы данных",
    
    # NO STRING
    "CFTE6": "В данной команде нельзя использовать ячейку с типом `string`",
    
    # CELL'S TYPE HAVE TO BE A STRING
    "CFTE5": "Тип ячейки должен быть `string`",

    # STRING AND INT
    "CFTE4": "У первой ячейки должен быть тип `string`, а у второй `int`",
    
    # UNDEFINED COMMAND
    "CFTE3": "Не существующая команда `{command}`",

    # INCCORECT CELL NAME
    "CFTE2": "Некорректное имя ячейки `{name}`. Может быть только отрицательным числом от -1",
    
    # UNDEFINED DATA TYPE
    "CFTE1": "Не существует такого типа данных как `{data_type}`"
}