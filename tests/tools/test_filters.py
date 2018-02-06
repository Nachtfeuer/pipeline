"""Testing of module filter."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to
from spline.tools.filters import render, find_matrix, find_stages


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

    def test_render_failed(self):
        """Testing failure in rendering."""
        # undefined variable 'env' (UndefinedError exception)
        assert_that(render('{{ env.missing }}'), equal_to(None))
        # syntax error (TemplateSyntaxError exception)
        assert_that(render('{% for %}'), equal_to(None))

    def test_find_matrix(self):
        """Testing function find_matrix."""
        assert_that(find_matrix({}), equal_to([]))
        document = {'matrix': [{'name': 'Python 27', 'env': {'PYTHON_VERSION': 'py27'}}]}
        assert_that(find_matrix(document), equal_to(document['matrix']))
        document = {'matrix(ordered)': [{'name': 'Python 27', 'env': {'PYTHON_VERSION': 'py27'}}]}
        assert_that(find_matrix(document), equal_to(document['matrix(ordered)']))
        document = {'matrix(parallel)': [{'name': 'Python 27', 'env': {'PYTHON_VERSION': 'py27'}}]}
        assert_that(find_matrix(document), equal_to(document['matrix(parallel)']))

    def test_find_stages(self):
        """Testing function find_stages."""
        stages = find_stages({'pipeline': [{'stage(Prepare)': 1}, {'stage(Build)': 2}, {'stage(Deploy)': 3}]})
        assert_that(stages, equal_to(['Prepare', 'Build', 'Deploy']))
        stages = find_stages({'pipeline': [{'env': 1}]})
        assert_that(stages, equal_to([]))
