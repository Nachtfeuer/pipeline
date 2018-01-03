"""Testing of module adapter."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from mock import patch
from hamcrest import assert_that, equal_to
from spline.application import Application
from spline.components.config import ApplicationOptions


class TestApplication(unittest.TestCase):
    """Testing of class Application."""

    def test_init(self):
        """Testing c'tor only."""
        tags = 'prepare,build'
        matrix_tags = "py27,py35"
        options = ApplicationOptions(definition='fake.yaml', matrix_tags=matrix_tags, tags=tags)
        application = Application(options)
        assert_that(application.options.tags, equal_to(['prepare', 'build']))
        assert_that(application.options.matrix_tags, equal_to(['py27', 'py35']))
        assert_that(application.options.validate_only, equal_to(False))
        assert_that(application.options.logging_config, equal_to(''))

    def test_find_matrix(self):
        """Testing functin Application.find_matrix."""
        assert_that(Application.find_matrix({}), equal_to(None))
        document = {'matrix': [{'name': 'Python 27', 'env': {'PYTHON_VERSION': 'py27'}}]}
        assert_that(Application.find_matrix(document), equal_to(document['matrix']))
        document = {'matrix(ordered)': [{'name': 'Python 27', 'env': {'PYTHON_VERSION': 'py27'}}]}
        assert_that(Application.find_matrix(document), equal_to(document['matrix(ordered)']))
        document = {'matrix(parallel)': [{'name': 'Python 27', 'env': {'PYTHON_VERSION': 'py27'}}]}
        assert_that(Application.find_matrix(document), equal_to(document['matrix(parallel)']))

    def test_invalidate_document(self):
        """Testing invalid document."""
        application = Application(ApplicationOptions(definition='data/invalid.yaml'))
        with patch('sys.exit') as mocked_exit:
            path = os.path.dirname(__file__)
            application.validate_document(os.path.join(path, "data/invalid.yaml"))
            mocked_exit.assert_called_once_with(1)

    def test_validate_document(self):
        """Testing valid document."""
        application = Application(ApplicationOptions(definition='data/simple.yaml'))
        application.validate_only = True
        with patch('sys.exit') as mocked_exit:
            path = os.path.dirname(__file__)
            document = application.validate_document(os.path.join(path, "data/simple.yaml"))
            mocked_exit.assert_not_called()
            assert_that(isinstance(document, dict), equal_to(True))

    def test_run_matrix(self):
        """Testing method Application.run_matrix."""
        mdef = [{'name': 'test1', 'env': {'message': 'hello 1'}},
                {'name': 'test2', 'env': {'message': 'hello 2'}}]
        pdef = {
            'pipeline': [{
                'stage(Test)': [{
                    'tasks': [{
                        'shell': {'script': 'echo "{{ env.message }}"'}
                    }]
                }]
            }]
        }

        application = Application(ApplicationOptions(definition='fake.yaml'))
        result = application.run_matrix(mdef, pdef)

        assert_that(result['success'], equal_to(True))
        output = [line for line in result['output'] if line.find('hello') >= 0]
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('hello 1'))
        assert_that(output[1], equal_to('hello 2'))
