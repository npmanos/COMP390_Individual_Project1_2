#!/usr/bin/env python3

from dsv.reader import DSVDictReader


def main():
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
    reader = DSVDictReader('./data/meteorite_landings_data.txt', delimiter='\t', type_map=type_map)

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
