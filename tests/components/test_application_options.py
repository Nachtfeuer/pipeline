"""Testing of module config."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest
from ddt import ddt, data
from hamcrest import assert_that, equal_to
from spline.components.config import ApplicationOptions


@ddt
class TestApplicationOptions(unittest.TestCase):
    """Testing of class ApplicationOptions."""

    def test_minimal_valid(self):
        """Testing to provide mandatory parameters only."""
        options = ApplicationOptions(definition='fake.yml')
        assert_that(options.definition, equal_to('fake.yml'))
        assert_that(options.matrix_tags, equal_to([]))
        assert_that(options.tags, equal_to([]))
        assert_that(options.logging_config, equal_to(''))
        assert_that(options.event_logging, equal_to(False))
        assert_that(options.validate_only, equal_to(False))
        assert_that(options.dry_run, equal_to(False))
        assert_that(options.debug, equal_to(False))
        assert_that(options.report, equal_to('off'))

    def test_missing_mandatory(self):
        """Testing missing mandatory parameter."""
        try:
            ApplicationOptions()
            self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            assert_that(str(exception), equal_to("Missing keys: 'definition'"))

    @data(('off', True), ('json', True), ('html', True), ('foo', False))
    def test_report(self, item):
        """Testing missing mandatory parameter."""
        try:
            options = {'definition': 'fake.yml'}
            options.update({'report': item[0]})
            ApplicationOptions(**options)
            if not item[1]:
                self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            if item[1]:
                self.assertFalse("Unexpected exception %s" % exception)
