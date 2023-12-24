"""
This module contains a table pretty printer.
"""

class TablePrinter:
    """
    Pretty print a table of data to the terminal.
    
    This class will ensure that all columns fit the longest value in each column with a
    set margin between columns, center the title if one is provided, and align numberic
    values to the right and non-numeric values to the left.
    """

    def __init__(self, header: tuple[str, ...], entries: list[tuple], title: str | None = None, colMargin: int = 4):
        """
        Initialize a TablePrinter object.

        Args:
            header (tuple[str, ...]): The header of the table.
            entries (list[tuple]): The entries of the table.
            title (str | None, optional): The title of the table. Defaults to None.
            colMargin (int, optional): The margin size between columns. Defaults to 4.
        """
        self._header = header
        self._entries = entries
        self.title = title
        self._headerLen = len(header)
        self._colSize = [len(name) for name in self._header] # Set minimum column size
        self._colMargin = colMargin


    def __str__(self):
        """
        Returns a string representation of the table.

        The string representation includes the title, header, and entries of the table.
        The title is printed centered above the table.
        The header is printed as the first row of the table.
        The entries are printed as subsequent rows of the table.

        Returns:
            str: The string representation of the table.
        """
        self._calcColumnSize()
        divider = ('=' * self._colMargin).join(['=' * size for size in self._colSize])
        
        str_repr = ''
        if self.title is not None:
            str_repr += f"{self.title:^{len(divider)}}\n" # Print centered title

        str_repr += self._formatRow(self._header) + '\n'
        str_repr += divider + '\n'
        
        for entry in self._entries:
            str_repr += self._formatRow(entry) + '\n'

        return str_repr


    def _calcColumnSize(self):
        """Iterates over entries, updating column size if a value is longer than the current size."""

        for entry in self._entries:
            # Ensure entry length matches header length
            if len(entry) != self._headerLen:
                raise ValueError("Entry length does not match header length.")

            # Update column size if entry value is longer than current size
            for i, colVal in enumerate(entry):
                if (col_size := len(str(colVal))) > self._colSize[i]:
                    self._colSize[i] = col_size


    def _formatRow(self, row: tuple[str, ...]) -> str:
        """Format a row of data to fit the column size and margin."""

        rowStr = ""
        for i, colVal in enumerate(row):
            if i == 0: # If first column, skip margin
                rowStr += f"{colVal:>{self._colSize[i]}}" if isinstance(colVal, int) or isinstance(colVal, float) or colVal.isdecimal() else f"{colVal:<{self._colSize[i]}}"
            else: # Otherwise, prepend margin    
                rowStr += f"{' ' * self._colMargin}{colVal:>{self._colSize[i]}}" if isinstance(colVal, int) or isinstance(colVal, float) or colVal.isdecimal() else f"{' ' * self._colMargin}{colVal:<{self._colSize[i]}}"

        return rowStr