"""
Author: AlmazCode
Version: 1.1o
"""

from interpreter import Interpreter
from json import dumps

code: str = ""

with open("code.cft", "r", encoding = "utf-8") as file:
    code = file.read()

C42 = Interpreter(code)
#print(dumps(C42.blocks, indent = 2, ensure_ascii = False))
C42.interpret()