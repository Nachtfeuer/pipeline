"""Testing of module condition."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to
from spline.tools.condition import Condition


class TestInitialCondition(unittest.TestCase):
    """Testing of initial conditions before rendering."""

    def test_empty_condition(self):
        """An empty condition is valid."""
        assert_that(Condition.is_valid(''), equal_to(True))

    def test_str_eq_str(self):
        """Comparing two strings; environment variable with a constant."""
        # compact version (env variables)
        assert_that(Condition.is_valid(
            '"{{ env.BRANCH_NAME }}" == "master"'), equal_to(True))
        # more spaces around are allowed (env variables)
        assert_that(Condition.is_valid(
            ' "{{ env.BRANCH_NAME }}"  ==  "master" '), equal_to(True))
        # compact version (tasks variables)
        assert_that(Condition.is_valid(
            '"{{ variables.cpu_count }}" == "6"'), equal_to(True))
        # more spaces around are allowed (tasks variables)
        assert_that(Condition.is_valid(
            ' "{{ variables.cpu_count }}"  ==  "6" '), equal_to(True))

    def test_num_eq_num(self):
        """Comparing two strings; environment variable with a constant."""
        # compact version (env variables)
        assert_that(Condition.is_valid(
            '{{ variables.cpu_count }} == 1'), equal_to(True))
        # more spaces around are allowed (env variables)
        assert_that(Condition.is_valid(
            '  {{ variables.cpu_count }}  ==  1  '), equal_to(True))
        # compact version (tasks variables)

    def test_str_in_str_list(self):
        """Testing format for checking string to be in a list of strings."""
        # compact ver sion (env variables)
        assert_that(Condition.is_valid(
            '"{{ env.BRANCH_NAME }}" in ["dev", "prod"]'), equal_to(True))
        # more spaces around are allowed (env variables)
        assert_that(Condition.is_valid(
            '  "{{ env.BRANCH_NAME }}"  in  [ "dev", "prod" ] '), equal_to(True))
        # compact version (task variables)
        assert_that(Condition.is_valid(
            '"{{ variables.cpu_count }}" in ["1", "2"]'), equal_to(True))

    def test_str_not_equal_str(self):
        """Comparing two strings to be not equal."""
        # compact version
        assert_that(Condition.is_valid(
            'not "{{ env.BRANCH_NAME }}" == "master"'), equal_to(True))
        # more spaces around are allowed
        assert_that(Condition.is_valid(
            ' not  "{{ env.BRANCH_NAME }}"  ==  "master" '), equal_to(True))
        # compact version
        assert_that(Condition.is_valid(
            'not "{{ variables.BRANCH_NAME }}" == "master"'), equal_to(True))
        # more spaces around are allowed
        assert_that(Condition.is_valid(
            ' not  "{{ variables.BRANCH_NAME }}"  ==  "master" '), equal_to(True))

    def test_str_not_in_str_list(self):
        """Testing format for checking string to be in a list of strings."""
        # compact ver sion (env variables)
        assert_that(Condition.is_valid(
            '"{{ env.BRANCH_NAME }}" not in ["dev", "prod"]'), equal_to(True))
        # more spaces around are allowed (env variables)
        assert_that(Condition.is_valid(
            '  "{{ env.BRANCH_NAME }}"  not in  [ "dev",  "prod" ] '), equal_to(True))
        # compact version (task variables)
        assert_that(Condition.is_valid(
            '"{{ variables.cpu_count }}" not in ["1", "2"]'), equal_to(True))

    def test_invalid(self):
        """Testing invalid conditions."""
        # expect str == str - comparison but quotes are missing on the right side
        assert_that(Condition.is_valid(
            '"{{ env.BRANCH_NAME }}" == master'), equal_to(False))
        # expect str == str - comparison but quotes are missing on the left side
        assert_that(Condition.is_valid(
            '{{ env.BRANCH_NAME }} == "master"'), equal_to(False))
        # expect not str == str - comparison but quotes are missing on the right side
        assert_that(Condition.is_valid(
            'not "{{ env.BRANCH_NAME }}" == master'), equal_to(False))
        # currently "env" and "variables" are supported only
        assert_that(Condition.is_valid(
            '"{{ foo.BRANCH_NAME }}" == master'), equal_to(False))
        # strings search in a list of integer doesn't work
        assert_that(Condition.is_valid(
            '"{{ variables.cpu_count }}" in [1, 2]'), equal_to(False))
        # mixed types are now allowed
        assert_that(Condition.is_valid(
            '"{{ variables.cpu_count }}" in [1, "2"]'), equal_to(False))
