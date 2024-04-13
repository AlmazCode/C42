import sys

class Error:
    def __init__(self, message, line, command):
        print()
        if command != None:
            print(f"> {command}")
        print(f"Ошибка : на строке {line} : {message}")
        sys.exit(1)

class BlockNotFound(Error):
    def __init__(self, name):
        super().__init__(f"Не удалось найти блок под номером {name}", None, None)

class IncorrectValue(Error):
    def __init__(self, line, command, trueType):
        super().__init__(f"Некорректное значение, ячейка может хранить только {trueType}", line, command)

class CellNotFound(Error):
    def __init__(self, line, command, name):
        super().__init__(f"Не удалось найти ячейку под номером {name}", line, command)

class DifferentTypes(Error):
    def __init__(self, line, command):
        super().__init__(f"У ячеек разные типы данных", line, command)

class NoString(Error):
    def __init__(self, line, command):
        super().__init__(f"В данной команде нельзя использовать ячейку с типом string", line, command)

class TypeIsNotString(Error):
    def __init__(self, line, command):
        super().__init__(f"Тип ячейки должен быть string", line, command)

class StringAndInt(Error):
    def __init__(self, line, command):
        super().__init__(f"У первой ячейки должен быть тип string, а у второй int", line, command)

class InvalidSyntax(Error):
    def __init__(self, line, command):
        super().__init__(f"Не корректный синтаксис", line, command)

class IncorrectCellName(Error):
    def __init__(self, line, command, name):
        super().__init__(f"Имя {name} для ячейки не корректное! имя должно быть отрицательным числом от -1", line, command)

class IncorrectDataType(Error):
    def __init__(self, line, command, name):
        super().__init__(f"Тип {name} для ячейки не корректное! Тип данных должен быть одним из: 0 - int, 1 - string, 2 - float", line, command)