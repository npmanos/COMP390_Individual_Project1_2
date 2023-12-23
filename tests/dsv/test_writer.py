from pathlib import Path
import pytest
from meteorite_filter.dsv.writer import *

class TestDSVWriter:
    text_row = ['this', 'is', 'a', 'test']
    num_row = [4, 7.4, -4, -7.4]
    none_row = [None, None, None, None]
    mixed_row = ['this', 4, None, -7.4]
    rows = [text_row, num_row, none_row, mixed_row]

    def test_format_row(self, tmp_path):
        path: Path = tmp_path / 'test_format_row.tsv'
        writer = DSVWriter(str(path), '\t')

        assert writer._format_row(self.text_row) == 'this\tis\ta\ttest\n'
        assert writer._format_row(self.num_row) == '4\t7.4\t-4\t-7.4\n'
        assert writer._format_row(self.none_row) == '\t\t\t\n'
        assert writer._format_row(self.mixed_row) == 'this\t4\t\t-7.4\n'


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
        assert 'this\tis\ta\ttest\n4\t7.4\t-4\t-7.4\n\t\t\t\nthis\t4\t\t-7.4\n' == path.read_text()


    def test_writerows(self, tmp_path):
        path: Path = tmp_path / 'test_writerows.tsv'
        writer = DSVWriter(str(path), '\t')

        writer.writerows(self.rows)
        assert 'this\tis\ta\ttest\n4\t7.4\t-4\t-7.4\n\t\t\t\nthis\t4\t\t-7.4\n' == path.read_text()


    def test_delims(self, tmp_path):
        comma_path = tmp_path / 'test_delim_comma.tsv'
        DSVWriter(str(comma_path)).writerows(self.rows)
        assert 'this,is,a,test\n4,7.4,-4,-7.4\n,,,\nthis,4,,-7.4\n' == comma_path.read_text()

        tab_path = tmp_path / 'test_delim_tab.tsv'
        DSVWriter(str(tab_path), '\t').writerows(self.rows)
        assert 'this\tis\ta\ttest\n4\t7.4\t-4\t-7.4\n\t\t\t\nthis\t4\t\t-7.4\n' == tab_path.read_text()

        pipe_path = tmp_path / 'test_delim_pipe.tsv'
        DSVWriter(str(pipe_path), '|').writerows(self.rows)
        assert 'this|is|a|test\n4|7.4|-4|-7.4\n|||\nthis|4||-7.4\n' == pipe_path.read_text()

