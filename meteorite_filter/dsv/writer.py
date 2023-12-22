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

        output += '\n'

        return output


    def __del__(self):
        """Close the DSV file when the object is deleted."""

        if hasattr(self, '_file'):
            self._file.close()


class DSVDictWriter(DSVWriter):
    def __init__(self, dsv_path: str, fieldnames: list[str], delimiter: str = ',', mode: str = 'w') -> None:
        super().__init__(dsv_path, delimiter, mode)
        self._fieldnames = fieldnames


    @property
    def fieldnames(self) -> list[str]:
        return self._fieldnames


    def writeheader(self) -> int:
        return super().writerow(self.fieldnames)


    def writerow(self, row: dict) -> int:
        if len(row) != len(self.fieldnames):
            raise ValueError

        ordered_row = [row[field] for field in self.fieldnames]
        return super().writerow(ordered_row)


    def writerows(self, rows: list[dict]) -> None:
        for row in rows:
            self.writerow(row)
