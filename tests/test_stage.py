"""Testing of class Stage."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to

from spline.pipeline import PipelineData
from spline.components.stage import Stage


class FakePipeline(object):
    """Fake pipeline class for tests."""

    def __init__(self, tags=None, hooks=None):
        """Initialization of fake pipeline."""
        self.data = PipelineData(self, tags, hooks)
        self.model = {}


class TestStage(unittest.TestCase):
    """Testing of class Stage."""

    def test_two_tasks_blocks(self):
        """Testing with two tasks blocks only."""
        pipeline = FakePipeline()
        stage = Stage(pipeline, 'test')

        definition = [{'tasks': [{'shell': {'script': '''echo tasks1:hello1'''}},
                                 {'shell': {'script': '''echo tasks1:hello2'''}}]},
                      {'tasks': [{'shell': {'script': '''echo tasks2:hello1'''}},
                                 {'shell': {'script': '''echo tasks2:hello2'''}}]}]
        result = stage.process(definition)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(4))
        assert_that(output[0], equal_to('tasks1:hello1'))
        assert_that(output[1], equal_to('tasks1:hello2'))
        assert_that(output[2], equal_to('tasks2:hello1'))
        assert_that(output[3], equal_to('tasks2:hello2'))

    def test_environemnt_variables(self):
        """Testing with environment variables."""
        pipeline = FakePipeline()
        stage = Stage(pipeline, 'test')

        definition = [{'env': {'message': 'hello 1.0'}},
                      {'tasks': [{'shell': {'script': '''echo "$message"'''}},
                                 {'env': {'message': 'hello 1.1'}},
                                 {'shell': {'script': '''echo "$message"'''}}]},
                      {'env': {'message': 'hello 2.0'}},
                      {'tasks': [{'shell': {'script': '''echo "$message"'''}},
                                 {'env': {'message': 'hello 2.1'}},
                                 {'shell': {'script': '''echo "$message"'''}}]}]

        result = stage.process(definition)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(4))
        assert_that(output[0], equal_to('hello 1.0'))
        assert_that(output[1], equal_to('hello 1.1'))
        assert_that(output[2], equal_to('hello 2.0'))
        assert_that(output[3], equal_to('hello 2.1'))
