#!/usr/bin/env python3

from dsv.reader import DSVDictReader


def main():
    type_map = {
        'id': int,
        'mass (g)': float,
        'year': int,
        'reclat': float,
        'reclong': float,
        'States': int,
        'Counties': int
    }

    reader = DSVDictReader('./data/meteorite_landings_data.txt', delimiter='\t', type_map=type_map)

    heavy_meteorites = [row for row in reader if row['mass (g)'] is not None and row['mass (g)'] > 2_900_000]
    heavy_meteorites = sorted(heavy_meteorites, key=lambda x: x['mass (g)'])

    print(f'     {"NAME".ljust(21)}{"MASS".ljust(8)}')
    print('=' * 35)

    for row_no, row in enumerate(heavy_meteorites, 1):
        out_row = f'{row_no}'.ljust(5)
        out_row += f'{row["name"]}'.ljust(21)
        out_row += f'{int(row["mass (g)"])}'.rjust(8)

        print(out_row)

    print()

    reader = DSVDictReader('./data/meteorite_landings_data.txt', delimiter='\t', type_map=type_map)

    recent_meteorites = [row for row in reader if row['year'] is not None and row['year'] >= 2013]
    recent_meteorites = sorted(recent_meteorites, key=lambda x: x['year'])

    print(f'     {"NAME".ljust(25)}{"YEAR".ljust(4)}')
    print('=' * 34)

    for row_no, row in enumerate(recent_meteorites, 1):
        out_row = f'{row_no}'.ljust(5)
        out_row += f'{row["name"]}'.ljust(25)
        out_row += f'{row["year"]}'.ljust(4)

        print(out_row)


if __name__ == "__main__":
    main()
