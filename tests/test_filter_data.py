from io import StringIO
from pytest import fixture, MonkeyPatch, CaptureFixture, mark
import pytest
from meteorite_filter.filter_data import *


@fixture
def mock_outputs(monkeypatch: MonkeyPatch):
    @staticmethod
    def mock_term_output(data: list[dict], field: str):
        print(f'TerminalOutput selected. data: {data}, field: {field}')

    @staticmethod
    def mock_text_output(data: list[dict], field: str):
        print(f'TextFileOutput selected. data: {data}, field: {field}')

    monkeypatch.setitem(OUTPUT_OPTIONS['terminal'], "func", mock_term_output)
    monkeypatch.setitem(OUTPUT_OPTIONS['text'], "func", mock_text_output)


@fixture
def write_stdin(monkeypatch: MonkeyPatch):
    stdin_sim = StringIO()

    def _make_stdin_stringio(mock_input: str):
        stdin_sim = StringIO(mock_input)
        monkeypatch.setattr('sys.stdin', stdin_sim)
        return stdin_sim

    yield _make_stdin_stringio

    monkeypatch.undo()
    stdin_sim.close()


class TestSelectOutput:
    data = [
        {
            'Counties': None, 'GeoLocation': '"(54.81667, 61.11667)"', 'States': None, 'fall': 'Fell', 'id': 57165,
            'mass (g)': 100000.0, 'name': 'Chelyabinsk', 'nametype': 'Valid', 'recclass': 'LL5',
            'reclat': 54.81667, 'reclong': 61.11667, 'year': 2013
        },
        {
            'Counties': None, 'GeoLocation': '"(0.0, 0.0)"', 'States': None, 'fall': 'Found', 'id': 57166,
            'mass (g)': 30.0, 'name': 'Northwest Africa 7755', 'nametype': 'Valid', 'recclass': 'Martian (shergottite)',
            'reclat': 0.0, 'reclong': 0.0, 'year': 2013
        },
        {
            'Counties': None, 'GeoLocation': '"(0.0, 0.0)"', 'States': None, 'fall': 'Found', 'id': 57258,
            'mass (g)': 46.2, 'name': 'Northwest Africa 7812', 'nametype': 'Valid', 'recclass': 'Angrite',
            'reclat': 0.0, 'reclong': 0.0, 'year': 2013
        },
        {
            'Counties': None, 'GeoLocation': '"(0.0, 0.0)"', 'States': None, 'fall': 'Found', 'id': 57268,
            'mass (g)': 45.8, 'name': 'Northwest Africa 7822', 'nametype': 'Valid', 'recclass': 'Achondrite-ung',
            'reclat': 0.0, 'reclong': 0.0, 'year': 2013
        },
        {
            'Counties': None, 'GeoLocation': '"(0.0, 0.0)"', 'States': None, 'fall': 'Found', 'id': 57420,
            'mass (g)': 916.0, 'name': 'Northwest Africa 7855', 'nametype': 'Valid', 'recclass': 'H4',
            'reclat': 0.0, 'reclong': 0.0, 'year': 2013
        }
    ]

    expected_menu = '''\x1B[36mHow would you like to output the filtered results?\x1B[39m
1 - Display on screen
2 - Save to a text (.txt) file
q - Quit the application
\x1B[36mType a letter or number to select your choice
\x1B[39m> \x1B[32m\x1B[39m'''

    @mark.parametrize('sim_input,field,output_option', [('1\n', 'mass (g)', 'TerminalOutput'), ('1\n', 'year', 'TerminalOutput'), ('2\n', 'mass (g)', 'TextFileOutput'), ('2\n', 'year', 'TextFileOutput')])
    def test_select_valid_output(self, sim_input: str, field: str, output_option: str, mock_outputs, write_stdin, capfd: CaptureFixture[str]):
        write_stdin(sim_input)
        select_output(self.data, field)
        assert capfd.readouterr().out == f'{self.expected_menu}\n{output_option} selected. data: {self.data}, field: {field}\n'


    @mark.parametrize('field', [('mass (g)'), ('year')])
    def test_quit(self, field: str, mock_outputs, write_stdin, capfd: CaptureFixture[str]):
        with pytest.raises(SystemExit):
            write_stdin('q')
            select_output(self.data, field)

        with pytest.raises(SystemExit):
            write_stdin('Q')
            select_output(self.data, field)

        with pytest.raises(SystemExit):
            write_stdin('?q')
            select_output(self.data, field)

        with pytest.raises(SystemExit):
            write_stdin('?Q')
            select_output(self.data, field)


    @mark.parametrize('bad_input', ['4', '0', '-1', 'show', 'SHOW', '1 Show', '!', '?', 'b', 'B'])
    def test_bad_input(self, bad_input: str, mock_outputs, monkeypatch: MonkeyPatch, write_stdin, capfd: CaptureFixture[str]):
        write_stdin(f'{bad_input}\n\n1\n')
        expected_error = '''\x1B[1m\x1B[31m
ERROR! Invalid option. Please enter the number or letter of your selection.
\x1B[39m\x1B[22m
\x1B[1mPress any key to continue...
\x1B[22m'''

        select_output(self.data, 'mass (g)')
        assert capfd.readouterr().out == f'{self.expected_menu}{expected_error}{self.expected_menu}\nTerminalOutput selected. data: {self.data}, field: mass (g)\n'
