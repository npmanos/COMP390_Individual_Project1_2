"""
This module contains classes to write Excel (xls) files.
"""

from xlwt import Workbook
from xlwt.Worksheet import Worksheet


class ExcelDictWriter:
    """
    A class for writing dictionaries to an Excel file.

    Args:
        xls_path (str): The path to the Excel file.
        fieldnames (list[str]): The list of field names for the Excel columns.
    """
    def __init__(self, xls_path: str, fieldnames: list[str]) -> None:
            """
            Initializes an instance of the ExcelDictWriter class.

            Args:
                xls_path (str): The path to the Excel file.
                fieldnames (list[str]): The list of field names for the Excel columns.
            """
            self._path = xls_path
            self._fieldnames = fieldnames
            self._workbook = Workbook()
            self._sheet: Worksheet = self._workbook.add_sheet('filteredMeteoriteData')
            self._cell = ExcelDictWriter._CellPointer(len(self.fieldnames))


    @property
    def path(self) -> str:
        """
        Get the path of the Excel file.

        Returns:
            str: The path of the Excel file.
        """
        return self._path


    @property
    def fieldnames(self) -> list[str]:
        """
        Get the field names of the Excel file.

        Returns:
            list[str]: The field names.
        """
        return self._fieldnames


    def writeheader(self) -> None:
        """
        This method writes the fieldnames as the header row in the Excel sheet.

        Returns:
            None
        """
        self._fresh_row()

        for field in self.fieldnames:
            self._sheet.write(self._cell.row, self._cell.col, field)
            self._cell += 1


    def writerow(self, row: dict):
        """
        Writes a row of data to the Excel sheet.

        Args:
            row (dict): A dictionary representing a row of data, where the keys are field names and the values are the corresponding values.

        Raises:
            ValueError: If the length of the row dictionary does not match the number of fieldnames.

        Returns:
            None
        """
        if len(row) != len(self.fieldnames):
            raise ValueError

        self._fresh_row()

        for field in self.fieldnames:
            if row[field] is None:
                self._cell += 1
                continue

            self._sheet.write(self._cell.row, self._cell.col, row[field])
            self._cell += 1


    def writerows(self, rows: list[dict]) -> None:
        """
        Writes multiple rows to the Excel file.

        Args:
            rows (list[dict]): A list of dictionaries representing the rows to be written.
        
        Raises:
            ValueError: If the length of a row dictionary does not match the number of fieldnames.

        Returns:
            None
        """
        for row in rows:
            self.writerow(row)


    def save(self) -> None:
        """
        Saves the workbook to the specified path.
        """
        self._workbook.save(self.path)


    def _fresh_row(self) -> None:
        """
        This method is used to move the cursor to the next row in the Excel sheet
        when processing data. It ensures that the cursor is positioned at the
        beginning of the row.

        Returns:
            None
        """
        if self._cell.col > 0:
            self._cell.nextrow()


    class _CellPointer:
        """
        A class for tracking the current cell location in an Excel sheet.
        """
        _row = 0
        _col = 0

        def __init__(self, row_length: int) -> None:
            """
            Initializes an instance of the CellPointer class.

            Args:
                row_length (int): The maximum row length in the Excel file.

            Returns:
                None
            """
            self._row_length = row_length


        @property
        def row(self) -> int:
            """
            Get the row number of the Excel cell.

            Returns:
                int: The row number.
            """
            return self._row


        @row.setter
        def row(self, num: int) -> None:
            """
            Setter method for the 'row' property.

            Args:
                num (int): The row number to set.

            Raises:
                ValueError: If the given row number is less than 0.
            """
            if num < 0:
                raise ValueError

            self._row = num


        @property
        def col(self) -> int:
            """
            Returns the column number of the cell.
            
            Returns:
                int: The column number of the cell.
            """
            return self._col


        @col.setter
        def col(self, num: int):
            """
            Sets the current column index to the specified number.

            Args:
                num (int): The column index to set.

            Raises:
                ValueError: If the specified column index is out of range.

            Returns:
                None
            """
            if num < 0 or num >= self._row_length:
                raise ValueError

            self._col = num


        def nextrow(self) -> None:
            """
            Move the cursor to the next row in the Excel sheet.
            """
            self.row += 1
            self.col = 0


        def __add__(self, other: int):
            """
            Adds an integer value to the current position in the Excel sheet, wrapping to the
            next row when the cell is at the maximum row length.

            Args:
                other (int): The integer value to be added.

            Returns:
                self: The updated Excel sheet position.
            """
            self.row += (self.col + other) // self._row_length
            self.col = (self.col + other) % self._row_length
            return self
