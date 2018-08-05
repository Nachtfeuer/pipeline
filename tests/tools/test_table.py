"""Testing of module table."""
# pylint: disable=no-self-use
import unittest

from hamcrest import assert_that, equal_to
from spline.tools.table import calculate_columns, calculate_row_format, pprint
from spline.tools.stream import stdout_redirector


class TestTable(unittest.TestCase):
    """Testing of module table."""

    def test_calulate_columns(self):
        """Testing of spline.tools.table.calculate_columns function."""
        data = self.default_test_data()
        columns = calculate_columns(data)

        assert_that(len(columns), equal_to(3))
        assert_that(columns['first name'], equal_to(10))  # column title
        assert_that(columns['surname'], equal_to(8))  # column title and value
        assert_that(columns['character'], equal_to(14))  # value

    def test_calculate_row_format(self):
        """Testing of spline.tools.table.calculate_row_format function."""
        data = self.default_test_data()
        columns = calculate_columns(data)
        row_format = calculate_row_format(columns, list(sorted(columns.keys())))
        expected_row_format = '|%(character)-14s|%(first name)-10s|%(surname)-8s|'
        assert_that(row_format, equal_to(expected_row_format))

    def test_pprint(self):
        data = self.default_test_data()
        with stdout_redirector() as stream:
            pprint(data, list(sorted(data[0].keys())))
            content = stream.getvalue()
            lines = content.split('\n')
            separator = '|--------------|----------|--------|'

            assert_that(len(lines), equal_to(7))
            assert_that(lines[0], equal_to(separator))
            assert_that(lines[1], equal_to('|Character     |First Name|Surname |'))
            assert_that(lines[2], equal_to(separator))
            assert_that(lines[3], equal_to('|Hercule Poirot|Agatha    |Christie|'))
            assert_that(lines[4], equal_to('|Nero Wolfe    |Rex       |Stout   |'))
            assert_that(lines[5], equal_to(separator))

    @staticmethod
    def default_test_data():
        """
        Provide test data.
        Returns:
            list: each entry a dictionatory representing the row data.
        """
        return [
            {'first name': 'Agatha', 'surname': 'Christie', 'character': 'Hercule Poirot'},
            {'first name': 'Rex', 'surname': 'Stout', 'character': 'Nero Wolfe'},
        ]
