# Individual Coding Assignment #1.2

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

### Installation

To install this program, download and extract the zip file, navigate to the folder in your command line or terminal, and type the following command:

```
python3 -m pip install -r requirements.txt
```

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
   r - open for reading (default)
   w - open for writing, truncating the file first (WARNING: This will delete
       all contents of the file)
   x - open for exclusive creation, failing if the file already exists
   a - open for writing, appending to the end of the file if it exists
   >q - Quit the application
   ```
   
   Type the number or letter of your choice. For most users, the default option (`1`) is best.

4. The application will now attempt to open your file using the options you've chosen. If unsuccessful, you will be given a chance to try change your selections.

   If opening your file succeeds, you will be shown a menu to choose whether you'd like to filter by year or mass:

   ```
   1 - Meteorite mass
   2 - Year meteorite fell
   q - Quit the application
   ```

   Type the number of your choice. The remainder of this manual will use year (option `2`) for its examples.

5. You will now be prompted to provide the range of your filter:

   ```
   Enter the LOWER limit (inclusive) for the year the meteorite fell: 1901
   Enter the UPPER limit (inclusive) for the year the meteorite fell: 1902
   ```

   **NOTE:** You may choose to set *only* a lower limit or *only* an upper limit by leaving the other option blank:

   ```
   Enter the LOWER limit (inclusive) for the year the meteorite fell: 
   Enter the UPPER limit (inclusive) for the year the meteorite fell: 1902
   ```

6. You will now be asked what kind of output you'd like for the filtered data:
   
   ```
   1 - Display on screen
   2 - Save to a text (.txt) file
   3 - Save to an Excel (.xls) file
   q - Quit the application
   ```

7. If you chose options 2 or 3, you will find the data in a file saved to your current folder. The file name will use the current date and time. If you chose option 1, you will now be shown a table with your filtered data:
   
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

8. You will again be shown the menu to choose the field to filter your data by. You may filter the data as many times with as many different ranges as you wish.

9.  When you are done, type `Q` to quit the application. You may also quit by typing `Q` at any prompt throughout the application.
    
    **NOTE:** You must type `>Q` to quit at the file name prompt. Failure to include the `>` will result in the application attempting to open a file named "`Q`".

## Project Status

All project requirements completed.

For full project requirements, see [COMP390F23_code_assignment_1_2.pdf](docs/COMP390F23_code_assignment_1_2.pdf)
