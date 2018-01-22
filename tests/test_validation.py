"""Testing of module validation."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to, is_not
from spline.validation import Validator


class TestValidation(unittest.TestCase):
    """Testing of validation."""

    def test_minimal(self):
        """Testing validation of a minimal pipeline."""
        definition = {'pipeline': [
            {'stage(test)': [
                {'tasks': [
                    {'shell': {
                        'script': 'echo "hello world"'
                    }}
                ]}
            ]}
        ]}
        assert_that(Validator.validate(definition), is_not(equal_to(None)))

    def test_invalid(self):
        """Testing fail."""
        definition = {'pipeline': []}
        assert_that(Validator.validate(definition), equal_to(None))

    def test_shell_complete(self):
        """Testing validation of shell task."""
        definition = {'pipeline': [
            {'stage(test)': [
                {'tasks': [
                    {'shell': {
                        'title': 'print out hello world!',
                        'script': 'echo "hello world"',
                        'tags': ['test'],
                        'with': [1, "hello", 3.1415926535],
                        'variable': 'output'
                    }}
                ]}
            ]}
        ]}
        assert_that(Validator.validate(definition), is_not(equal_to(None)))

    def test_docker_container_complete(self):
        """Testing validation of a Docker container task."""
        definition = {'pipeline': [
            {'stage(test)': [
                {'tasks': [
                    {'docker(container)': {
                        'title': 'print out hello world!',
                        'image': 'centos:7',
                        'mount': True,
                        'remove': True,
                        'background': False,
                        'script': 'echo "hello world"',
                        'tags': ['test'],
                        'with': [1, "hello", 3.1415926535],
                        'variable': 'output'
                    }}
                ]}
            ]}
        ]}
        assert_that(Validator.validate(definition), is_not(equal_to(None)))

    def test_tasks_ordered(self):
        """Testing of ordered tasks."""
        definition = {'pipeline': [
            {'stage(test)': [
                {'tasks(ordered)': [
                    {'shell': {'script': 'echo "hello world 1"'}},
                    {'shell': {'script': 'echo "hello world 2"'}}
                ]}
            ]}
        ]}
        assert_that(Validator.validate(definition), is_not(equal_to(None)))

    def test_tasks_parallel(self):
        """Testing of ordered tasks."""
        definition = {'pipeline': [
            {'stage(test)': [
                {'tasks(parallel)': [
                    {'shell': {'script': 'echo "hello world 1"'}},
                    {'shell': {'script': 'echo "hello world 2"'}}
                ]}
            ]}
        ]}
        assert_that(Validator.validate(definition), is_not(equal_to(None)))

    def test_model(self):
        """Testing validation of model."""
        definition = {
            'model': {
                'count': 3,
                'entries': [1, 'some data', 3.1415],
                'name': 'Agatha Christie',
                'pi': 3.1415926535,
                'author': {'name': 'Hercules Poirot'}
            },
            'pipeline': [
                {'stage(test)': [{'tasks': [{'shell': {'script': 'echo "hello world"'}}]}]}]}
        assert_that(Validator.validate(definition), is_not(equal_to(None)))

    def test_complete_valid_matrix(self):
        """Testing validation of a valid complete matrix."""
        definition = {
            'matrix': [
                {'name': 'Python 2.7.x', 'env': {'PYTHON_VERSION': 'py27'}, 'tags': ['py27']},
                {'name': 'Python 3.5.x', 'env': {'PYTHON_VERSION': 'py35'}, 'tags': ['py35']}
            ],
            'pipeline': [
                {'stage(test)': [{'tasks': [{'shell': {'script': 'echo "hello world"'}}]}]}]}
        assert_that(Validator.validate(definition), is_not(equal_to(None)))
