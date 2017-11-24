"""Testing of class Container."""
# pylint: disable=no-self-use, invalid-name
import unittest
from spline.components.docker import Container
from hamcrest import assert_that, equal_to


class TestContainer(unittest.TestCase):
    """Testing of class Container (docker)."""

    def test_script_only(self):
        """Testing simple Docker container script."""
        container = Container('''echo "hello"''')
        output = [line for line in container.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello'))

    def test_creator_complete(self):
        """Testing creator function using model data end env. vars via Jinja templating."""
        container = Container.creator(
            {'script': '''echo "{{ env.foo }}-{{ model.foo }}"''', 'title': 'test'},
            model={'foo': 'model foo'}, env={'foo': 'env foo'})
        output = [line for line in container.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('env foo-model foo'))
