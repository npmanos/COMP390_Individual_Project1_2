class DSVWriter:
    """A class for writing files in a Delimiter Seperated Value (DSV) format.

    The DSV format is a format for storing tabular data in a text file. Common
    delimiters include commas (CSV) and tabs (TSV).
    """

    def __init__(self, dsv_path: str, delimiter: str = ',', mode: str = 'w') -> None:
        self._file = open(dsv_path, mode)
        self._delimiter = delimiter

    @property
    def delimiter(self):
        return self._delimiter


    def writerow(self, row: list) -> int:
        return self._file.write(self._format_row(row))


    def writerows(self, rows: list[list]):
        for row in rows:
            self.writerow(row)


    def _format_row(self, row: list) -> str:
        output = ''
        for idx, field in enumerate(row, 1):
            if field is not None:
                output += str(field)                
            
            if idx < len(row):
                output += self.delimiter

        return output
