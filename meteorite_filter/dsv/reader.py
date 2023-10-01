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
