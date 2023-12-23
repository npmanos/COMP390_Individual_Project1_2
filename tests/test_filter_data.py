from io import StringIO
from pytest import fixture, MonkeyPatch, CaptureFixture
from meteorite_filter.filter_data import *
from meteorite_filter.output import TerminalOutput, TextFileOutput


@fixture
def mock_term_output(monkeypatch: MonkeyPatch):
    @staticmethod
    def mock_output(data: list[dict], field: str):
        print(f'TerminalOutput selected. data: {data}, field: {field}')

    monkeypatch.setitem(OUTPUT_OPTIONS['terminal'], "func", mock_output)


@fixture
def mock_text_output(monkeypatch: MonkeyPatch):
    @staticmethod
    def mock_output(data: list[dict], field: str):
        print(f'TextFileOutput selected. data: {data}, field: {field}')

    monkeypatch.setitem(OUTPUT_OPTIONS['text'], "func", mock_output)


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
\x1B[39m> \x1B[32m\x1B[39m
'''


    def test_select_terminal(self, mock_term_output, write_stdin, capfd: CaptureFixture[str]):
        write_stdin('1\n')

        field = 'mass (g)'
        select_output(self.data, field)

        assert capfd.readouterr().out == f'{self.expected_menu}TerminalOutput selected. data: {self.data}, field: {field}\n'


    def test_select_text(self, mock_text_output, write_stdin, capfd: CaptureFixture[str]):
        write_stdin('2\n')

        field = 'year'
        select_output(self.data, field)
        
        assert capfd.readouterr().out == f'{self.expected_menu}TextFileOutput selected. data: {self.data}, field: {field}\n'

