__author__ = "AlmazCode"
__vertion__ = "1.1.5"


import click

from pathlib import Path
from interpreter import Interpreter
from constants import FILE_EXTENSIONS


@click.command()
@click.argument("filename", required=False, type=click.Path(exists=True, readable=True))
def run(filename):
    """C42 Interpretator"""

    file_suffix = Path(filename).suffix[1:]
    if file_suffix not in FILE_EXTENSIONS:
        raise NameError(f"Incorrect file extension! Must be one of the following: {', '.join(FILE_EXTENSIONS)}")

    with open(filename, "r", encoding="utf-8") as file:
        code = file.read()

    C42 = Interpreter(code)
    C42.interpret()

if __name__ == "__main__":
    run()