# C42

# На русском
C42 - это язык программирования, который представляет собой эзотерическую разновидность ассемблера, где программы конструируются исключительно из ограниченного набора команд, состоящего из 42 инструкций, пронумерованных от 01 до 42.

## Основные конструкции языка
В языке определены три варианта использования команд (у каждой команды свой вариант написания):
- `COMMAND ARG`
- `COMMAND ARG1 ARG2`
- `COMMAND`

## Типы данных
В языке C42 переменные - это ячейки (подобные регистрам), каждая из которых способна хранить только один из определенных типов данных:
- `INT`
- `STRING`
- `FLOAT`

## Создание ячеек (переменных)
Для создания ячейки используется команда `41`. Пример:
```c42
41 -1 0
```
Первый аргумент — имя переменной (только отрицательное число, начиная с `-1`).
Второй аргумент — тип данных, которое оно сможет хранить:
- `0` - INT
- `1` - STRING
- `2` - FLOAT

## Блоки кода
Код на C42 может быть структурирован в блоки, аналогичные функциям в других языках программирования. Блоки могут иметь любые идентификаторы.

### Объявление блока
- `#1 <имя>` — ключевое слово объявления блока. После `#1` указывается имя блока.
- `#0` — завершение блока.

Блок с идентификатором `main` является точкой входа программы, где размещается основной исполняемый код.

## Пример кода
Программа для вывода любимой фразы программистов:
```c42
#1 main $ Создаем блок с идентификатором main (точка входа)

41 -1 1 $ Создание ячейки -1 с типом STRING
04 -1 "Hello, World!" $ Записываем в ячейку нашу фразу
02 -1 $ Выводим ячейку в консоль

#0 $ Завершаем блок
```

Этот пример иллюстрирует основные элементы синтаксиса и функциональность языка.

# Список Команд
| Код  | Синтаксис            | Описание |
|------|----------------------|----------|
| 01   | 01                             | Завершает выполнение программы. |
| 02   | 02&nbsp;CELL                   | Выводит значение указанной ячейки в консоль. |
| 03   | 03&nbsp;CELL                   | Записывает данные, введенные пользователем, в указанную ячейку. |
| 04   | 04&nbsp;CELL&nbsp;VALUE        | Присваивает указанной ячейке конкретное значение. |
| 05   | 05&nbsp;CELL1&nbsp;CELL2       | Суммирует значения двух указанных ячеек и записывает результат в первую ячейку. |
| 06   | 06&nbsp;CELL1&nbsp;CELL2       | Вычитает значение второй ячейки из первой и записывает результат в первую ячейку. |
| 07   | 07&nbsp;CELL1&nbsp;CELL2       | Умножает значения двух указанных ячеек и записывает результат в первую ячейку. |
| 08   | 08&nbsp;CELL1&nbsp;CELL2       | Делит значение первой ячейки на значение второй и записывает результат в первую ячейку. |
| 09   | 09&nbsp;CELL                   | Увеличивает значение указанной ячейки на 1 (только для чисел типа int/float). |
| 10   | 10&nbsp;CELL                   | Уменьшает значение указанной ячейки на 1 (только для чисел типа int/float). |
| 11   | 11&nbsp;CELL1&nbsp;CELL2       | Записывает в первую ячейку остаток от деления значения первой ячейки на значение второй. |
| 12   | 12                             | Очищает консоль. |
| 13   | 13&nbsp;CELL1&nbsp;CELL2       | Выполняет следующую команду, если значения двух указанных ячеек равны. |
| 14   | 14&nbsp;CELL1&nbsp;CELL2       | Выполняет следующую команду, если значения двух указанных ячеек не равны. |
| 15   | 15&nbsp;CELL1&nbsp;CELL2       | Выполняет следующую команду, если значение первой ячейки больше значения второй. |
| 16   | 16&nbsp;CELL1&nbsp;CELL2       | Выполняет следующую команду, если значение первой ячейки меньше значения второй. |
| 17   | 17&nbsp;CELL1&nbsp;CELL2       | Выполняет следующую команду, если значение первой ячейки больше или равно значению второй. |
| 18   | 18&nbsp;CELL1&nbsp;CELL2       | Выполняет следующую команду, если значение первой ячейки меньше или равно значению второй. |
| 19   | 19&nbsp;CELL                   | Переводит значение указанной ячейки в верхний регистр (если это строка). |
| 20   | 20&nbsp;CELL                   | Переводит значение указанной ячейки в нижний регистр (если это строка). |
| 21   | 21&nbsp;CELL1&nbsp;CELL2       | Возвращает длину строки во второй ячейке и записывает результат в первую ячейку. |
| 22   | 22&nbsp;CELL                   | Инвертирует значение указанной ячейки. |
| 23   | 23&nbsp;CELL                   | Вызывает блок с идентификатором, указанным в ячейке. |
| 24   | 24&nbsp;CELL&nbsp;VALUE        | Увеличивает значение указанной ячейки на константное число или добавляет строку. |
| 25   | 25&nbsp;CELL1&nbsp;CELL2       | Обменивает значения между двумя указанными ячейками. |
| 26   | 26&nbsp;CELL1&nbsp;CELL2       | Копирует значение из второй ячейки в первую. |
| 27   | 27&nbsp;CELL1&nbsp;CELL2       | Удаляет в первой ячейке символ по индексу, указанному во второй ячейке. |
| 28   | 28&nbsp;CELL1&nbsp;CELL2       | Сохраняет в первую ячейку преобразованное число из строки во второй ячейке. |
| 29   | 29&nbsp;CELL1&nbsp;CELL2       | Сохраняет в первую ячейку преобразованную строку из числа во второй ячейке. |
| 30   | 30&nbsp;CELL1&nbsp;CELL2       | Выполняет битовую операцию И и сохраняет результат в первую ячейку (только для int). |
| 31   | 31&nbsp;CELL1&nbsp;CELL2       | Выполняет битовую операцию ИЛИ и сохраняет результат в первую ячейку (только для int). |
| 32   | 32&nbsp;CELL1&nbsp;CELL2       | Выполняет битовую операцию исключающего ИЛИ и сохраняет результат в первую ячейку (только для int). |
| 33   | 33&nbsp;CELL                   | Выполняет битовую операцию НЕ и сохраняет результат в указанную ячейку (только для int). |
| 34   | 34&nbsp;CELL                   | Останавливает выполнение программы на время, указанное в ячейке. |
| 35   | 35&nbsp;CELL                   | Начинает цикл, код которого будет блок, указанный в ячейке. |
| 36   | 36&nbsp;CELL1&nbsp;CELL2       | Выбирает случайный символ из CELL2 и сохраняет его в CELL1. |
| 37   | 37&nbsp;CELL1&nbsp;CELL2       | Ищет максимальное значение из двух указанных ячеек и сохраняет его в первую ячейку. |
| 38   | 38&nbsp;CELL1&nbsp;CELL2       | Ищет минимальное значение из двух указанных ячеек и сохраняет его в первую ячейку. |
| 39   | 39&nbsp;CELL1&nbsp;CELL2       | Вычисляет НОД двух чисел и сохраняет результат в первую ячейку. |
| 40   | 40&nbsp;CELL1&nbsp;CELL2       | Вычисляет НОК двух чисел и сохраняет результат в первую ячейку. |
| 41   | 41&nbsp;NAME&nbsp;DATATYPE     | Создание новой ячейки. |
| 42   | 42                             | Принудительное завершение блока или цикла. |

