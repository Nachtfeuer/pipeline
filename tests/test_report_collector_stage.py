"""Testing of module report."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest
import time

from hamcrest import assert_that, equal_to
from spline.tools.report import CollectorStage


class TestReportCollectorStage(unittest.TestCase):
    """Testing of class CollectorStage."""

    def test_valid(self):
        """Testing a valid example."""
        item = CollectorStage(stage='build', status='started')

        assert_that(item.stage, equal_to('build'))
        assert_that(item.status, equal_to('started'))
        assert_that(len(item.events), equal_to(0))

    def test_missing_mandatory(self):
        """Testing missing mandatory parameter."""
        try:
            CollectorStage()
            self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            assert_that(str(exception), equal_to("Missing keys: 'stage', 'status'"))
