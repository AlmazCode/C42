"""
Author: AlmazCode
Version: 1.0.2.42
"""

from interpreter import Interpreter


code: str = ""

with open("code.cft", "r", encoding = "utf-8") as file:
    code = file.read()

C42 = Interpreter(code)
C42.Interpret()