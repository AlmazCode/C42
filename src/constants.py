# all constants of C42

EXIT                = "01" # Завершение программы.
PRINT               = "02" # Вывод ячейки.
INPUT               = "03" # Запись пользовательских данных в ячейку.
ASSIGN_VALUE        = "04" # Присвоение значения ячейке.
SUM_CELLS           = "05" # Суммирование значений двух ячеек и запись результата в CELL1.
SUBTRACT_CELLS      = "06" # Вычитание значения CELL2 из CELL1 и запись результата в CELL1.
MULTIPLY_CELLS      = "07" # Умножение значений двух ячеек и запись результата в CELL1.
DIVIDE_CELLS        = "08" # Деление значения CELL2 на CELL1 и запись результата в CELL1.
INCREMENT_CELL      = "09" # Увеличение значения ячейки на 1 (только для int/float).
DECREMENT_CELL      = "10" # Уменьшение значения ячейки на 1 (только для int/float).
MODULO_CELLS        = "11" # Запись в CELL1 остатка от деления CELL1 на CELL2.
CLEAR_CONSOLE       = "12" # Очистка консоли.
EQUAL_CELLS         = "13" # Выполнение команды ниже, если значения ячеек равны.
NOT_EQUAL_CELLS     = "14" # Выполнение команды ниже, если значения ячеек не равны.
GREATER_THAN_CELLS  = "15" # Выполнение команды ниже, если значение ячейки CELL1 больше значения CELL2.
LESS_THAN_CELLS     = "16" # Выполнение команды ниже, если значение ячейки CELL1 меньше значения CELL2.
GREATER_EQUAL_CELLS = "17" # Выполнение команды ниже, если значение ячейки CELL1 больше или равно значению CELL2.
LESS_EQUAL_CELLS    = "18" # Выполнение команды ниже, если значение ячейки CELL1 меньше или равно значению CELL2.
UPPERCASE_CELL      = "19" # Перевод значения ячейки в верхний регистр (только для string).
LOWERCASE_CELL      = "20" # Перевод значения ячейки в нижний регистр (только для string).
LENGTH_CELL         = "21" # Возвращение длины строки CELL2 и запись результата в CELL1.
INVERT_CELL         = "22" # Инвертирование значения ячейки (если ячейка типа int или float, то меняет знак; если string, то инвертирует строку).
CALL_BLOCK          = "23" # Вызов блока с указанным идентификатором в ячейке.
ADD_CONSTANT        = "24" # Увеличение значения ячейки на константное число, если ячейка типа int/float, иначе добавление строки.
SWAP_CELLS          = "25" # Обмен значениями между CELL1 и CELL2.
COPY_CELL           = "26" # Копирование значения из CELL2 в CELL1.
DELETE_CHAR         = "27" # Удаление в CELL1 символа по индексу, указанному в CELL2.
STRING_TO_INT       = "28" # Сохранение в CELL1 преобразованного числа из строки CELL2.
INT_TO_STRING       = "29" # Сохранение в CELL1 преобразованной строки из числа CELL2.
BITWISE_AND         = "30" # Выполнение битового И между значениями CELL1 и CELL2 и сохранение результата в CELL1 (только для int).
BITWISE_OR          = "31" # Выполнение битового ИЛИ между значениями CELL1 и CELL2 и сохранение результата в CELL1 (только для int).
BITWISE_XOR         = "32" # Выполнение битового исключающего ИЛИ между значениями CELL1 и CELL2 и сохранение результата в CELL1 (только для int).
BITWISE_NOT         = "33" # Выполнение битового НЕ для значения в ячейке и сохранение результата в CELL (только для int).
SLEEP               = "34" # Остановка выполнения программы на значение, указанное в VALUE.
START_LOOP          = "35" # Начать цикл, код которого будет блок, указанный в CELL
RANDOM_CHAR         = "36" # Выбор случайного символа из VALUE и сохранение его в CELL.
MAX_CELLS           = "37" # Поиск максимального значения из двух ячеек и сохранение его в CELL1.
MIN_CELLS           = "38" # Поиск минимального значения из двух ячеек и сохранение его в CELL1.
GCD_CELLS           = "39" # Вычисление НОД (наибольшего общего делителя) двух чисел и сохранение результата в CELL1.
LCM_CELLS           = "40" # Вычисление НОК (наименьшего общего кратного) двух чисел и сохранение результата в CELL1.
CREATE_CELL         = "41" # Создание новой ячейки
RETURN              = "42" # Возвращение из блока.


START_BLOCK     = "#1"      # start of the block
END_BLOCK       = "#0"      # end of the block
ENTER_BLOCK     = "main"    # enter block of program
COMMENT_SYMBOL  = '$'       # the symbol to start a comment line