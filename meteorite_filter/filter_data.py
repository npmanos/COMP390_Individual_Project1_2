#!/usr/bin/env python3

from dsv.reader import DSVDictReader
from tui.menu import Menu, MenuItem
from constants import *
from tui.table import TablePrinter


def main():
    print(WELCOME_MESSAGE + '\n')

    reader = open_file()

    data = list(reader)

    # Filter the data by mass
    heavy_meteorites = filter_data(data, 'mass (g)', 2_900_001)

    # Print the data
    heavy_table = TablePrinter(('', 'NAME', 'MASS'), [(row_no, row['name'], row['mass (g)']) for row_no, row in enumerate(heavy_meteorites, 1)])
    print(heavy_table)

    # Filter the data by year
    recent_meteorites = filter_data(data, 'year', '2013')

    # Print the data
    recent_table = TablePrinter(('', 'NAME', 'YEAR'), [(row_no, row['name'], row['year']) for row_no, row in enumerate(recent_meteorites, 1)])
    print(recent_table)


def open_file() -> DSVDictReader:
    print('To begin, please type the filename, including its file extension and path if')
    print('necessary (ex: "file.txt"). To exit the application, type "?q"')
    file_name = input('> ')

    if file_name in ('?q', '?Q'):
        exit(0)

    open_mode = ''
    def set_open_mode(mode: str):
        nonlocal open_mode
        open_mode += mode

    open_mode_menu = Menu(
        [MenuItem(mode['desc'], lambda m=mode['param']: m, set_open_mode) for mode in OPEN_MODES],
        'What mode would you like to use to open the file?',
        default=0
    )

    open_format_menu = Menu(
        [MenuItem(mode['desc'], lambda m=mode['param']: m, set_open_mode) for mode in OPEN_FORMATS],
        'What format would you like to use to open the file?',
        default=0
    )

    open_rw_menu = Menu(
        [
            MenuItem('Yes', lambda: '+', set_open_mode),
            MenuItem('No', lambda: '', set_open_mode)
        ],
        'Would you like to open the file for reading and writing?',
        default=1
    )

    open_mode_menu()
    open_format_menu()
    open_rw_menu()

    print(f'Opening file "{file_name}" using {OPEN_SHORT_DESCS[open_mode[0]]}{" "+OPEN_SHORT_DESCS[open_mode[1]]}{" (read/write)" if len(open_mode) == 3 else ""} mode...\n')

    # Create a type map to convert values to specified types
    type_map = {
        'id': int,
        'mass (g)': float,
        'year': int,
        'reclat': float,
        'reclong': float,
        'States': int,
        'Counties': int
    }

    # Create a reader
    try:
        reader = DSVDictReader(file_name, delimiter='\t', type_map=type_map, mode=open_mode)
    except:
        print(f'ERROR! Could not open {file_name}. Please double check the file name is correct and the file contains the required format.')
        reader = open_file()
    
    return reader


def filter_data(data: list[dict], field: str, min_val: str | float = float('-inf'), max_val: str | float = float('inf')):
    if isinstance(min_val, str):
        min_val = float(min_val)

    if isinstance(max_val, str):
        max_val = float(max_val)

    return sorted([row for row in data if (val := row[field]) is not None and val >= min_val and val < max_val], key=lambda x, k=field: x[k])


if __name__ == "__main__":
    main()
