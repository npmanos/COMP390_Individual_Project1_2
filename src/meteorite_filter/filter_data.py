#!/usr/bin/env python3
"""
This module is an interactive terminal application to a meteorite data file.

The user must provide a correctly formatted data file. They will then have
the option to filter based on mass or year and can choose to output the
filtered data to the terminal or save it to a text or xls file.
"""


from meteorite_filter.constants import *
from meteorite_filter.dsv.reader import DSVDictReader
from meteorite_filter.tui.menu import Menu, MenuItem, ReturnableMenuItem
from meteorite_filter.tui.utils import *


def main():
    """
    Main function that filters meteorite data based on user input.
    """
    clear()
    print(WELCOME_MESSAGE + '\n')

    reader = get_reader()

    data = list(reader)

    filter_menus = Menu([ReturnableMenuItem(
            prop['menu_desc'], lambda desc=prop['input_desc']: filter_range_input(desc),
            lambda range, data=data, field=option: select_output(filter_data(data, field, *range), field)
        ) for option, prop in FILTER_OPTIONS.items()], 'Which field would you like to use to filter the data?')

    filter_menus()


def input_file_path() -> str:
    """
    Prompts the user to enter the filename, including its file extension and path if necessary.
    If the user enters ">q" or ">Q", the application will exit.
    
    Returns:
        str: The entered file name.
    """
    print(term_format('To begin, please type the filename, including its file extension and path if\nnecessary (ex: "file.txt"). To exit the application, type ">q" or ">Q"',
          TERM_FG_CYAN))  # '?' and '>' are not valid filename characters in Windows and is used in case a user has a file named 'q'. This remains an issue on Linux and macOS
    file_name = finput('> ', TERM_FG_GREEN)

    if file_name in ('?q', '?Q', '>q', '>Q'):
        quit_app()

    return file_name


def select_open_mode() -> str:
    """
    Prompts the user to select an open mode for the file.

    Returns:
        str: The selected open mode.
    """
    open_mode = ''

    def set_open_mode(mode: str):
        nonlocal open_mode
        open_mode += mode

    open_mode_menu = Menu({mode['param']: MenuItem(
        label=mode['desc'], func_call=lambda m=mode['param']: m, callback=set_open_mode) for mode in OPEN_MODES},
        preamble='What mode would you like to use to open the file?',
        default=0, quit_label='>q')

    open_mode_menu()
    return open_mode


def get_reader() -> DSVDictReader:
    """
    Retrieves a DSVDictReader object for reading a file.

    Returns:
        DSVDictReader: The reader object for reading the file.
    """
    file_name = input_file_path()

    print()

    open_mode = select_open_mode()
    print(f'Opening file {term_format(file_name, [TERM_ITALIC, TERM_FG_GREEN])} using {term_format(OPEN_SHORT_DESCS[open_mode[0]], [TERM_ITALIC, TERM_FG_GREEN])} mode...\n')

    # Create a reader
    try:
        reader = DSVDictReader(file_name, delimiter='\t', type_map=TYPE_MAP, mode=open_mode)
    except IOError:
        throw_error(f'Could not open {term_format(file_name, TERM_ITALIC)}. Please double check the file name is correct and the file contains the required format.')
        reader = get_reader()

    return reader


def filter_range_input(desc: str) -> tuple[float, float]:
    """
    Prompts the user to enter lower and upper filter limits for a given description.

    Args:
        desc (str): The description of the filter.

    Returns:
        tuple[float, float]: A tuple containing the lower and upper filter limits.
    """
    print(term_format('Enter a number for the upper and lower filter limits or type "Q" to quit.\nYou may leave one limit blank.', TERM_FG_CYAN))

    min_input = finput(f'Enter the LOWER limit (inclusive) for {desc}: ', TERM_FG_GREEN)

    if 'Q' == min_input:
        quit_app()

    max_input = finput(f'Enter the UPPER limit (inclusive) for {desc}: ', TERM_FG_GREEN)

    if 'Q' == max_input:
        quit_app()
    
    return filter_input_error_check(min_input, max_input, desc)


def filter_input_error_check(min_input: str, max_input: str, desc: str) -> tuple[float, float]:
    """
    Check for input errors in the filter range values.

    Args:
        min_input (str): The minimum value of the filter range.
        max_input (str): The maximum value of the filter range.
        desc (str): The description of the filter range.

    Returns:
        tuple[float, float]: A tuple containing the minimum and maximum values of the filter range.

    Raises:
        ValueError: If the limits are not valid numeric values.

    """
    if min_input == '' and max_input == '':
        throw_error('At least one limit must be set.')
        return filter_range_input(desc)

    min_input = '-inf' if min_input == '' else min_input
    max_input = 'inf' if max_input == '' else max_input

    try:
        return (float(min_input), float(max_input))
    except ValueError:
        throw_error('Limits must be valid numeric values.')
        return filter_range_input(desc)


def filter_data(data: list[dict], field: str, min_val = float('-inf'), max_val = float('inf')) -> list[dict]:
    """
    Filters the given data based on the specified field and value range.

    Args:
        data (list[dict]): The list of dictionaries representing the data.
        field (str): The field to filter on.
        min_val (float, optional): The minimum value for the field. Defaults to negative infinity.
        max_val (float, optional): The maximum value for the field. Defaults to positive infinity.

    Returns:
        list[dict]: The filtered data as a list of dictionaries.
    """
    return sorted([row for row in data if (val := row[field]) is not None and val >= min_val and val <= max_val], key=lambda x, k=field: (x[k], x['name']))


def select_output(data: list[dict], field):
    """
    Selects the output method for the filtered results.

    Args:
        data (list[dict]): The input data to be filtered.
        field: The field to be filtered.

    Returns:
        None
    """
    output_menus = Menu([MenuItem(
            prop['menu_desc'],
            lambda output_func=prop['func'], data=data, field=field: output_func(data, field)
        ) for option, prop in OUTPUT_OPTIONS.items()],
        'How would you like to output the filtered results?'
    )

    output_menus()


if __name__ == "__main__":
    main()
