"""Testing of module query."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest

from hamcrest import assert_that, equal_to
from spline.tools.query import Select


class TestQuery(unittest.TestCase):
    """Testing of module query."""

    def test_select_where(self):
        """Testing of filter function."""
        result = Select(1, 2, 3, 4).where(lambda n: n % 2 == 0).build()
        assert_that(result, equal_to([2, 4]))
        result = Select([1, 2, 3, 4]).where(lambda n: n % 2 == 0).build()
        assert_that(result, equal_to([2, 4]))
        result = Select((1, 2, 3, 4)).where(lambda n: n % 2 == 0).build()
        assert_that(result, equal_to([2, 4]))

    def test_select_transform(self):
        """Testing of transform function."""
        result = Select(1, 2, 3, 4).transform(lambda n: n * 3).build()
        assert_that(result, equal_to([3, 6, 9, 12]))
