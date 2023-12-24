"""
This module contains constants and utility functions for formatting terminal text.
"""

TERM_RESET = '\u001b[0m'

TERM_BOLD = ('\u001b[1m', '\u001b[22m')
TERM_FAINT = ('\u001b[2m', '\u001b[22m')
TERM_ITALIC = ('\u001b[3m', '\u001b[23m')
TERM_UNDERLINE = ('\u001b[4m', '\u001b[24m')
TERM_BLINK = ('\u001b[5m', '\u001b[25m')
TERM_INVERSE = ('\u001b[7m', '\u001b[27m')
TERM_HIDDEN = ('\u001b[8m', '\u001b[28m')
TERM_STRIKE = ('\u001b[9m', '\u001b[29m')

TERM_FG_DEFAULT = '\u001b[39m'
TERM_FG_BLACK = ('\u001b[30m', TERM_FG_DEFAULT)
TERM_FG_RED = ('\u001b[31m', TERM_FG_DEFAULT)
TERM_FG_GREEN = ('\u001b[32m', TERM_FG_DEFAULT)
TERM_FG_YELLOW = ('\u001b[33m', TERM_FG_DEFAULT)
TERM_FG_BLUE = ('\u001b[34m', TERM_FG_DEFAULT)
TERM_FG_MAGENTA = ('\u001b[35m', TERM_FG_DEFAULT)
TERM_FG_CYAN = ('\u001b[36m', TERM_FG_DEFAULT)
TERM_FG_WHITE = ('\u001b[37m', TERM_FG_DEFAULT)

TERM_BG_DEFAULT = '\u001b[49m'
TERM_BG_BLACK = ('\u001b[40m', TERM_BG_DEFAULT)
TERM_BG_RED = ('\u001b[41m', TERM_BG_DEFAULT)
TERM_BG_GREEN = ('\u001b[42m', TERM_BG_DEFAULT)
TERM_BG_YELLOW = ('\u001b[43m', TERM_BG_DEFAULT)
TERM_BG_BLUE = ('\u001b[44m', TERM_BG_DEFAULT)
TERM_BG_MAGENTA = ('\u001b[45m', TERM_BG_DEFAULT)
TERM_BG_CYAN = ('\u001b[46m', TERM_BG_DEFAULT)
TERM_BG_WHITE = ('\u001b[47m', TERM_BG_DEFAULT)

def throw_error(msg: str):
    """
    Prints an error message in red color and pauses the program execution.

    Args:
        msg (str): The error message to be displayed.
    """
    print(
        term_format(
            term_format(
                f'\nERROR! {msg}\n',
                TERM_FG_RED
            ),
            TERM_BOLD
        )
    )
    pause()


def pause():
    """
    Pauses the program and waits for user input to continue.
    """
    input(term_format('Press any key to continue...\n', TERM_BOLD))


def clear():
    """
    Clears the terminal screen.
    """
    print('\u001b[2J')


def term_format(text: str, format: tuple[str, str] | list[tuple[str, str]]) -> str:
    """
    Formats the given text with the specified formatting.

    Args:
        text (str): The text to be formatted.
        format (tuple[str, str] | list[tuple[str, str]]): The formatting to be applied. 
            It can be a tuple of start and end formatting strings, or a list of multiple 
            start and end formatting tuples.

    Returns:
        str: The formatted text.
    """
    if isinstance(format, tuple):
        return f'{format[0]}{text}{format[1]}'

    format_str, unformat_str = str(), str()
    for (start, end) in format:
        format_str += start
        unformat_str = end + unformat_str
    
    return f'{format_str}{text}{unformat_str}'


def finput(prompt: str, format: tuple[str, str]) -> str:
    """
    Prompt the user for input and return the input as a string.

    Args:
        prompt (str): The prompt to display to the user.
        format (tuple[str, str]): A tuple containing the formatting to display the user's input with.

    Returns:
        str: The user input as a string.
    """
    in_str = input(f'{prompt}{format[0]}')
    print(format[1], end='')
    return in_str


def quit_app():
    """
    Quit the application.

    This function prints a goodbye message and raises a SystemExit exception to terminate the program.
    """
    print('\nQuitting application... Goodbye!')
    raise SystemExit(0)
