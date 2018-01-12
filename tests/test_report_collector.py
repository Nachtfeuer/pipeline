"""Testing of module report."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest
import time

from hamcrest import assert_that, equal_to
from spline.tools.report import Collector, CollectorUpdate


class TestReportCollector(unittest.TestCase):
    """Testing of class Collector."""

    def test_singleton(self):
        """Testing collector to be a singleton."""
        collector_a = Collector()
        collector_b = Collector()
        assert_that(collector_a, equal_to(collector_b))
        assert_that(id(collector_a), equal_to(id(collector_b)))

    def test_stage(self):
        """Testing update defining a start of a stage."""
        Collector().clear()
        item = CollectorUpdate(
            stage='Build', status='started',
            timestamp=int(time.time()), information={'language': 'java'})
        Collector().update(item)

        stage = Collector().get_stage('default', 'Build')
        assert_that(stage.stage, equal_to('Build'))

        assert_that(Collector().count_matrixes(), equal_to(1))
        assert_that(Collector().count_stages('default'), equal_to(1))
