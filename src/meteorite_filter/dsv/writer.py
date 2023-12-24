"""The dsv.writer module provides classes for writing files in a
Delimiter Seperated Value (DSV) format. The DSV format is a format for
storing tabular data in a text file. Common delimiters include commas (CSV)
and tabs (TSV).

The DSVWriter class provides an easy way to iteratively write the lines of a DSV
file. The DSVDictWriter class provides similar functionality, but uses
a dictionary for each line instead of a list of strings.

Both classes are inspired by the Python stdlib csv module.
"""

class DSVWriter:
    """A class for writing files in a Delimiter Seperated Value (DSV) format.

    The DSV format is a format for storing tabular data in a text file. Common
    delimiters include commas (CSV) and tabs (TSV).
    """

    def __init__(self, dsv_path: str, delimiter: str = ',', mode: str = 'w') -> None:
        """
        Initializes a DSVWriter object.

        Args:
            dsv_path (str): The path to the DSV file.
            delimiter (str, optional): The delimiter used in the DSV file. Defaults to ','.
            mode (str, optional): The mode in which the file is opened. Defaults to 'w'.
        """
        self._file = open(dsv_path, mode, encoding='utf-8')
        self._delimiter = delimiter

    @property
    def delimiter(self):
        """
        Get the delimiter used in the DSV writer.

        Returns:
            str: The delimiter used in the DSV writer.
        """
        return self._delimiter


    def writerow(self, row: list) -> int:
        """
        Writes a single row of data to the file.

        Args:
            row (list): The row of data to be written.

        Returns:
            int: The number of characters written to the file.
        """
        ret_val = self._file.write(self._format_row(row))
        self._file.flush()
        return ret_val


    def writerows(self, rows: list[list]):
        """
        Writes multiple rows to the file.

        Args:
            rows (list[list]): A list of rows to be written to the file.
        """
        for row in rows:
            self._file.write(self._format_row(row))


    def _format_row(self, row: list) -> str:
        """
        Formats a row of data into a delimited string.

        Args:
            row (list): The row of data to be formatted.

        Returns:
            str: The formatted row as a delimited string.
        """
        output = ''
        for idx, field in enumerate(row, 1):
            if field is not None:
                output += str(field)

            if idx < len(row):
                output += self.delimiter

        output += '\n'

        return output


    def __del__(self):
        """Close the DSV file when the object is deleted."""

        if hasattr(self, '_file'):
            self._file.close()


class DSVDictWriter(DSVWriter):
    '''
    A class for reading a DSV file from the data in a dictionary.
    '''
    def __init__(self, dsv_path: str, fieldnames: list[str], delimiter: str = ',', mode: str = 'w') -> None:
        """
        Initialize a DSVWriter object.

        Args:
            dsv_path (str): The path to the DSV file.
            fieldnames (list[str]): The list of field names for the DSV file.
            delimiter (str, optional): The delimiter used in the DSV file. Defaults to ','.
            mode (str, optional): The mode in which the DSV file is opened. Defaults to 'w'.
        """
        super().__init__(dsv_path, delimiter, mode)
        self._fieldnames = fieldnames


    @property
    def fieldnames(self) -> list[str]:
        """
        Get the list of field names for the writer.

        Returns:
            list[str]: The field names.
        """
        return self._fieldnames


    def writeheader(self) -> int:
        """
        Writes the header row to the file.

        Returns:
            int: The number of characters written.
        """
        return super().writerow(self.fieldnames)


    def writerow(self, row: dict) -> int:
        """
        Writes a single row to the DSV file.

        Args:
            row (dict): A dictionary representing the row data.

        Returns:
            int: The number of characters written to the file.

        Raises:
            ValueError: If the length of the row dictionary does not match the number of fieldnames.
        """
        if len(row) != len(self.fieldnames):
            raise ValueError

        ordered_row = [row[field] for field in self.fieldnames]
        return super().writerow(ordered_row)


    def writerows(self, rows: list[dict]) -> None:
        """
        Write multiple rows to the DSV file.

        Args:
            rows (list[dict]): A list of dictionaries representing the rows to be written.

        Raises:
            ValueError: If the number of fields in any row does not match the number of fieldnames.

        Returns:
            None
        """
        for row in rows:
            if len(row) != len(self.fieldnames):
                raise ValueError

        ordered_rows = [self._dict_to_row_list(row) for row in rows]
        super().writerows(ordered_rows)

    def _dict_to_row_list(self, row: dict):
        """
        Converts a dictionary row to a list of values.

        Args:
            row (dict): The dictionary row to convert.

        Returns:
            list: A list of values extracted from the dictionary row.
        """
        return [row[field] for field in self.fieldnames]
