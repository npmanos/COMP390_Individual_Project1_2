from pathlib import Path
import pytest
from meteorite_filter.dsv.writer import *

class TestDSVWriter:
    text_row = ['this', 'is', 'a', 'test']
    num_row = [4, 7.4, -4, -7.4]
    none_row = [None, None, None, None]
    mixed_row = ['this', 0, None, 0.0]
    rows = [text_row, num_row, none_row, mixed_row]

    def test_format_row(self, tmp_path):
        path: Path = tmp_path / 'test_format_row.tsv'
        writer = DSVWriter(str(path), '\t')

        assert writer._format_row(self.text_row) == 'this\tis\ta\ttest\n'
        assert writer._format_row(self.num_row) == '4\t7.4\t-4\t-7.4\n'
        assert writer._format_row(self.none_row) == '\t\t\t\n'
        assert writer._format_row(self.mixed_row) == 'this\t0\t\t0.0\n'


    def test_writerow(self, tmp_path):
        path: Path = tmp_path / 'test_writerow.tsv'
        writer = DSVWriter(str(path), '\t')

        writer.writerow(self.text_row)
        assert 'this\tis\ta\ttest\n' == path.read_text()

        writer.writerow(self.num_row)
        assert 'this\tis\ta\ttest\n4\t7.4\t-4\t-7.4\n' == path.read_text()

        writer.writerow(self.none_row)
        assert 'this\tis\ta\ttest\n4\t7.4\t-4\t-7.4\n\t\t\t\n' == path.read_text()

        writer.writerow(self.mixed_row)
        assert 'this\tis\ta\ttest\n4\t7.4\t-4\t-7.4\n\t\t\t\nthis\t0\t\t0.0\n' == path.read_text()


    def test_writerows(self, tmp_path):
        path: Path = tmp_path / 'test_writerows.tsv'
        writer = DSVWriter(str(path), '\t')

        writer.writerows(self.rows)
        assert 'this\tis\ta\ttest\n4\t7.4\t-4\t-7.4\n\t\t\t\nthis\t0\t\t0.0\n' == path.read_text()


    def test_delims(self, tmp_path):
        comma_path = tmp_path / 'test_delim_comma.csv'
        comma_writer = DSVWriter(str(comma_path))
        assert comma_writer.delimiter == ','
        comma_writer.writerows(self.rows)
        assert 'this,is,a,test\n4,7.4,-4,-7.4\n,,,\nthis,0,,0.0\n' == comma_path.read_text()

        tab_path = tmp_path / 'test_delim_tab.tsv'
        tab_writer = DSVWriter(str(tab_path), '\t')
        assert tab_writer.delimiter == '\t'
        tab_writer.writerows(self.rows)
        assert 'this\tis\ta\ttest\n4\t7.4\t-4\t-7.4\n\t\t\t\nthis\t0\t\t0.0\n' == tab_path.read_text()

        pipe_path = tmp_path / 'test_delim_pipe.txt'
        pipe_writer = DSVWriter(str(pipe_path), '|')
        assert pipe_writer.delimiter == '|'
        pipe_writer.writerows(self.rows)
        assert 'this|is|a|test\n4|7.4|-4|-7.4\n|||\nthis|0||0.0\n' == pipe_path.read_text()


class TestDSVDictWriter:
    fieldnames = ['string', 'int', 'none', 'float']
    header = 'string\tint\tnone\tfloat\n'

    rows: list[dict] = [
        {
            'string': 'this is text',
            'int': 47,
            'none': None,
            'float': 7.4
        },
        {
            'string': 'this is also text',
            'int': -74,
            'none': None,
            'float': -4.7
        },
        {
            'string': None,
            'int': None,
            'none': None,
            'float': None
        },
        {
            'string': 'even more text',
            'int': 0,
            'none': None,
            'float': 0.0
        }
    ]
    all_rows = '''this is text\t47\t\t7.4
this is also text\t-74\t\t-4.7
\t\t\t
even more text\t0\t\t0.0
'''

    def test_writeheader(self, tmp_path):
        path: Path = tmp_path / 'TestDSVDictWriter'
        path.mkdir()
        path = path / 'test_writeheader.tsv'

        writer = DSVDictWriter(str(path), self.fieldnames, '\t')
        assert writer.fieldnames == self.fieldnames

        writer.writeheader()
        assert path.read_text() == self.header


    def test_writerow(self, tmp_path):
        path: Path = tmp_path / 'TestDSVDictWriter'
        path.mkdir()
        path = path / 'test_writerow.tsv'

        writer = DSVDictWriter(str(path), self.fieldnames, '\t')

        writer.writerow(self.rows[0])
        assert path.read_text() == 'this is text\t47\t\t7.4\n'

        writer.writerow(self.rows[1])
        assert path.read_text() == 'this is text\t47\t\t7.4\nthis is also text\t-74\t\t-4.7\n'

        writer.writerow(self.rows[2])
        assert path.read_text() == 'this is text\t47\t\t7.4\nthis is also text\t-74\t\t-4.7\n\t\t\t\n'

        writer.writerow(self.rows[3])
        assert path.read_text() == 'this is text\t47\t\t7.4\nthis is also text\t-74\t\t-4.7\n\t\t\t\neven more text\t0\t\t0.0\n'

        too_few_fields = {
            'string': 'foo',
            'int': 47,
            'none': None
        }
        with pytest.raises(ValueError):
            writer.writerow(too_few_fields)
        
        too_many_fields = {
            'string': 'bar',
            'int': 74,
            'none': None,
            'float': 4.7,
            'extra': True
        }
        with pytest.raises(ValueError):
            writer.writerow(too_many_fields)


    def test_writerows(self, tmp_path):
        path: Path = tmp_path / 'TestDSVDictWriter'
        path.mkdir()
        path = path / 'test_writerows.tsv'

        writer = DSVDictWriter(str(path), self.fieldnames, '\t')

        writer.writerows(self.rows)
        assert path.read_text() == self.all_rows

        too_few_fields = self.rows + [{
            'string': 'foo',
            'int': 47,
            'none': None
        }]

        with pytest.raises(ValueError):
            writer.writerows(too_few_fields)

        too_many_fields = self.rows + [{
            'string': 'bar',
            'int': 74,
            'none': None,
            'float': 4.7,
            'extra': True
        }]

        with pytest.raises(ValueError):
            writer.writerows(too_many_fields)

    def test_full(self, tmp_path):
        path: Path = tmp_path / 'TestDSVDictWriter'
        path.mkdir()
        path = path / 'test_full.tsv'

        writer = DSVDictWriter(str(path), self.fieldnames, '\t')

        writer.writeheader()
        writer.writerows(self.rows)
        assert path.read_text() == self.header + self.all_rows
        