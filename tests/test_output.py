from pathlib import Path
from pytest import MonkeyPatch
from meteorite_filter.output import TerminalOutput, TextFileOutput
from meteorite_filter.tui.table import TablePrinter

class TestTerminalOutput:
    def test_output(self, capfd):
        data = [
            {'name': 'Meteorite 1', 'mass (g)': '-1.0'},
            {'name': 'Meteorite 2', 'mass (g)': '0.0'},
            {'name': 'Meteorite 3', 'mass (g)': '1.0'}
        ]
        field = 'mass (g)'

        TerminalOutput.output(data, field)

        captured = capfd.readouterr()
        expected_output = '\n' + str(TablePrinter(('', 'NAME', 'MASS (g)'), [(1, 'Meteorite 1', '-1.0'), (2, 'Meteorite 2', '0.0'), (3, 'Meteorite 3', '1.0')])) + '\n'
        assert captured.out == expected_output

        data = [
            {'name': 'Meteorite 1', 'year': '1999'},
            {'name': 'Meteorite 2', 'year': '2010'},
            {'name': 'Meteorite 3', 'year': '2023'}
        ]
        field = 'year'

        TerminalOutput.output(data, field)

        captured = capfd.readouterr()
        expected_output = '\n' + str(TablePrinter(('', 'NAME', 'YEAR'), [(1, 'Meteorite 1', '1999'), (2, 'Meteorite 2', '2010'), (3, 'Meteorite 3', '2023')])) + '\n'
        assert captured.out == expected_output


class TestTextFileOutput:
    def test_output(self, tmp_path: Path, monkeypatch: MonkeyPatch):
        data = [
            {'name': 'Meteorite 1', 'mass (g)': '-1.0'},
            {'name': 'Meteorite 2', 'mass (g)': '0.0'},
            {'name': 'Meteorite 3', 'mass (g)': '1.0'}
        ]
        field = 'mass (g)'

        path: Path = tmp_path / 'TestTextFileOutput'
        path.mkdir()
        path = path / 'test_output.txt'
        
        monkeypatch.setattr('meteorite_filter.output._gen_filename', lambda *args, **kargs: str(path))

        TextFileOutput.output(data, field)

        assert path.read_text() == 'name\tmass (g)\nMeteorite 1\t-1.0\nMeteorite 2\t0.0\nMeteorite 3\t1.0\n'
