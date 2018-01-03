"""Testing of module config."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest
from hamcrest import assert_that, equal_to, contains_string
from spline.components.config import ShellConfig


class TestShellConfig(unittest.TestCase):
    """Testing of class ShellConfig."""

    def test_minimal_valid(self):
        """Testing to provide mandatory parameters only."""
        config = ShellConfig(script='echo "hello world"')
        assert_that(config.script, equal_to('echo "hello world"'))
        assert_that(config.title, equal_to(''))
        assert_that(config.model, equal_to({}))
        assert_that(config.env, equal_to({}))
        assert_that(config.item, equal_to(None))
        assert_that(config.dry_run, equal_to(False))

    def test_complete_valid(self):
        """Testing to provide mandatory and all optional parameters."""
        config = ShellConfig(script='echo "hello world"', title='test', model={'foo': 123},
                             env={'bar': "xyz"}, item='hello', dry_run=True)
        assert_that(config.script, equal_to('echo "hello world"'))
        assert_that(config.title, equal_to('test'))
        assert_that(config.model, equal_to({'foo': 123}))
        assert_that(config.env, equal_to({'bar': "xyz"}))
        assert_that(config.item, equal_to('hello'))
        assert_that(config.dry_run, equal_to(True))

    def test_missing_mandatory(self):
        """Testing invalid parameter."""
        try:
            ShellConfig()
            self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            assert_that(str(exception), equal_to("Missing keys: 'script'"))

    def test_undefined_parameter(self):
        """Testing undefined parameter."""
        try:
            ShellConfig(script='echo "hello world"', XYZ='foo and bar')
            self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            assert_that(str(exception), contains_string("Wrong keys 'XYZ'"))
