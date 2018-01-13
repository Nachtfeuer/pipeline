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
        stage_item = CollectorStage(stage='build', status='started')

        assert_that(stage_item.stage, equal_to('build'))
        assert_that(stage_item.status, equal_to('started'))
        assert_that(len(stage_item.events), equal_to(0))

    def test_add(self):
        """Testing addding event information."""
        timestamp = int(time.time())
        information = {'step': 'compile'}

        stage_item = CollectorStage(stage='build', status='started')
        stage_item.add(timestamp, information)

        assert_that(len(stage_item.events), equal_to(1))
        assert_that(stage_item.events[0]['timestamp'], equal_to(timestamp))
        assert_that(stage_item.events[0]['information'], equal_to(information))

    def test_missing_mandatory(self):
        """Testing missing mandatory parameter."""
        try:
            CollectorStage()
            self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            assert_that(str(exception), equal_to("Missing keys: 'stage', 'status'"))

    def test_add_invalid_timestamp(self):
        """Testing add method with invalid timestamp."""
        try:
            stage_item = CollectorStage(stage='build', status='started')
            stage_item.add("hello", information={'step': 'compile'})
            self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            assert_that(str(exception),
                        equal_to("Key 'timestamp' error:\n'hello' should be instance of 'int'"))

    def test_add_invalid_information(self):
        """Testing add method with invalid information."""
        try:
            stage_item = CollectorStage(stage='build', status='started')
            stage_item.add(int(time.time()), "hello")
            self.assertFalse("RuntimeError expected")
        except RuntimeError as exception:
            assert_that(str(exception),
                        equal_to("Key 'information' error:\n'hello' should be instance of 'dict'"))
