# C42
C42 - это язык программирования, который представляет собой эзотерическую разновидность ассемблера, где программы конструируются исключительно из ограниченного набора команд, состоящего из 42 инструкций, пронумерованных от 01 до 42.

В языке определены три варианта использования команд (у каждой команды свой вариант написания):
- COMMAND ARG
- COMMAND ARG ARG
- COMMAND

В данном языке переменные - это ячейки (подобные регистрам), каждая из которых способна хранить только один из определенных типов данных:
- INT
- STRING
- FLOAT

Для создания ячейки используется команда 41, пример:
```
41 -1 0
```
Первым аргументом мы указываем имя переменной, которое может быть только отрицательным числом начиная с -1.
А вторым указываем тип данных, которое оно сможет хранить: 0 - INT, 1 - STRING, 2 - FLOAT.

Код на этом языке может быть структурирован в блоки, аналогичные функциям в других языках программирования. Блоки могут иметь идентификаторы только в виде числовых значений и используются для организации логики программы. Блок с идентификатором 1 является точкой входа, где размещается основной исполняемый код программы.

Пример использования языка для вывода любимой фразы программистов:

```
#1 1 $ Создаем блок с индефикатором 1 (точка входа)

41 -1 1 $ Создание ячейки -1 с типом STRING
04 -1 "Hello, World!" $ Записываем в ячейку нашу фразу
02 -1 $ Выводим ячейку в консоль

#0
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
- **41 NAME DATATYPE** - Создание новой ячейки.
- **42** - Принудительное завершение блока или цикла.
