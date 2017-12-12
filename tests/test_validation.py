"""Testing of module validation."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from spline.tools.validation import validate_schema
from hamcrest import assert_that, equal_to


class TestValidation(unittest.TestCase):
    """Testing of validation."""

    def test_simple(self):
        """Testing most simple pipeline."""
        schema_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spline/schema.yaml')
        source_file = os.path.join(os.path.dirname(__file__), 'data/simple.yaml')
        assert_that(validate_schema(source_file, schema_file), equal_to(True))

    def test_invalid(self):
        """Testing invalid pipeline syntax."""
        schema_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spline/schema.yaml')
        source_file = os.path.join(os.path.dirname(__file__), 'data/invalid.yaml')
        assert_that(validate_schema(source_file, schema_file), equal_to(False))
