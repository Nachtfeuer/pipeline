"""Testing of module event."""
# pylint: disable=no-self-use, invalid-name
import unittest
from logging import Logger
from mock import patch
from hamcrest import assert_that, equal_to
from spline.tools.event import Event
from spline.tools.logger import NoLogger


class FakeQueue(object):
    """Fake queue for testing."""

    def __init__(self):
        """Initialize queue."""
        self.queue = []

    def put(self, obj):
        """Putting an object into the queue."""
        self.queue.append(obj)

    def __len__(self):
        """Length of the queue."""
        return len(self.queue)


class TestEvent(unittest.TestCase):
    """Testing of class Event."""

    def test_succeeded(self):
        """Testing simple event that was successful."""
        Event.configure(collector_queue=FakeQueue())
        event = Event.create(__name__, stage='Build')
        event.succeeded()
        assert_that(event.status, equal_to('succeeded'))
        assert_that(len(event.information), equal_to(1))
        assert_that(event.information['stage'], equal_to('Build'))
        assert_that(isinstance(event.logger, NoLogger), equal_to(True))
        # timestamps for creation and for finish
        assert_that(len(Event.collector_queue), equal_to(0))

    def test_succeeded_with_report(self):
        """Testing simple event that was successful."""
        Event.configure(collector_queue=FakeQueue())
        event = Event.create(__name__, stage='Build', report='html')
        event.succeeded()
        assert_that(event.status, equal_to('succeeded'))
        assert_that(event.information['report'], equal_to('html'))
        assert_that(event.information['stage'], equal_to('Build'))
        assert_that(isinstance(event.logger, NoLogger), equal_to(True))
        # timestamps for creation and for finish
        assert_that(len(Event.collector_queue), equal_to(2))

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

    def test_configure_wrong_key(self):
        """"Testing unknown config key."""
        with patch('logging.Logger.error') as mocked_logging:
            Event.configure(unknown='foo')
            mocked_logging.assert_called_once_with(
                'Unknown key %s in configure or bad type %s', 'unknown', type(""))
