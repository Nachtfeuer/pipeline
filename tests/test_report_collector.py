"""Testing of module report."""
# pylint: disable=no-self-use, invalid-name, redundant-unittest-assert
import unittest
import time

from hamcrest import assert_that, equal_to
from spline.tools.report.collector import Collector, CollectorUpdate


class TestReportCollector(unittest.TestCase):
    """Testing of class Collector."""

    def test_singleton(self):
        """Testing collector to be a singleton."""
        collector_a = Collector()
        collector_b = Collector()
        assert_that(collector_a, equal_to(collector_b))
        assert_that(id(collector_a), equal_to(id(collector_b)))

    def test_update_first(self):
        """Testing creating a stage."""
        Collector().clear()
        item = CollectorUpdate(
            stage='Build', status='started',
            timestamp=int(time.time()), information={'language': 'java'})
        Collector().update(item)

        stage = Collector().get_stage('default', 'Build')
        assert_that(stage.stage, equal_to('Build'))

        assert_that(Collector().count_matrixes(), equal_to(1))
        assert_that(Collector().count_stages('default'), equal_to(1))

    def test_update_existing(self):
        """Testing updating an existing stage."""
        Collector().clear()
        item = CollectorUpdate(
            stage='Build', status='started',
            timestamp=int(time.time()), information={'language': 'java'})
        Collector().update(item)

        item = CollectorUpdate(
            stage='Build', status='succeeded',
            timestamp=int(time.time()))
        Collector().update(item)

        assert_that(Collector().count_matrixes(), equal_to(1))
        assert_that(Collector().count_stages('default'), equal_to(1))

        stage = Collector().get_stage('default', 'Build')
        assert_that(stage.stage, equal_to('Build'))
        assert_that(stage.status, equal_to('succeeded'))
        assert_that(len(stage.events), equal_to(2))

    def test_not_existing_stage(self):
        """Testing get_stage for a stage that does not exist."""
        Collector().clear()
        item = CollectorUpdate(
            stage='Build', status='started',
            timestamp=int(time.time()), information={'language': 'java'})
        Collector().update(item)

        stage = Collector().get_stage('default', 'Deploy')
        assert_that(stage, equal_to(None))

    def test_not_existing_matrix(self):
        """Testing get_stage for a matrix that does not exist."""
        Collector().clear()
        item = CollectorUpdate(
            stage='Build', status='started',
            timestamp=int(time.time()), information={'language': 'java'})
        Collector().update(item)

        stage = Collector().get_stage('test', 'Build')
        assert_that(stage, equal_to(None))
