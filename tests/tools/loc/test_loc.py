"""Testing of module loc."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from mock import patch, call
from hamcrest import assert_that, equal_to, ends_with
from spline.tools.loc.application import Application, main
from spline.tools.adapter import Adapter


class TestLoc(unittest.TestCase):
    """Testing of spline loc tool."""

    def test_loc_application(self):
        """Testing application."""
        loc = Application(**self.default_options())
        loc.run()
        self.verify_results(loc)

    def test_loc_main(self):
        """Testing main."""
        with patch('sys.exit') as mocked_exit:
            loc = main(**self.default_options())
            assert_that(mocked_exit.mock_calls, equal_to([call(1)]))
            self.verify_results(loc)

    def verify_results(self, loc):
        """Testing for expected results."""
        results = sorted(loc.results, key=lambda entry: Adapter(entry).file)
        assert_that(len(results), equal_to(len(self.expected_results())))

        for idx, expected in enumerate(self.expected_results()):
            assert_that(Adapter(results[idx]).file, ends_with(expected.filename))
            assert_that(Adapter(results[idx]).loc, equal_to(expected.loc))
            assert_that(Adapter(results[idx]).com, equal_to(expected.com))

    @staticmethod
    def expected_results():
        """Expected test results."""
        return [
            Adapter({'filename': 'com_only.py', 'loc': 0, 'com': 4}),
            Adapter({'filename': 'fifty_fifty.py', 'loc': 2, 'com': 2}),
            Adapter({'filename': 'more_com_than_loc.py', 'loc': 2, 'com': 3}),
            Adapter({'filename': 'more_loc_than_com.py', 'loc': 4, 'com': 1})
        ]

    @staticmethod
    def default_options():
        """Provide default application options."""
        return {
            'path': [os.path.join(os.path.dirname(__file__), 'data')],
            'threshold': 0.5,
            'show_all': True
        }
