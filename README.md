# Individual Coding Assignment #1

Bridgewater State University - Computer Science Dept.

COMP390 - Software Engineering (Fall 2023)

Prof. Joeseph Matta

Author: Nick Manos

## Overview

The purpose of this application is to filter a large dataset. The target dataset is a collection of 45,716 data entries. Each entry has information about a single meteorite landing on Earth and consists of the following twelve data fields:

```TSV
name id nametype recclass mass (g) fall year reclat reclong GeoLocation States Counties
```

This dataset is provided as a text file ([*'meteorite_landings_data.txt'*](data/meteorite_landings_data.txt)). Each line of text in the file, except for the first line, is an entrly describing a single meteorite landing. (Remember: each line ends with a newline character, `'\n'`.) Each meteorite landing is described by the twelve fields listed above. These fields are "tab-separated" on each line. Meaning that in between each field value string there is a 'tab' character (`'\t'`). Some field values in a data entry line may be empty. Instead of having a value, empty fields consist of an empty string (`''`).

For full project requirements, see [COMP390F23_code_assignment_1.pdf](docs/COMP390F23_code_assignment_1.pdf)

## Output

This program will print two formatted tables to the terminal containing data entries filtered based on two criteria. The criteria and a partial output are shown below:

1. Name and Mass of all meteorites weighing *more than* 2,900,000 grams

   ```
         NAME                 MASS
    ===================================
    1    Al Haggounia 001      3000000
    2    Toluca                3000000
    3    Xifu                  3000000
    4    Yingde                3000000
    5    Youndegin             3800000
   ```

2. Name and Year of all meteorites falling in the year 2013 *or after* (2013-2022, inclusive)

   ```
         NAME                     YEAR
    ==================================
    1    Chelyabinsk              2013
    2    Northwest Africa 7755    2013
    3    Northwest Africa 7812    2013
    4    Northwest Africa 7822    2013
    5    Northwest Africa 7855    2013
   ```

## Running

This project requires `python >= 3.11`.

1. *(Optional)* Set up Python virtual envrionment in cloned folder and activate

   Windows:

   ```
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

   macOS/Linux:

   ```
   python3 -m venv .venv
   source ./.venv/bin/activate
   ```

2. Run program

   Windows:

   ```
   python meteorite_filter\filter_data.py
   ```

   macOS/Linux:

   ```
   python3 ./meteorite_filter/filter_data.py
   ```
