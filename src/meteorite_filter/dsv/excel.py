from xlwt import Workbook


class ExcelDictWriter:
    def __init__(self, xls_path: str, fieldnames: list[str]) -> None:
        self._path = xls_path
        self._fieldnames = fieldnames
        self._workbook = Workbook()
        self._sheet = self._workbook.add_sheet('filteredMeteoriteData')
        self._cell = ExcelDictWriter._CellPointer(len(self.fieldnames))


    @property
    def path(self) -> str:
        return self._path


    @property
    def fieldnames(self) -> list[str]:
        return self._fieldnames


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


        def __iadd__(self, other: int) -> None:
            rows_inc = other // self._row_length
            cols_inc = other % self._row_length

            self.row += rows_inc
            self.col += cols_inc


        def __isub__(self, other: int) -> None:
            rows_inc = other // self._row_length
            cols_inc = other % self._row_length

            self.row -= rows_inc
            self.col -= cols_inc
