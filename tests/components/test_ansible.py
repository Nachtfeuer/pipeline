"""Testing of class Ansible."""
# pylint: disable=no-self-use, invalid-name
import unittest
from mock import patch, call
from hamcrest import assert_that, contains_string, equal_to
from spline.components.ansible import Ansible
from spline.components.config import ShellConfig


class TestAnsible(unittest.TestCase):
    """Testing of class Ansible."""

    def test_creator_dry_run(self):
        """Testing Ansible but dry run mode only."""
        script = '''---\n- hosts: all\n  tasks:\n    - name: Print a message\n      dbg: msg=hello'''
        config = ShellConfig(script=script, model={}, env={}, dry_run=True)
        ansible = Ansible.creator({'inventory': '''[all]\n127.0.0.1''', 'limit': ''}, config)
        output = list(ansible.process())

        assert_that(output[-4], contains_string("rm -f ansible.inventory"))
        assert_that(output[-3], contains_string("rm -f ansible.playbook"))

    def test_creator_no_run(self):
        """Testing Ansible but dry run mode only."""
        inventory = '''[all]\n127.0.0.1'''
        script = '''---\n- hosts: all\n  tasks:\n    - name: Print a message\n      dbg: msg=hello'''
        config = ShellConfig(script=script, model={}, env={}, dry_run=False)

        with patch('spline.components.ansible.write_temporary_file') as mocked_write_temporary_file:
            mocked_write_temporary_file.return_value = ['first', 'second']
            Ansible.creator({'inventory': inventory, 'limit': ''}, config)

            assert_that(mocked_write_temporary_file.mock_calls, equal_to([
                call(script, 'ansible-play-', '.yaml'),
                call(inventory, prefix='ansible-inventory-')
            ]))
