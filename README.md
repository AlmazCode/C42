# C42
C42 - это язык программирования, который представляет собой эзотерическую разновидность ассемблера, где программы конструируются исключительно из ограниченного набора команд, состоящего из 42 инструкций, пронумерованных от 01 до 42.

В языке определены три варианта использования команд:
- COMMAND ARG
- COMMAND ARG ARG
- COMMAND

Существует 15 "ячеек" (подобных регистрам), пронумерованных от -1 до -15, каждая из которых способна хранить определенный тип данных:

INT:
-1, -2, -3, -4, -5

STRING:
-6, -7, -8, -9, -10

FLOAT:
-11, -12, -13, -14, -15

Код на этом языке может быть структурирован в блоки, аналогичные функциям в других языках программирования. Блоки могут иметь идентификаторы только в виде числовых значений и используются для организации логики программы. Блок с идентификатором 1 является точкой входа, где размещается основной исполняемый код программы.

Пример использования языка:

```
#01000010 1 $ Определение блока с идентификатором 1

04 -2 98 $ Присвоение ячейке -2 значения 98
02 -2 $ Вывод содержимого ячейки -2 в консоль

13 -1 -3 $ Если содержимое ячейки -2 равно содержимому ячейки -3 (по умолчанию они обе равны 0), то выполнить следующую команду, в противном случае - пропустить
23 2 $ Переход к блоку с идентификатором 2

#01000101 $ Завершение блока

#01000010 2

04 -5 "This is Block 2" $ Присвоение ячейке -5 значения "This is Block 2"
04 -9 3.14 $ Еще одно присвоение ячейке -9 значения 3.14

$ Вывод содержимого ячеек
02 -5
02 -9

#01000101
```

Представленный выше пример иллюстрирует основные элементы синтаксиса и функциональность языка.

# Список Команд
- **01** - Завершает выполнение программы.
- **02 CELL** - Выводит значение указанной ячейки в консоль.
- **03 CELL** - Записывает данные, введенные пользователем, в указанную ячейку.
- **04 CELL VALUE** - Присваивает указанной ячейке конкретное значение.
- **05 CELL1 CELL2** - Суммирует значения двух указанных ячеек и записывает результат в первую ячейку.
- **06 CELL1 CELL2** - Вычитает значение второй ячейки из первой и записывает результат в первую ячейку.
- **07 CELL1 CELL2** - Умножает значения двух указанных ячеек и записывает результат в первую ячейку.
- **08 CELL1 CELL2** - Делит значение первой ячейки на значение второй и записывает результат в первую ячейку.
- **09 CELL** - Увеличивает значение указанной ячейки на 1 (только для чисел типа int/float).
- **10 CELL** - Уменьшает значение указанной ячейки на 1 (только для чисел типа int/float).
- **11 CELL1 CELL2** - Записывает в первую ячейку остаток от деления значения первой ячейки на значение второй.
- **12** - Очищает консоль.
- **13 CELL1 CELL2** - Выполняет следующую команду, если значения двух указанных ячеек равны.
- **14 CELL1 CELL2** - Выполняет следующую команду, если значения двух указанных ячеек не равны.
- **15 CELL1 CELL2** - Выполняет следующую команду, если значение первой ячейки больше значения второй.
- **16 CELL1 CELL2** - Выполняет следующую команду, если значение первой ячейки меньше значения второй.
- **17 CELL1 CELL2** - Выполняет следующую команду, если значение первой ячейки больше или равно значению второй.
- **18 CELL1 CELL2** - Выполняет следующую команду, если значение первой ячейки меньше или равно значению второй.
- **19 CELL** - Переводит значение указанной ячейки в верхний регистр (если это строка).
- **20 CELL** - Переводит значение указанной ячейки в нижний регистр (если это строка).
- **21 CELL1 CELL2** - Возвращает длину строки во второй ячейке и записывает результат в первую ячейку.
- **22 CELL** - Инвертирует значение указанной ячейки (если ячейка типа int или float, то меняет знак; если string, то инвертирует строку).
- **23 CELL** - Вызывает блок с идентификатором, указанным в ячейке.
- **24 CELL VALUE** - Увеличивает значение указанной ячейки на константное число, если ячейка типа int/float, иначе добавляет строку.
- **25 CELL1 CELL2** - Обменивает значения между двумя указанными ячейками.
- **26 CELL1 CELL2** - Копирует значение из второй ячейки в первую.
- **27 CELL1 CELL2** - Удаляет в первой ячейке символ по индексу, указанному во второй ячейке.
- **28 CELL1 CELL2** - Сохраняет в первую ячейку преобразованное число из строки во второй ячейке.
- **29 CELL1 CELL2** - Сохраняет в первую ячейку преобразованную строку из числа во второй ячейке.
- **30 CELL1 CELL2** - Выполняет битовую операцию И между значениями двух указанных ячеек и сохраняет результат в первую ячейку (только для int).
- **31 CELL1 CELL2** - Выполняет битовую операцию ИЛИ между значениями двух указанных ячеек и сохраняет результат в первую ячейку (только для int).
- **32 CELL1 CELL2** - Выполняет битовую операцию исключающего ИЛИ между значениями двух указанных ячеек и сохраняет результат в первую ячейку (только для int).
- **33 CELL** - Выполняет битовую операцию НЕ для значения в указанной ячейке и сохраняет результат в эту же ячейку (только для int).
- **34 CELL** - Останавливает выполнение программы на время, указанное в в ячейке.
- **35 CELL** - Начинает цикл, код которого будет блок, указанный в ячейке.
- **36 CELL VALUE** - Выбирает случайный символ из VALUE и сохраняет его в указанную ячейку.
- **37 CELL1 CELL2** - Ищет максимальное значение из двух указанных ячеек и сохраняет его в первую ячейку.
- **38 CELL1 CELL2** - Ищет минимальное значение из двух указанных ячеек и сохраняет его в первую ячейку.
- **39 CELL1 CELL2** - Вычисляет НОД (наибольший общий делитель) двух чисел и сохраняет результат в первую ячейку.
- **40 CELL1 CELL2** - Вычисляет НОК (наименьшее общее кратное) двух чисел и сохраняет результат в первую ячейку.
- **41** - Очищает значения всех ячеек.
- **42** - Возвращает из блока или цикла (return).
