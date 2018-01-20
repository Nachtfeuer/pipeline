"""Testing of module report."""
# pylint: disable=no-self-use
import unittest
import os
import time

from mock import patch
from spline.tools.report.collector import Collector, CollectorUpdate


class TestReportCollector(unittest.TestCase):
    """Testing of class Store."""

    TIMEOUT = 5  # timeout of 5 seconds

    def test_start_and_stop(self):
        """Testing start and stop mechanism."""
        collector = Collector()

        with patch("logging.Logger.info") as mocked_logging:
            collector.queue.put(None)
            collector.run()
            mocked_logging.assert_called_once_with("Stopping collector process ...")

    def test_generate(self):
        """Testing generating call."""
        collector = Collector()
        collector.queue.put(CollectorUpdate(stage='Build', status='started',
                                            timestamp=int(time.time()), information={'language': 'java'}))
        collector.queue.put(None)
        # the generate is imported in the collectory.py (that's why)
        with patch('spline.tools.report.collector.generate') as mocked_generate:
            collector.run()
            mocked_generate.assert_called_once_with(collector.store, 'html', os.getcwd())
