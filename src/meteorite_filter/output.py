from datetime import datetime as dt
from meteorite_filter.dsv.excel import ExcelDictWriter
from meteorite_filter.dsv.writer import DSVDictWriter
from meteorite_filter.tui.table import TablePrinter

class OutputInterface:
    @staticmethod
    def output(data: list[dict], field: str):
        pass


class TerminalOutput(OutputInterface):
    @staticmethod
    def output(data: list[dict], field: str):
        from meteorite_filter.constants import FILTER_OPTIONS
        table = TablePrinter(('', 'NAME', FILTER_OPTIONS[field]['header']), [(row_no, row['name'], row[field]) for row_no, row in enumerate(data, 1)])
        print()
        print(table)


class TextFileOutput(OutputInterface):
    @staticmethod
    def output(data: list[dict], field: str):
        path = _gen_filename('txt')
        fieldnames = list(data[0].keys())

        writer = DSVDictWriter(path, fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(data)


class ExcelFileOutput(OutputInterface):
    @staticmethod
    def output(data: list[dict], field: str):
        path = _gen_filename('xls')
        fieldnames = list(data[0].keys())

        writer = ExcelDictWriter(path, fieldnames)
        writer.writeheader()
        writer.writerows(data)
        writer.save()


def _gen_filename(ext: str) -> str:
    return dt.now().strftime(f'%Y-%m-%d_%H_%M_%f.{ext}')
