class DSVReader:
    def __init__(self, dsv_path: str, delimiter=','):
        self._file = open(dsv_path, 'r')
        self.delimiter = delimiter
        self._line_num = 0
    
    def __del__(self):
        self._file.close()

    @property
    def line_num(self):
        return self._line_num
    
    def __next__(self) -> list[str]:
        self._line_num += 1
        return self._file.readline().split(self.delimiter)

