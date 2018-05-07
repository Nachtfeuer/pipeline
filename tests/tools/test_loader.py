"""Testing of Loader class (for yaml)."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from hamcrest import assert_that, equal_to, calling, raises

from spline.tools.loader import Loader
from spline.tools.adapter import Adapter
from spline.tools.filters import render


class TestLoader(unittest.TestCase):
    """Testing of Loader class (for yaml)."""

    def test_valid_loader(self):
        """Testing Loader used the right way."""
        yaml_file = os.path.join(os.path.dirname(__file__), 'data/loader_main.yaml')
        document = Adapter(Loader.load(yaml_file))
        render(document.some, model=document.model)
        assert_that(render(document.some, model=document.model), equal_to('hello world!'))

    def test_missing_main_file(self):
        """Testing the case does the main file doesn't exist."""
        assert_that(calling(Loader.load).with_args('file-that-does-not-exist'),
                    raises(RuntimeError, "File .* doesn't exist!"))

    def test_missing_include_file(self):
        """Testing missing include file."""
        existing_yaml_file = os.path.join(os.path.dirname(__file__),
                                          'data/loader_error_missing_include_file.yaml')
        assert_that(calling(Loader.load).with_args(existing_yaml_file),
                    raises(RuntimeError, "Include file .* doesn't exist!"))

    def test_not_supported_include(self):
        """Testing not supported include on list of files."""
        existing_yaml_file = os.path.join(os.path.dirname(__file__),
                                          'data/loader_error_not_supported_include.yaml')
        assert_that(calling(Loader.load).with_args(existing_yaml_file),
                    raises(RuntimeError, "Not supported !include on type .*"))
