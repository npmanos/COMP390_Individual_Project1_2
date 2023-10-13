"""The dsv.reader module provides classes for reading files in a
Delimiter Seperated Value (DSV) format. The DSV format is a format for
storing tabular data in a text file. Common delimiters include commas (CSV)
and tabs (TSV).

The DSVReader class provides an easy way to iterate over the lines of a DSV
file. The DSVDictReader class provides similar functionality, but returns
a dictionary for each line instead of a list of strings.

Both classes are inspired by the Python stdlib csv module.
"""

class DSVReader:
    """A class for reading files in a Delimiter Seperated Value (DSV) format.

    The DSV format is a format for storing tabular data in a text file. Common
    delimiters include commas (CSV) and tabs (TSV).
    """

    def __init__(self, dsv_path: str, delimiter=',', newline: str | None=None, mode='r'):
        """Initialize a DSVReader object.

        Args:
            dsv_path: The path to the DSV file to read.
            delimiter: The character that separates values on a line. Defaults to ','.
            newline: The character(s) that separate lines. If None, the default
                line separator for the operating system will be used.
        """
        self._file = open(dsv_path, mode, newline=newline)
        self.delimiter = delimiter
        self._line_num = 0

        if newline is None:
            self._newline = '\n'
        else:
            self._newline = newline

    def __del__(self):
        """Close the DSV file when the object is deleted."""
        self._file.close()

    @property
    def line_num(self):
        """The number of lines read so far."""
        return self._line_num

    def __iter__(self):
        """Return an iterator over the lines of the file."""
        return self

    def __next__(self) -> list[str]:
        """Return the next line of the file as a list of strings.

        Raises:
            StopIteration: If there are no more lines to read.
        """
        self._line_num += 1
        return next(self._file).rstrip(self._newline).split(self.delimiter)


class DSVDictReader(DSVReader):
    '''
    A class for reading a DSV file and returning the data as a dictionary.
    '''

    def __init__(
            self,
            dsv_path: str,
            delimiter=',',
            fieldnames: list[str] | None=None,
            type_map: dict | None=None,
            mode: str = 'r'):
        """Initialize a DSVDictReader object.

        Args:
            dsv_path: The path to the DSV file to be read.
            delimiter: The delimiter of the DSV file. Defaults to ','.
            fieldnames: The fieldnames of the DSV file. Defaults to first row of the file.
            type_map: An optional dictionary mapping fieldnames to functions for parsing the field values.
        """
        super().__init__(dsv_path, delimiter, mode=mode)

        if fieldnames is None:
            self._fieldnames = super().__next__()
        else:
            self._fieldnames = fieldnames

        self._type_map = type_map

    @property
    def fieldnames(self):
        '''
        The fieldnames of the DSV file.
        '''
        return self._fieldnames

    def __next__(self) -> dict:
        '''
        Returns the next row of the DSV file as a dictionary.

        Raises:
            StopIteration: If there are no more lines to read.
        '''
        row_dict = dict(zip(self._fieldnames, super().__next__()))

        if self._type_map is not None:
            for field, type_func in self._type_map.items():
                if row_dict[field] != '':
                    row_dict[field] = type_func(row_dict[field])
                else:
                    row_dict[field] = None #type: ignore

        return row_dict
