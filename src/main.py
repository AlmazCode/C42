from interpreter import Interpreter

import sys


def main(filename: str):
    with open(filename, "r", encoding = "utf-8") as file:
        code = file.read()
    
    C42 = Interpreter(code)
    C42.interpret()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        filename = r"src\Test\code.cft"
        main(filename)