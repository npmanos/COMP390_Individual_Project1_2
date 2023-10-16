#!/usr/bin/env python3

from constants import *
from dsv.reader import DSVDictReader
from tui.menu import Menu, MenuItem, ReturnableMenuItem
from tui.table import TablePrinter
from tui.utils import *


def main():
    clear()
    print(WELCOME_MESSAGE + '\n')

    reader = open_file()

    data = list(reader)

    filter_menus = Menu(
        [
            ReturnableMenuItem(
                v['menu_desc'],
                lambda desc=v['input_desc']: filter_range_input(desc),
                lambda range, data=data, field=k: print_table(filter_data(data, field, *range), field)
            ) for k, v in FILTER_OPTIONS.items()
        ],
        'Which field would you like to use to filter the data?'
    )

    filter_menus()


def open_file() -> DSVDictReader:
    print(term_format('To begin, please type the filename, including its file extension and path if\nnecessary (ex: "file.txt"). To exit the application, type "?q"', TERM_FG_CYAN))
    file_name = finput('> ', TERM_FG_GREEN)

    if file_name in ('?q', '?Q'):
        quit_app()

    print()

    open_mode = ''
    def set_open_mode(mode: str):
        nonlocal open_mode
        open_mode += mode

    open_mode_menu = Menu(
        [MenuItem(mode['desc'], lambda m=mode['param']: m, set_open_mode) for mode in OPEN_MODES],
        'What mode would you like to use to open the file?',
        default=0
    )

    open_mode_menu()

    open_format_menu = Menu(
        [MenuItem(mode['desc'], lambda m=mode['param']: m, set_open_mode) for mode in OPEN_FORMATS],
        'What format would you like to use to open the file?',
        default=0
    )

    open_format_menu()

    open_rw_menu = Menu(
        [
            MenuItem('Yes', lambda: '+', set_open_mode),
            MenuItem('No', lambda: '', set_open_mode)
        ],
        'Would you like to open the file for reading and writing?',
        default=1
    )

    open_rw_menu()

    print(f'Opening file {term_format(term_format(file_name, TERM_FG_GREEN), TERM_ITALIC)} using {TERM_FG_GREEN[0]}{TERM_ITALIC[0]}{OPEN_SHORT_DESCS[open_mode[0]]}{" "+OPEN_SHORT_DESCS[open_mode[1]]}{" (read/write)" if len(open_mode) == 3 else ""}{TERM_FG_DEFAULT}{TERM_ITALIC[1]} mode...\n')

    # Create a reader
    try:
        reader = DSVDictReader(file_name, delimiter='\t', type_map=TYPE_MAP, mode=open_mode)
    except IOError:
        throw_error(f'Could not open {term_format(file_name, TERM_ITALIC)}. Please double check the file name is correct and the file contains the required format.')
        reader = open_file()
    
    
    return reader


def filter_range_input(desc: str) -> tuple[float, float]:
    print(term_format('Enter a number for the upper and lower filter limits or type "q" to quit.\nYou may leave one limit blank.', TERM_FG_CYAN))

    min_input = finput(f'Enter the LOWER limit (inclusive) for {desc}: ', TERM_FG_GREEN)

    if 'q' == min_input:
        quit_app()

    max_input = finput(f'Enter the UPPER limit (inclusive) for {desc}: ', TERM_FG_GREEN)

    if 'q' == max_input:
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


def print_table(data: list[dict], field: str):
    heavy_table = TablePrinter(('', 'NAME', FILTER_OPTIONS[field]['header']), [(row_no, row['name'], row[field]) for row_no, row in enumerate(data, 1)])
    print()
    print(heavy_table)

if __name__ == "__main__":
    main()
