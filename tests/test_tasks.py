"""Testing of class Logger."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to

from spline.components.tasks import Tasks, worker
from spline.components.bash import Bash
from spline.components.hooks import Hooks
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

        assert_that(result['success'], equal_to(True))
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

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('hello1'))
        assert_that(output[1], equal_to('hello2'))

    def test_failed_ordered(self):
        """Testing cleanup when a task has failed (ordered)."""
        hooks = Hooks()
        hooks.cleanup = '''echo cleanup hello'''
        pipeline = FakePipeline(hooks=hooks)
        tasks = Tasks(pipeline, parallel=False)

        definition = [{'shell': {'script': '''exit 123'''}},
                      {'shell': {'script': '''echo hello'''}}]
        result = tasks.process(definition)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(False))
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('cleanup hello'))

    def test_failed_parallel(self):
        """Testing cleanup when a task has failed (parallel)."""
        hooks = Hooks()
        hooks.cleanup = '''echo cleanup 123'''
        pipeline = FakePipeline(hooks=hooks)
        tasks = Tasks(pipeline, parallel=True)

        definition = [{'shell': {'script': '''exit 123'''}},
                      {'shell': {'script': '''echo hello'''}}]
        result = tasks.process(definition)
        output = sorted([line for line in result['output']
                         if line.find("hello") >= 0 or line.find("cleanup") >= 0])

        assert_that(result['success'], equal_to(False))
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('cleanup 123'))
        assert_that(output[1], equal_to('hello'))

    def test_tags_ordered(self):
        """Testing for filtering of tags."""
        pipeline = FakePipeline()
        tasks = Tasks(pipeline, parallel=False)

        definition = [{'shell': {'script': '''echo hello1''', 'tags': ['first']}},
                      {'shell': {'script': '''echo hello2''', 'tags': ['second']}}]

        pipeline.data.tags = ['first']
        result = tasks.process(definition)
        output = [line for line in result['output'] if line.find("hello") >= 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello1'))

        pipeline.data.tags = ['second']
        result = tasks.process(definition)
        output = [line for line in result['output'] if line.find("hello") >= 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello2'))

    def test_env_ordered(self):
        """Testing environment variables (ordered)."""
        pipeline = FakePipeline()
        tasks = Tasks(pipeline, parallel=False)

        definition = [{'env': {'message': 'hello'}},
                      {'shell': {'script': '''echo "1:{{env.message}}"'''}},
                      {'shell': {'script': '''echo "2:$message"'''}}]
        result = tasks.process(definition)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('1:hello'))
        assert_that(output[1], equal_to('2:hello'))

    def test_worker(self):
        """Testing worker used by class Tasks for parallel execution."""
        data = {'creator': Bash.__name__,
                'entry': {'script': '''echo "{{model.mode}}:{{env.message}}"'''},
                'env': {'message': 'hello'}, 'model': {'mode': 'test'}}
        result = worker(data)
        output = [line for line in result['output'] if line.find("hello") >= 0]
        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('test:hello'))
