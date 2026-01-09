from colorama import Fore

class Exception:
    def __init__(
            self,
            error_number: str,
            message: str,
            line: int | None = None,
            command_in_string: str | None = None) -> None:

        if command_in_string is not None:
            print(f"\n\n  -> {command_in_string}")
        if line is not None:
            print(f"{Fore.CYAN}[{line}] {Fore.RESET}{error_number} : {Fore.RED}{message}{Fore.RESET}")
        else:
            print(f"{error_number} : {Fore.RED}{message}{Fore.RESET}")


ERRORS: dict[str, str] = {
    # INVALID SYNTAX
    "CFTE12": "Invalid syntax",

    # ENTER FUNCTION NOT FOUND
    "CFTE11": "Failed to find entry point",
    
    # BLOCK NOT FOUND
    "CFTE10": "Failed to find block with name `{name}`",
    
    # INCORRECT VALUE
    "CFTE9": "Incorrect value for type `{data_type}`",
    
    # CELL NOT FOUND
    "CFTE8": "Failed to find cell with name `{name}`",
    
    # CELLS HAVE DIFFERENT TYPES
    "CFTE7": "Cells have different data types",
    
    # NO STRING
    "CFTE6": "Cannot use cell with type `string` in this command",
    
    # CELL'S TYPE HAVE TO BE A STRING
    "CFTE5": "Cell type must be `string`",

    # STRING AND INT
    "CFTE4": "First cell must have type `string`, and second cell must have type `int`",
    
    # UNDEFINED COMMAND
    "CFTE3": "Non-existent command `{command}`",

    # INCORRECT CELL NAME
    "CFTE2": "Incorrect cell name `{name}`. Can only be a negative number starting from -1",
    
    # UNDEFINED DATA TYPE
    "CFTE1": "Data type `{data_type}` does not exist"
}