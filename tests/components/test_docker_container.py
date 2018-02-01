"""Testing of class Container."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from hamcrest import assert_that, equal_to, matches_regexp
from spline.components.docker import Container
from spline.components.config import ShellConfig


@unittest.skipIf('INSIDE_DOCKER' in os.environ and os.environ['INSIDE_DOCKER'] == 'yes',
                 "Docker based tests cannot run inside Docker")
class TestContainer(unittest.TestCase):
    """Testing of class Container (docker)."""

    def test_script_only(self):
        """Testing simple Docker container script."""
        container = Container(ShellConfig(script='''echo "hello"'''))
        output = [line for line in container.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello'))

    def test_creator_complete(self):
        """Testing creator function using model data end env. vars via Jinja templating."""
        config = ShellConfig(script='''echo "test:{{ env.foo }}-{{ model.foo }}"''',
                             title='test', model={'foo': 'model foo'}, env={'foo': 'env foo'})
        container = Container.creator({}, config)
        output = [line for line in container.process() if line.startswith("test:")]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('test:env foo-model foo'))

    def test_pipeline_bash_file_variable(self):
        """Testing the injected variable representing the script."""
        config = ShellConfig(script='''echo "PIPELINE_BASH_FILE=$PIPELINE_BASH_FILE"''', model={}, env={})
        container = Container.creator({}, config)

        output = [line for line in container.process() if line.lower().find("pipeline") >= 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], matches_regexp('PIPELINE_BASH_FILE=/root/scripts/pipeline-script-.*.sh'))

        config = ShellConfig(script='echo "PIPELINE_BASH_FILE=$PIPELINE_BASH_FILE"', model={}, env={})
        container = Container.creator({}, config)

        output = [line for line in container.process() if line.lower().find("pipeline") >= 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], matches_regexp('PIPELINE_BASH_FILE=/root/scripts/pipeline-script-.*.sh'))
