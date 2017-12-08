"""Testing of class Bash."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from mock import patch
from spline.components.bash import Bash
from hamcrest import assert_that, equal_to


class TestBash(unittest.TestCase):
    """Testing of class Bash."""

    def test_script_only(self):
        """Testing simple bash script."""
        bash = Bash('''echo "hello"''')
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello'))

    def test_using_custom_env_vars(self):
        """Testing using user defined environment variables."""
        bash = Bash('''echo "foo=${foo}"''', env={'foo': 'some foo'})
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('foo=some foo'))

    def test_templ_using_custom_env_vars(self):
        """Testing using user defined environment variables."""
        bash = Bash('''echo "foo={{ env.foo }}"''', env={'foo': 'some foo'})
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('foo=some foo'))

    def test_templ_using_model(self):
        """Testing using model data via Jinja templating."""
        bash = Bash('''echo "foo={{ model.foo }}"''', model={'foo': 'some model foo'})
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('foo=some model foo'))

    def test_creator_complete(self):
        """Testing creator function using model data end env. vars via Jinja templating."""
        bash = Bash.creator({'script': '''echo "{{ env.foo }}-{{ model.foo }}"''', 'title': 'test'},
                            model={'foo': 'model foo'}, env={'foo': 'env foo'})
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('env foo-model foo'))

    def test_failed_exit_not_zero(self):
        """testing normal failed bash script."""
        bash = Bash('''exit 1''')
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(0))
        assert_that(bash.exit_code, equal_to(1))

    def test_external_bash_script(self):
        """Testing of an external bash script."""
        bash = Bash('''{{ env.tests }}/scripts/hello.sh''', env={'tests': os.path.dirname(__file__)})
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('hello'))

    def test_oserror(self):
        """Testing exception."""
        bash = Bash('''echo "hello"''')
        with patch('subprocess.Popen') as mocked_popen:
            mocked_popen.side_effect = OSError('Exception: popen has failed')
            output = [line for line in bash.process() if len(line) > 0]

            assert_that(len(output), equal_to(1))
            assert_that(output[0], equal_to('Exception: popen has failed'))
            assert_that(bash.exit_code, equal_to(1))

    def test_nested_templ_using_model(self):
        """Testing using model data via Jinja templating."""
        bash = Bash('''echo "foo={{ model.template|render(model=model) }}"''',
                    model={'foo': 'some nested foo', 'template': '{{ model.foo }}'})
        output = [line for line in bash.process() if len(line) > 0]
        assert_that(len(output), equal_to(1))
        assert_that(output[0], equal_to('foo=some nested foo'))
