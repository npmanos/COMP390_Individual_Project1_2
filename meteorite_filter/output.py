from datetime import datetime as dt
from dsv.writer import DSVDictWriter
from tui.table import TablePrinter

class OutputInterface:
    @staticmethod
    def output(data: list[dict], field: str):
        pass


class TerminalOutput(OutputInterface):
    @staticmethod
    def output(data: list[dict], field: str):
        from constants import FILTER_OPTIONS
        table = TablePrinter(('', 'NAME', FILTER_OPTIONS[field]['header']), [(row_no, row['name'], row[field]) for row_no, row in enumerate(data, 1)])
        print()
        print(table)


class TextFileOutput(OutputInterface):
    @staticmethod
    def output(data: list[dict], field: str):
        path = dt.now().strftime('%Y-%m-%d_%H_%M_%f.txt')
        fieldnames = list(data[0].keys())

        writer = DSVDictWriter(path, fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(data)
