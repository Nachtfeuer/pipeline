"""Testing of module event."""
# pylint: disable=no-self-use, invalid-name
import unittest
from logging import Logger
from hamcrest import assert_that, equal_to
from spline.tools.event import Event
from spline.tools.logger import NoLogger
from spline.tools.report import Collector


class TestHooks(unittest.TestCase):
    """Testing of class Event."""

    def test_succeed(self):
        """Testing simple event that was successful."""
        Collector().clear()
        event = Event.create(__name__)
        event.succeeded()
        assert_that(event.status, equal_to('succeeded'))
        assert_that(event.information, equal_to({}))
        assert_that(isinstance(event.logger, NoLogger), equal_to(True))
        assert_that(Collector().count_matrixes(), equal_to(0))

    def test_succeed_with_information(self):
        """Testing simple event that was successful."""
        event = Event.create(__name__)
        event.succeeded(stage='build')
        assert_that(event.status, equal_to('succeeded'))
        assert_that(event.information, equal_to({'stage': 'build'}))

    def test_configure_logging_enabled(self):
        """Testing configuration of logging."""
        assert_that(Event.is_logging_enabled, equal_to(False))
        Event.configure(is_logging_enabled=True)
        assert_that(Event.is_logging_enabled, equal_to(True))
        Event.configure(is_logging_enabled=False)
        assert_that(Event.is_logging_enabled, equal_to(False))

    def test_logging_enabled(self):
        """Testing instation of a concrete logger."""
        Event.configure(is_logging_enabled=True)
        event = Event.create(__name__)
        assert_that(isinstance(event.logger, Logger), equal_to(True))
        Event.configure(is_logging_enabled=False)

    def test_stage_succeeded(self):
        """Testing event to update collector for a stage."""
        Collector().clear()
        event = Event.create(__name__, stage='Build')
        event.succeeded()
        assert_that(Collector().count_matrixes(), equal_to(1))
        assert_that(Collector().get_stage('default', 'Build').status, equal_to('succeeded'))
        assert_that(len(Collector().get_stage('default', 'Build').events), equal_to(2))
