__author__ = "AlmazCode"
__vertion__ = "1.1o"

import click
from interpreter import Interpreter

@click.command()
@click.argument("filename", default="src/Examples/testing conditions.cft", required=False, type=click.Path(exists=True, readable=True))
def run(filename):
    """C42 Interpretator"""

    with open(filename, "r", encoding="utf-8") as file:
        code = file.read()

    C42 = Interpreter(code)
    C42.interpret()

if __name__ == "__main__":
    run()