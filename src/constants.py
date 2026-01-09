# all constants of C42

EXIT                = "01" # Program termination.
PRINT               = "02" # Output cell value.
INPUT               = "03" # Write user data to cell.
ASSIGN_VALUE        = "04" # Assign value to cell.
SUM_CELLS           = "05" # Sum values of two cells and write result to CELL1.
SUBTRACT_CELLS      = "06" # Subtract CELL2 value from CELL1 and write result to CELL1.
MULTIPLY_CELLS      = "07" # Multiply values of two cells and write result to CELL1.
DIVIDE_CELLS        = "08" # Divide CELL2 value by CELL1 and write result to CELL1.
INCREMENT_CELL      = "09" # Increment cell value by 1 (int/float only).
DECREMENT_CELL      = "10" # Decrement cell value by 1 (int/float only).
MODULO_CELLS        = "11" # Write to CELL1 the remainder of dividing CELL1 by CELL2.
CLEAR_CONSOLE       = "12" # Clear console.
EQUAL_CELLS         = "13" # Execute command below if cell values are equal.
NOT_EQUAL_CELLS     = "14" # Execute command below if cell values are not equal.
GREATER_THAN_CELLS  = "15" # Execute command below if CELL1 value is greater than CELL2.
LESS_THAN_CELLS     = "16" # Execute command below if CELL1 value is less than CELL2.
GREATER_EQUAL_CELLS = "17" # Execute command below if CELL1 value is greater than or equal to CELL2.
LESS_EQUAL_CELLS    = "18" # Execute command below if CELL1 value is less than or equal to CELL2.
UPPERCASE_CELL      = "19" # Convert cell value to uppercase (string only).
LOWERCASE_CELL      = "20" # Convert cell value to lowercase (string only).
LENGTH_CELL         = "21" # Return string length of CELL2 and write result to CELL1.
INVERT_CELL         = "22" # Invert cell value (if cell is int or float, changes sign; if string, reverses string).
CALL_BLOCK          = "23" # Call block with identifier specified in cell.
ADD_CONSTANT        = "24" # Increment cell value by constant number if cell is int/float, otherwise append string.
SWAP_CELLS          = "25" # Swap values between CELL1 and CELL2.
COPY_CELL           = "26" # Copy value from CELL2 to CELL1.
DELETE_CHAR         = "27" # Delete character in CELL1 at index specified in CELL2.
STRING_TO_INT       = "28" # Save to CELL1 the converted number from string CELL2.
INT_TO_STRING       = "29" # Save to CELL1 the converted string from number CELL2.
BITWISE_AND         = "30" # Perform bitwise AND between CELL1 and CELL2 values and save result to CELL1 (int only).
BITWISE_OR          = "31" # Perform bitwise OR between CELL1 and CELL2 values and save result to CELL1 (int only).
BITWISE_XOR         = "32" # Perform bitwise XOR between CELL1 and CELL2 values and save result to CELL1 (int only).
BITWISE_NOT         = "33" # Perform bitwise NOT on cell value and save result to CELL (int only).
SLEEP               = "34" # Pause program execution for duration specified in VALUE.
START_LOOP          = "35" # Start loop with code block specified in CELL.
RANDOM_CHAR         = "36" # Select random character from VALUE and save to CELL.
MAX_CELLS           = "37" # Find maximum value from two cells and save to CELL1.
MIN_CELLS           = "38" # Find minimum value from two cells and save to CELL1.
GCD_CELLS           = "39" # Calculate GCD (greatest common divisor) of two numbers and save result to CELL1.
LCM_CELLS           = "40" # Calculate LCM (least common multiple) of two numbers and save result to CELL1.
CREATE_CELL         = "41" # Create new cell.
RETURN              = "42" # Return from block.


START_BLOCK     = "#1"      # start of the block
END_BLOCK       = "#0"      # end of the block
ENTER_BLOCK     = "main"    # enter block of program
COMMENT_SYMBOL  = '$'       # the symbol to start a comment line

FILE_EXTENSIONS = [
    "c42",
    "cft",
    "C42",
    "CFT"
]