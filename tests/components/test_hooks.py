"""Testing of module hooks."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to
from spline.components.hooks import Hooks


class TestHooks(unittest.TestCase):
    """Testing of class Hooks."""

    def test_simple(self):
        """Testing hooks without a document."""
        hooks = Hooks()
        assert_that(hooks.cleanup, equal_to(''))

    def test_document(self):
        """Testing hooks with a document."""
        hooks = Hooks({'hooks': {'cleanup': {}}})
        assert_that(hooks.cleanup, equal_to(''))
        hooks = Hooks({'hooks': {'cleanup': {'script': 'echo "hello"'}}})
        assert_that(hooks.cleanup, equal_to('echo "hello"'))
