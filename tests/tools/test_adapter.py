"""Testing of module adapter."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to
from spline.tools.adapter import Adapter


class TestAdapter(unittest.TestCase):
    """Testing of class Adapter."""

    def test_simple(self):
        """Testing simple usage."""
        adapted = Adapter({'a': 10, 'b': {'c': 20}})
        assert_that(adapted.a, equal_to(10))
        assert_that(adapted.b.c, equal_to(20))

    def test_length(self):
        """Testing __len__ method."""
        adapted = Adapter({'a': 10, 'b': {'c': 20}})
        assert_that(len(adapted), equal_to(2))

    def test_str(self):
        """Testing __str__ method."""
        data = {'a': 10, 'b': {'c': 20}}
        adapted = Adapter(data)
        assert_that(str(adapted), equal_to(str(data)))

    def test_callable(self):
        """Testing callable attribute"""
        data = {'a': 10, 'b': {'c': 20}}
        adapted = Adapter(data)
        assert_that(list(adapted.items()), equal_to(list(data.items())))

    def test_unknown_field_or_callable(self):
        """Testing unknown field or callable."""
        data = {'a': 10, 'b': {'c': 20}}
        adapted = Adapter(data)
        assert_that(adapted.foo, equal_to(None))
