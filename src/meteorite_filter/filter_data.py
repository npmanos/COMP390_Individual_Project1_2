#!/usr/bin/env python3

from meteorite_filter.constants import *
from meteorite_filter.dsv.reader import DSVDictReader
from meteorite_filter.tui.menu import Menu, MenuItem, ReturnableMenuItem
from meteorite_filter.tui.utils import *


def main():
    clear()
    print(WELCOME_MESSAGE + '\n')

    reader = open_file()

    data = list(reader)

    filter_menus = Menu(
        [
            ReturnableMenuItem(
                prop['menu_desc'],
                lambda desc=prop['input_desc']: filter_range_input(desc),
                lambda range, data=data, field=option: select_output(filter_data(data, field, *range), field)
            ) for option, prop in FILTER_OPTIONS.items()
        ],
        'Which field would you like to use to filter the data?'
    )

    filter_menus()


def open_file() -> DSVDictReader:
    print(term_format('To begin, please type the filename, including its file extension and path if\nnecessary (ex: "file.txt"). To exit the application, type ">q" or ">Q"', TERM_FG_CYAN)) # '?' and '>' are not valid filename characters in Windows and is used in case a user has a file named 'q'. This remains an issue on Linux and macOS
    file_name = finput('> ', TERM_FG_GREEN)

    if file_name in ('?q', '?Q', '>q', '>Q'):
        quit_app()

    print()

    open_mode = ''
    def set_open_mode(mode: str):
        nonlocal open_mode
        open_mode += mode

    open_mode_menu = Menu(
        {mode['param']: MenuItem(mode['desc'], lambda m=mode['param']: m, set_open_mode) for mode in OPEN_MODES},
        'What mode would you like to use to open the file?',
        default=0, quit_label='>q'
    )

    open_mode_menu()

    print(f'Opening file {term_format(file_name, [TERM_ITALIC, TERM_FG_GREEN])} using {term_format(OPEN_SHORT_DESCS[open_mode[0]], [TERM_ITALIC, TERM_FG_GREEN])} mode...\n')

    # Create a reader
    try:
        reader = DSVDictReader(file_name, delimiter='\t', type_map=TYPE_MAP, mode=open_mode)
    except IOError:
        throw_error(f'Could not open {term_format(file_name, TERM_ITALIC)}. Please double check the file name is correct and the file contains the required format.')
        reader = open_file()
    
    
    return reader


def filter_range_input(desc: str) -> tuple[float, float]:
    print(term_format('Enter a number for the upper and lower filter limits or type "Q" to quit.\nYou may leave one limit blank.', TERM_FG_CYAN))

    min_input = finput(f'Enter the LOWER limit (inclusive) for {desc}: ', TERM_FG_GREEN)

    if 'Q' == min_input:
        quit_app()

    max_input = finput(f'Enter the UPPER limit (inclusive) for {desc}: ', TERM_FG_GREEN)

    if 'Q' == max_input:
        quit_app()
    
    if min_input == '' and max_input == '':
        throw_error('At least one limit must be set.')
        return filter_range_input(desc)
    elif min_input == '':
        min_input = '-inf'
    elif max_input == '':
        max_input = 'inf'

    try:
        return (float(min_input), float(max_input))
    except ValueError:
        throw_error('Limits must be valid numeric values.')
        return filter_range_input(desc)


def filter_data(data: list[dict], field: str, min_val = float('-inf'), max_val = float('inf')) -> list[dict]:
    return sorted([row for row in data if (val := row[field]) is not None and val >= min_val and val <= max_val], key=lambda x, k=field: (x[k], x['name']))


def select_output(data: list[dict], field):
    output_menus = Menu([MenuItem(
            prop['menu_desc'],
            lambda output_func=prop['func'], data=data, field=field: output_func(data, field)
        ) for option, prop in OUTPUT_OPTIONS.items()],
        'How would you like to output the filtered results?'
    )

    output_menus()


if __name__ == "__main__":
    main()