# In English

C42 is a programming language that represents an esoteric variant of assembly, where programs are constructed exclusively from a limited set of commands consisting of 42 instructions numbered from 01 to 42.

## Basic Language Constructs
The language defines three variants of command usage (each command has its own syntax):
- `COMMAND ARG`
- `COMMAND ARG1 ARG2`
- `COMMAND`

## Data Types
In the C42 language, variables are cells (similar to registers), each capable of storing only one of the specified data types:
- `INT`
- `STRING`
- `FLOAT`

## Creating Cells (Variables)
To create a cell, use command `41`. Example:
```c42
41 -1 0
```
The first argument is the variable name (only negative numbers, starting from `-1`).
The second argument is the data type it can store:
- `0` - INT
- `1` - STRING
- `2` - FLOAT

## Code Blocks
Code in C42 can be structured into blocks, analogous to functions in other programming languages. Blocks can have any identifiers.

### Block Declaration
- `#1 <name>` — block declaration keyword. After `#1`, specify the block name.
- `#0` — block termination.

The block with identifier `main` is the program entry point where the main executable code is placed.

## Code Example
A program to output programmers' favorite phrase:
```c42
#1 main $ Create a block with identifier main (entry point)

41 -1 1 $ Create cell -1 with type STRING
04 -1 "Hello, World!" $ Write our phrase to the cell
02 -1 $ Output the cell to console

#0 $ End the block
```

This example illustrates the basic syntax elements and functionality of the language.

