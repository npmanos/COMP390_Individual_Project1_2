# Individual Coding Assignment #1.1

Bridgewater State University - Computer Science Dept.

COMP390-002 - Software Engineering (Fall 2023)

Prof. Joeseph Matta

Author: Nick Manos

## User Guide

The Meteorite Data Filter application allows you to filter a data file containing meteorite landings by the meteorite's mass or the year it fell and display the filtered data in a table. Interactive menus allow you to open your file and choose your filter options.

### Requirements

- [Python 3.11 or newer](https://www.python.org/downloads/)
- A text file containing meteorite landings data. This file ***must*** have one meteorite landing per line and contain the following 12 data fields separated by a tab character:

   ```TSV
   name id nametype recclass mass (g) fall year reclat reclong GeoLocation States Counties
   ```

   If a field has no value, it must be left blank between tabs.

### Demo

[![asciicast](https://asciinema.org/a/SBSSGbBN0Ht1djIIWQdwkNunS.svg)](https://asciinema.org/a/SBSSGbBN0Ht1djIIWQdwkNunS)

### Using The Application

1. To begin, type the following into your command line or terminal:

   ```
   python3 meteorite_filter/filter_data.py
   ```

2. You will then be prompted to enter the name and location of your data file. If your file has a file extension (e.g. `.txt`), please be sure to include it. If your data file is not in the same folder as you are currently working in, please be sure to include the path to the file (e.g. `data/meteorites/landings.txt`)

   ```
   > meteorite_landings_data.txt
   ```

3. Next, you will select which mode to use to attempt to open the file:

   ```
   1 - open for reading (default)
   2 - open for writing, truncating the file first
   3 - open for exclusive creation, failing if the file already exists
   4 - open for writing, appending to the end of the file if it exists
   q - Quit the application
   ```
   
   Type the number or letter of your choice. For most users, the default option (`1`) is best.

4. Then, you will select which format to use for opening the data file:

   ```
   1 - text mode (default)
   2 - binary mode
   q - Quit the application
   ```

   Once again, the default option (`1`) is the best option for most users.

5. Finally, you will be asked if you'd like to open the file for reading and writing:

   ```
   1 - Yes
   2 - No (default)
   q - Quit the application
   ```

   Again, most users should choose the default (`2`).

6. The application will now attempt to open your file using the options you've chosen. If unsuccessful, you will be given a chance to try change your selections.

   If opening your file succeeds, you will be shown a menu to choose whether you'd like to filter by year or mass:

   ```
   1 - Meteorite mass
   2 - Year meteorite fell
   q - Quit the application
   ```

   Type the number of your choice. The remainder of this manual will use year (option `2`) for its examples.

7. You will now be prompted to provide the range of your filter:

   ```
   Enter the LOWER limit (inclusive) for the year the meteorite fell: 1901
   Enter the UPPER limit (inclusive) for the year the meteorite fell: 1902
   ```

   **NOTE:** You may choose to set *only* a lower limit or *only* an upper limit by leaving the other option blank:

   ```
   Enter the LOWER limit (inclusive) for the year the meteorite fell: 
   Enter the UPPER limit (inclusive) for the year the meteorite fell: 1902
   ```

8. You will now be shown a table with your filtered data:
   
   ```
        NAME                         YEAR
   =======================================
   1    Ashfork                      1901
   2    Chervettaz                   1901
   3    Gay Gulch                    1901
   4    Hendersonville               1901
   5    Hvittis                      1901
   ```

   *Table shortened for length*

9. You will again be shown the menu to choose the field to filter your data by. You may filter the data as many times with as many different ranges as you wish.

10. When you are done, type `q` to quit the application. You may also quit by typing `q` at any prompt throughout the application.
    
    **NOTE:** You must type `?q` to quit at the file name prompt. Failure to include the `?` will result in the application attempting to open a file named "`q`".

## Project Status

All project requirements completed.

For full project requirements, see [COMP390F23_code_assignment_1_1.pdf](docs/COMP390F23_code_assignment_1_1.pdf)

While not required by this project, additional comments and docstrings need to be written or updated.
