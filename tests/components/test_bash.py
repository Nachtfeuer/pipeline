# -*- coding: utf-8 -*-
"""Testing of class Bash."""
# pylint: disable=no-self-use, invalid-name, too-many-public-methods
import os
import unittest
from mock import patch
from hamcrest import assert_that, equal_to, matches_regexp
from spline.components.bash import Bash
from spline.components.config import ShellConfig


class TestBash(unittest.TestCase):
    """Testing of class Bash."""

    def test_script_only(self):
        """Testing simple bash script."""
        bash = Bash(ShellConfig(script='''echo "hello"'''))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello'))

    def test_using_custom_env_vars(self):
        """Testing using user defined environment variables."""
        bash = Bash(ShellConfig(script='''echo "foo=${foo}"''', env={'foo': 'some foo'}))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('foo=some foo'))

    def test_templ_using_custom_env_vars(self):
        """Testing using user defined environment variables."""
        bash = Bash(ShellConfig(script='''echo "foo={{ env.foo }}"''', env={'foo': 'some foo'}))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('foo=some foo'))

    def test_templ_using_model(self):
        """Testing using model data via Jinja templating."""
        config = ShellConfig(script='''echo "foo={{ model.foo }}"''', model={'foo': 'some model foo'})
        bash = Bash(config)
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('foo=some model foo'))

    def test_creator_complete(self):
        """Testing creator function using model data end env. vars via Jinja templating."""
        config = ShellConfig(script='''echo "{{ env.foo }}-{{ model.foo }}"''',
                             title='test', model={'foo': 'model foo'}, env={'foo': 'env foo'})
        bash = Bash.creator(None, config)
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('env foo-model foo'))

    def test_failed_exit_not_zero(self):
        """testing normal failed bash script."""
        bash = Bash(ShellConfig(script='''exit 1'''))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(0))
        assert_that(bash.exit_code, equal_to(1))

    def test_external_bash_script(self):
        """Testing of an external bash script."""
        bash = Bash(ShellConfig(script='''{{ env.tests }}/scripts/hello.sh''',
                                env={'tests': os.path.dirname(__file__)}))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello'))

    def test_oserror(self):
        """Testing exception."""
        bash = Bash(ShellConfig(script='''echo "hello"'''))
        with patch('subprocess.Popen') as mocked_popen:
            mocked_popen.side_effect = OSError('Exception: popen has failed')
            output = [line for line in bash.process() if len(line) > 0]

            assert_that(len(output), equal_to(1))
            assert_that(output[0], equal_to('Exception: popen has failed'))
            assert_that(bash.exit_code, equal_to(1))

    def test_render_error(self):
        """Testing error in jinja2 rendering."""
        bash = Bash(ShellConfig(script='''echo "{{ foo.bar }}"'''))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(0))
        assert_that(bash.success, equal_to(False))
        assert_that(bash.exit_code, equal_to(0))

    def test_nested_templ_using_model(self):
        """Testing using model data via Jinja templating."""
        bash = Bash(ShellConfig(script='''echo "foo={{ model.template|render(model=model) }}"''',
                                model={'foo': 'some nested foo', 'template': '{{ model.foo }}'}))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('foo=some nested foo'))

    def test_pipeline_bash_file_variable(self):
        """Testing the injected variable representing the script."""
        bash = Bash(ShellConfig(script='''echo "PIPELINE_BASH_FILE=$PIPELINE_BASH_FILE"'''))
        output = [line for line in bash.process() if line.lower().find("script") > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], matches_regexp('PIPELINE_BASH_FILE=/tmp/pipeline-script-.*.sh'))

        bash = Bash(ShellConfig(script='''echo "PIPELINE_BASH_FILE={{ env.PIPELINE_BASH_FILE }}"'''))
        output = [line for line in bash.process() if line.lower().find("script") > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], matches_regexp('PIPELINE_BASH_FILE=/tmp/pipeline-script-.*.sh'))

    def test_dry_run(self):
        """Testing simple bash script in dry run mode."""
        bash = Bash(ShellConfig(script='''echo "hello"''', dry_run=True))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('''#!/bin/bash'''))
        assert_that(output[1], equal_to('''echo "hello"'''))

    def test_get_temporary_scripts_path(self):
        """Testing temporary scripts path."""
        bash = Bash(ShellConfig(script='''echo "hello"''', temporary_scripts_path='/tmp'))
        assert_that(bash.get_temporary_scripts_path(), equal_to('/tmp'))

        bash = Bash(ShellConfig(script='''echo "hello"''', temporary_scripts_path=''))
        assert_that(bash.get_temporary_scripts_path(), equal_to(None))

        bash = Bash(ShellConfig(script='''echo "hello"''', temporary_scripts_path='/tmp/does-not-exist'))
        assert_that(bash.get_temporary_scripts_path(), equal_to(None))

    def test_render_bash_options(self):
        """Testing rendering Bash options."""
        bash = Bash(ShellConfig(script='''echo "hello"'''))
        assert_that(bash.render_bash_options(), equal_to(''))
        bash = Bash(ShellConfig(script='''echo "hello"''', debug=True))
        assert_that(bash.render_bash_options(), equal_to('set -x\n'))
        bash = Bash(ShellConfig(script='''echo "hello"''', strict=True))
        assert_that(bash.render_bash_options(), equal_to('set -euo pipefail\n'))

    def test_internal_flag(self):
        """Testing simple bash script with internal flag."""
        bash = Bash(ShellConfig(script='''echo "hello"''', internal=True))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello'))

        bash = Bash(ShellConfig(script='''echo "hello"''', internal=True, dry_run=True))
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('#!/bin/bash'))
        assert_that(output[1], equal_to('echo "hello"'))
