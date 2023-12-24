from xlwt import Workbook
from xlwt.Worksheet import Worksheet


class ExcelDictWriter:
    def __init__(self, xls_path: str, fieldnames: list[str]) -> None:
        self._path = xls_path
        self._fieldnames = fieldnames
        self._workbook = Workbook()
        self._sheet: Worksheet = self._workbook.add_sheet('filteredMeteoriteData')
        self._cell = ExcelDictWriter._CellPointer(len(self.fieldnames))


    @property
    def path(self) -> str:
        return self._path


    @property
    def fieldnames(self) -> list[str]:
        return self._fieldnames


    def writeheader(self) -> None:
        # cell = self._cell

        self._fresh_row()

        for field in self.fieldnames:
            self._sheet.write(self._cell.row, self._cell.col, field)
            self._cell += 1


    def writerow(self, row: dict):
        if len(row) != len(self.fieldnames):
            raise ValueError

        # cell = self._cell

        self._fresh_row()

        for field in self.fieldnames:
            if row[field] is None:
                self._cell += 1
                continue

            self._sheet.write(self._cell.row, self._cell.col, row[field])
            self._cell += 1


    def writerows(self, rows: list[dict]) -> None:
        for row in rows:
            self.writerow(row)


    def save(self) -> None:
        self._workbook.save(self.path)


    def _fresh_row(self) -> None:
        # cell = self._cell
        if self._cell.col > 0:
            self._cell.nextrow()


    class _CellPointer:
        _row = 0
        _col = 0

        def __init__(self, row_length: int) -> None:
            self._row_length = row_length


        @property
        def row(self) -> int:
            return self._row


        @row.setter
        def row(self, num: int) -> None:
            if num < 0:
                raise ValueError

            self._row = num


        @property
        def col(self) -> int:
            return self._col


        @col.setter
        def col(self, num: int):
            if num < 0 or num >= self._row_length:
                raise ValueError

            self._col = num


        def nextrow(self) -> None:
            self.row += 1
            self.col = 0


        def __add__(self, other: int):
            self.row += (self.col + other) // self._row_length
            self.col = (self.col + other) % self._row_length

            # self.row += rows_inc
            # self.col += cols_inc

            return self


        def __sub__(self, other: int):
            rows_inc = other // self._row_length
            cols_inc = other % self._row_length

            self.row -= rows_inc
            self.col -= cols_inc

            return self
