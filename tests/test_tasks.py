"""Testing of class Logger."""
# pylint: disable=no-self-use, invalid-name
import logging
import unittest
import multiprocessing
import codecs
from io import StringIO
from hamcrest import assert_that, equal_to

from spline.components.tasks import Tasks
from spline.pipeline import PipelineData


class FakePipeline(object):
    """Fake pipeline class for tests."""

    def __init__(self, tags=None, hooks=None):
        """Initialization of fake pipeline."""
        self.data = PipelineData(self, tags, hooks)
        self.model = {}


class TestTasks(unittest.TestCase):
    """Testing of class Tasks."""

    def test_two_tasks_ordered(self):
        """Testing with two task only (ordered)."""
        pipeline = FakePipeline()
        tasks = Tasks(pipeline, parallel=False)

        f = StringIO()
        ch = logging.StreamHandler(f)
        logging.getLogger().addHandler(ch)

        definition = [{'shell': {'script': '''echo hello1'''}},
                      {'shell': {'script': '''echo hello2'''}}]
        tasks.process(definition)

        output = [line for line in f.getvalue().split('\n') if line.find("hello") >= 0]
        logging.getLogger().removeHandler(ch)
        f.close()

        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to(' | hello1'))
        assert_that(output[1], equal_to(' | hello2'))
