"""Testing of module loc."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from hamcrest import assert_that, equal_to, ends_with
from spline.tools.loc.application import Application, main
from spline.tools.adapter import Adapter


class TestLoc(unittest.TestCase):
    """Testing of spline loc tool."""

    def test_loc_application(self):
        """Testing application."""
        loc = Application(**self.default_options())
        loc.run()
        assert_that(len(loc.results), equal_to(1))
        assert_that(Adapter(loc.results[0]).file, ends_with('fifty_fifty.py'))
        assert_that(Adapter(loc.results[0]).loc, equal_to(2))
        assert_that(Adapter(loc.results[0]).com, equal_to(2))

    def test_loc_main(self):
        """Testing main."""
        loc = main(**self.default_options())
        assert_that(len(loc.results), equal_to(1))
        assert_that(Adapter(loc.results[0]).file, ends_with('fifty_fifty.py'))
        assert_that(Adapter(loc.results[0]).loc, equal_to(2))
        assert_that(Adapter(loc.results[0]).com, equal_to(2))

    @staticmethod
    def default_options():
        """Provide default application options."""
        return {
            'path': os.path.join(os.path.dirname(__file__), 'data'),
            'threshold': 0.5,
            'show_all': True
        }
