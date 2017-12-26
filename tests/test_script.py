"""Testing of module script."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest
from hamcrest import assert_that, equal_to
from spline.components.config import ShellConfig
from spline.components.script import Script


class TestScript(unittest.TestCase):
    """Testing of class Script."""

    def test_python(self):
        """Testing using Python."""
        config = ShellConfig(script='''print("name={{model.name}}, version={{env.version}}")''',
                             title='test python', model={'name': 'test'}, env={'version': '1.0'})
        script = Script.creator({'type': 'python'}, config)
        output = list(script.process())
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to("name=test, version=1.0"))
