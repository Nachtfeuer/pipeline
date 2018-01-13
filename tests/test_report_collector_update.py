"""Testing of module report."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest
import time

from hamcrest import assert_that, equal_to
from spline.tools.report import CollectorUpdate


class TestReportCollectorUpdate(unittest.TestCase):
    """Testing of class CollectorUpdate."""

    def test_minimal_valid(self):
        """Testing to provide mandatory parameters only."""
        timestamp = int(time.time())
        update_item = CollectorUpdate(stage='build', timestamp=timestamp, status='started')

        assert_that(update_item.matrix, equal_to('default'))
        assert_that(update_item.stage, equal_to('build'))
        assert_that(update_item.timestamp, equal_to(timestamp))
        assert_that(update_item.status, equal_to('started'))
        assert_that(update_item.information, equal_to({}))

    def test_complete_valid(self):
        """Testing providing all parameter."""
        timestamp = int(time.time())
        update_item = CollectorUpdate(stage='build', timestamp=timestamp, status='started',
                                      matrix='Python 2.7', information={'parallel': True})

        assert_that(update_item.matrix, equal_to('Python 2.7'))
        assert_that(update_item.stage, equal_to('build'))
        assert_that(update_item.timestamp, equal_to(timestamp))
        assert_that(update_item.status, equal_to('started'))
        assert_that(update_item.information, equal_to({'parallel': True}))

    def test_missing_mandatory(self):
        """Testing missing mandatory parameter."""
        try:
            CollectorUpdate()
            self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            assert_that(str(exception), equal_to("Missing keys: 'stage', 'status', 'timestamp'"))
