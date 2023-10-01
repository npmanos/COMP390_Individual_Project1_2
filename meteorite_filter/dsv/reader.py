class DSVReader:
    def __init__(self, dsv_path: str, delimiter=',', newline: str | None=None):
        self._file = open(dsv_path, 'r', newline=newline)
        self.delimiter = delimiter
        self._line_num = 0

        if newline is None:
            self._newline = '\n'
        else:
            self._newline = newline

    def __del__(self):
        self._file.close()

    @property
    def line_num(self):
        return self._line_num

    def __iter__(self):
        return self

    def __next__(self) -> list[str]:
        self._line_num += 1
        return next(self._file).rstrip(self._newline).split(self.delimiter)

class DSVDictReader(DSVReader):
    def __init__(
            self,
            dsv_path: str,
            delimiter=',',
            fieldnames: list[str] | None=None,
            type_map: dict | None=None):
        super().__init__(dsv_path, delimiter)

        if fieldnames is None:
            self._fieldnames = super().__next__()
        else:
            self._fieldnames = fieldnames

        self._type_map = type_map

    @property
    def fieldnames(self):
        return self._fieldnames

    def __next__(self) -> dict:
        row_dict = dict(zip(self._fieldnames, super().__next__()))

        if self._type_map is not None:
            for field, type_func in self._type_map.items():
                if row_dict[field] != '':
                    row_dict[field] = type_func(row_dict[field])
                else:
                    row_dict[field] = None #type: ignore

        return row_dict
