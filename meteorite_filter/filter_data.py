#!/usr/bin/env python3

from meteorite_filter.dsv.reader import DSVDictReader
from meteorite_filter.tui.menu import Menu, MenuItem


def main():
    print(
        '''\
Meteorite Data Filter
(c) October 2023 Nick Manos
        
Welcome! This application allows you to filter a provided meteorite data file.

To begin, please type the filename, including its file extension and path if
necessary. (Ex: "meteorite_landings_data.txt") To exit the application, type "?q":\
'''
    )
    file_name = input('file> ')

    if file_name in ('?q', '?Q'):
        exit(0)

    open_mode = ''
    def set_open_mode(mode: str):
        nonlocal open_mode
        open_mode += mode

    open_mode_menu = Menu(
        [
            MenuItem('open for reading', lambda: 'r', set_open_mode),
            MenuItem('open for writing, truncating the file first', lambda: 'w', set_open_mode),
            MenuItem('open for exclusive creation, failing if the file already exists', lambda: 'x', set_open_mode),
            MenuItem('open for writing, appending to the end of the file if it exists', lambda: 'a', set_open_mode)
        ],
        'What mode would you like to use to open the file?',
        'Type a letter or number to select your choice or press enter for the default\nmode> ',
        0
    )

    open_format_menu = Menu(
        [
            MenuItem('text mode', lambda: 't', set_open_mode),
            MenuItem('binary mode', lambda: 'b', set_open_mode)
        ],
        'What format would you like to use to open the file?',
        'Type a letter or number to select your choice or press enter for the default\nformat> ',
        0
    )

    open_rw_menu = Menu(
        [
            MenuItem('Yes', lambda: '+', set_open_mode),
            MenuItem('No', lambda: '', set_open_mode)
        ],
        'Would you like to open the file for reading and writing?',
        'Type a letter or number to select your choice or press enter for the default\nread/write> ',
        1
    )

    open_mode_menu()
    open_format_menu()
    open_rw_menu()

    print(f'Opening file "{file_name}" using mode "{open_mode}"...')

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
    reader = DSVDictReader(file_name, delimiter='\t', type_map=type_map, mode=open_mode)

    # Filter the data by mass
    heavy_meteorites = [row for row in reader if row['mass (g)'] is not None and row['mass (g)'] > 2_900_000]

    # Sort the data
    heavy_meteorites = sorted(heavy_meteorites, key=lambda x: x['mass (g)'])

    # Print the data
    print(f'     {"NAME".ljust(21)}{"MASS".ljust(8)}')
    print('=' * 35)

    for row_no, row in enumerate(heavy_meteorites, 1):
        out_row = f'{row_no}'.ljust(5)
        out_row += f'{row["name"]}'.ljust(21)
        out_row += f'{int(row["mass (g)"])}'.rjust(8)

        print(out_row)

    print()

    # Reset the reader
    reader = DSVDictReader('./data/meteorite_landings_data.txt', delimiter='\t', type_map=type_map)

    # Filter the data by year
    recent_meteorites = [row for row in reader if row['year'] is not None and row['year'] >= 2013]

    # Sort the data
    recent_meteorites = sorted(recent_meteorites, key=lambda x: x['year'])

    # Print the data
    print(f'     {"NAME".ljust(25)}{"YEAR".ljust(4)}')
    print('=' * 34)

    for row_no, row in enumerate(recent_meteorites, 1):
        out_row = f'{row_no}'.ljust(5)
        out_row += f'{row["name"]}'.ljust(25)
        out_row += f'{row["year"]}'.ljust(4)

        print(out_row)


if __name__ == "__main__":
    main()
