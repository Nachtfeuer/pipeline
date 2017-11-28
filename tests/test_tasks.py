"""Testing of class Logger."""
# pylint: disable=no-self-use, invalid-name
import unittest
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

        definition = [{'shell': {'script': '''echo hello1'''}},
                      {'shell': {'script': '''echo hello2'''}}]
        result = tasks.process(definition)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('hello1'))
        assert_that(output[1], equal_to('hello2'))

    def test_two_tasks_parallel(self):
        """Testing with two task only (parallel)."""
        pipeline = FakePipeline()
        tasks = Tasks(pipeline, parallel=True)

        definition = [{'shell': {'script': '''echo hello1'''}},
                      {'shell': {'script': '''echo hello2'''}}]
        result = tasks.process(definition)
        output = sorted([line for line in result['output'] if line.find("hello") >= 0])

        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('hello1'))
        assert_that(output[1], equal_to('hello2'))
