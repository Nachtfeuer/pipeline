"""Testing of Jinja2 rendering."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to

from spline.components.bash import Bash
from spline.components.tasks import Tasks, worker
from spline.components.hooks import Hooks
from spline.components.config import ApplicationOptions, ShellConfig
from spline.pipeline import PipelineData


class FakePipeline(object):
    """Fake pipeline class for tests."""

    def __init__(self, hooks=None):
        """Initialization of fake pipeline."""
        self.data = PipelineData(hooks)
        self.model = {}
        self.options = ApplicationOptions(definition='fake.yaml')
        self.variables = {}


class TestRender(unittest.TestCase):
    """Testing of render function."""

    def test_render_no_raw(self):
        """Testing with a task only (ordered)."""
        pipeline = FakePipeline()
        tasks = Tasks(pipeline, parallel=False)

        document = [{'env': {'a': '''hello1'''}},
                    {'shell': {'script': '''echo {{ env.a }}''', 'when': ''}}]
        result = tasks.process(document)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello1'))

    def test_render_one_raw(self):
        """Testing with a task only (ordered)."""
        pipeline = FakePipeline()
        tasks = Tasks(pipeline, parallel=False)

        document = [{'env': {'a': '''hello1'''}},
                    {'shell': {'script': '''echo "{% raw %}{{ env.a }}{% endraw %}"''', 'when': ''}}]
        result = tasks.process(document)
        output = [line for line in result['output'] if line.find("{{") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('{{ env.a }}'))

    def test_render_one_env_raw(self):
        """Testing with a task only (ordered)."""
        pipeline = FakePipeline()
        tasks = Tasks(pipeline, parallel=False)

        document = [{'env': {'a': '''{% raw %}{{ hello1 }}{% endraw %}'''}},
                    {'shell': {'script': '''echo "{{ env.a }}"''', 'when': ''}}]
        result = tasks.process(document)
        output = [line for line in result['output'] if line.find("{{") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('{{ hello1 }}'))

    def test_render_one_env_self_referencing_raw(self):
        """Testing with a task only (ordered)."""
        pipeline = FakePipeline()
        tasks = Tasks(pipeline, parallel=False)

        document = [{'env': {'a': '''{% raw %}{{ hello1 }}{% endraw %}''', 'b': "{{ env.a }}"}},
                    {'shell': {'script': '''echo "{{ env.b }}"''', 'when': ''}}]
        result = tasks.process(document)
        output = [line for line in result['output'] if line.find("{{") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('{{ hello1 }}'))

    def test_render_script_only(self):
        """Testing rendering of a simple bash script."""
        bash = Bash(ShellConfig(script='''echo {% raw %}"hello"{% endraw %}'''))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello'))