# Command List
| Code | Syntax                         | Description |
|------|--------------------------------|-------------|
| 01   | 01                             | Terminates program execution. |
| 02   | 02&nbsp;CELL                   | Outputs the value of the specified cell to the console. |
| 03   | 03&nbsp;CELL                   | Writes user-entered data to the specified cell. |
| 04   | 04&nbsp;CELL&nbsp;VALUE        | Assigns a specific value to the specified cell. |
| 05   | 05&nbsp;CELL1&nbsp;CELL2       | Sums the values of two specified cells and writes the result to the first cell. |
| 06   | 06&nbsp;CELL1&nbsp;CELL2       | Subtracts the value of the second cell from the first and writes the result to the first cell. |
| 07   | 07&nbsp;CELL1&nbsp;CELL2       | Multiplies the values of two specified cells and writes the result to the first cell. |
| 08   | 08&nbsp;CELL1&nbsp;CELL2       | Divides the value of the first cell by the value of the second and writes the result to the first cell. |
| 09   | 09&nbsp;CELL                   | Increments the value of the specified cell by 1 (int/float only). |
| 10   | 10&nbsp;CELL                   | Decrements the value of the specified cell by 1 (int/float only). |
| 11   | 11&nbsp;CELL1&nbsp;CELL2       | Writes to the first cell the remainder of dividing the first cell's value by the second cell's value. |
| 12   | 12                             | Clears the console. |
| 13   | 13&nbsp;CELL1&nbsp;CELL2       | Executes the next command if the values of the two specified cells are equal. |
| 14   | 14&nbsp;CELL1&nbsp;CELL2       | Executes the next command if the values of the two specified cells are not equal. |
| 15   | 15&nbsp;CELL1&nbsp;CELL2       | Executes the next command if the value of the first cell is greater than the value of the second. |
| 16   | 16&nbsp;CELL1&nbsp;CELL2       | Executes the next command if the value of the first cell is less than the value of the second. |
| 17   | 17&nbsp;CELL1&nbsp;CELL2       | Executes the next command if the value of the first cell is greater than or equal to the value of the second. |
| 18   | 18&nbsp;CELL1&nbsp;CELL2       | Executes the next command if the value of the first cell is less than or equal to the value of the second. |
| 19   | 19&nbsp;CELL                   | Converts the value of the specified cell to uppercase (if it's a string). |
| 20   | 20&nbsp;CELL                   | Converts the value of the specified cell to lowercase (if it's a string). |
| 21   | 21&nbsp;CELL1&nbsp;CELL2       | Returns the string length in the second cell and writes the result to the first cell. |
| 22   | 22&nbsp;CELL                   | Inverts the value of the specified cell. |
| 23   | 23&nbsp;CELL                   | Calls the block with the identifier specified in the cell. |
| 24   | 24&nbsp;CELL&nbsp;VALUE        | Increments the value of the specified cell by a constant number or appends a string. |
| 25   | 25&nbsp;CELL1&nbsp;CELL2       | Swaps values between two specified cells. |
| 26   | 26&nbsp;CELL1&nbsp;CELL2       | Copies the value from the second cell to the first. |
| 27   | 27&nbsp;CELL1&nbsp;CELL2       | Deletes the character in the first cell at the index specified in the second cell. |
| 28   | 28&nbsp;CELL1&nbsp;CELL2       | Saves to the first cell the converted number from the string in the second cell. |
| 29   | 29&nbsp;CELL1&nbsp;CELL2       | Saves to the first cell the converted string from the number in the second cell. |
| 30   | 30&nbsp;CELL1&nbsp;CELL2       | Performs bitwise AND operation and saves the result to the first cell (int only). |
| 31   | 31&nbsp;CELL1&nbsp;CELL2       | Performs bitwise OR operation and saves the result to the first cell (int only). |
| 32   | 32&nbsp;CELL1&nbsp;CELL2       | Performs bitwise XOR operation and saves the result to the first cell (int only). |
| 33   | 33&nbsp;CELL                   | Performs bitwise NOT operation and saves the result to the specified cell (int only). |
| 34   | 34&nbsp;CELL                   | Pauses program execution for the time specified in the cell. |
| 35   | 35&nbsp;CELL                   | Starts a loop whose code will be the block specified in the cell. |
| 36   | 36&nbsp;CELL1&nbsp;CELL2       | Selects a random character from CELL2 and saves it to CELL1. |
| 37   | 37&nbsp;CELL1&nbsp;CELL2       | Finds the maximum value from two specified cells and saves it to the first cell. |
| 38   | 38&nbsp;CELL1&nbsp;CELL2       | Finds the minimum value from two specified cells and saves it to the first cell. |
| 39   | 39&nbsp;CELL1&nbsp;CELL2       | Calculates the GCD of two numbers and saves the result to the first cell. |
| 40   | 40&nbsp;CELL1&nbsp;CELL2       | Calculates the LCM of two numbers and saves the result to the first cell. |
| 41   | 41&nbsp;NAME&nbsp;DATATYPE     | Creates a new cell. |
| 42   | 42                             | Forces termination of a block or loop. |