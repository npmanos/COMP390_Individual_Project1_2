"""
This module contains an interface for output methods and
classes which implement it.
"""

from datetime import datetime as dt
from meteorite_filter.dsv.excel import ExcelDictWriter
from meteorite_filter.dsv.writer import DSVDictWriter
from meteorite_filter.tui.table import TablePrinter

class OutputInterface:
    @staticmethod
    def output(data: list[dict], field: str):
        """
        Interface for output classes.

        Args:
            data (list[dict]): The data to be outputted.
            field (str): The field to be displayed in the output.
        """
        pass


class TerminalOutput(OutputInterface):
    @staticmethod
    def output(data: list[dict], field: str):
        """
        Output the data to the terminal.

        Args:
            data (list[dict]): The data to be outputted.
            field (str): The field to be displayed in the output.
        """
        from meteorite_filter.constants import FILTER_OPTIONS
        table = TablePrinter(('', 'NAME', FILTER_OPTIONS[field]['header']), [(row_no, row['name'], row[field]) for row_no, row in enumerate(data, 1)])
        print()
        print(table)


class TextFileOutput(OutputInterface):
    @staticmethod
    def output(data: list[dict], field: str):
        """
        Output the data to a text file.

        Args:
            data (list[dict]): The data to be outputted.
            field (str): The field to be displayed in the output.
        """
        path = _gen_filename('txt')
        fieldnames = list(data[0].keys())

        writer = DSVDictWriter(path, fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(data)


class ExcelFileOutput(OutputInterface):
    @staticmethod
    def output(data: list[dict], field: str):
        """
        Output the data to an Excel file.

        Args:
            data (list[dict]): The data to be outputted.
            field (str): The field to be displayed in the output.
        """
        path = _gen_filename('xls')
        fieldnames = list(data[0].keys())

        writer = ExcelDictWriter(path, fieldnames)
        writer.writeheader()
        writer.writerows(data)
        writer.save()


def _gen_filename(ext: str) -> str:
    """
    Generate a filename with the given extension.

    Args:
        ext (str): The file extension.

    Returns:
        str: The generated filename.
    """
    return dt.now().strftime(f'%Y-%m-%d_%H_%M_%f.{ext}')
