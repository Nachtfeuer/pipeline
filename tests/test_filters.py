"""Testing of module filter."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to
from spline.tools.filters import render


class TestFilters(unittest.TestCase):
    """Testing of Jinja filters."""

    def test_render_simple(self):
        """Testing simple rendering without usage nested templates."""
        model = {"message": "hello world!"}
        given = render("{{model.message}}", model=model)
        assert_that(given, equal_to('hello world!'))

    def test_render_nested(self):
        """Testing using nested templates."""
        model = {"message": "hello world!", "template": "{{ model.message }}"}
        given = render("{{ model.template|render(model=model) }}", model=model)
        assert_that(given, equal_to('hello world!'))
