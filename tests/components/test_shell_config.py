"""Testing of module config."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest
from hamcrest import assert_that, equal_to, contains_string
from ddt import ddt, data
from spline.components.config import ShellConfig


@ddt
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
        assert_that(config.debug, equal_to(False))
        assert_that(config.strict, equal_to(False))
        assert_that(config.variables, equal_to({}))

    @data({'dry_run': True}, {'debug': True}, {'dry_run': False}, {'item': 'hello'},
          {'env': {'message': 'hello'}}, {'model': {'foo': 123}}, {'title': 'test'},
          {'variables': {'output': 'hello'}}, {'strict': True})
    def test_individual_valid(self, kwargs):
        """Testing to provide mandatory and all optional parameters."""
        # defaults
        final_kwargs = {'script': 'echo "hello world"', 'title': '', 'debug': False, 'strict': False,
                        'dry_run': False, 'item': None, 'env': {}, 'model': {}, 'variables': {}}
        final_kwargs.update(kwargs)

        config = ShellConfig(**final_kwargs)
        for key, value in final_kwargs.items():
            assert_that(key in config.__dict__, equal_to(True))
            assert_that(config.__dict__[key], equal_to(value))

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
