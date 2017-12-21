"""Testing of module adapter."""
# pylint: disable=no-self-use, invalid-name
import unittest
from mock import patch
from hamcrest import assert_that, equal_to
from spline.application import Application


class TestApplication(unittest.TestCase):
    """Testing of class Application."""

    def test_init(self):
        """Testing c'tor only."""
        definition = "pipeline.yaml"
        tags = 'prepare,build'
        matrix_tags = "py27,py35"
        application = Application(definition=definition, matrix_tags=matrix_tags,
                                  tags=tags, validate_only=True, logging_config='')
        assert_that(application.definition, equal_to('pipeline.yaml'))
        assert_that(application.tag_list, equal_to(['prepare', 'build']))
        assert_that(application.matrix_tag_list, equal_to(['py27', 'py35']))
        assert_that(application.validate_only, equal_to(True))
        assert_that(application.logging_config, equal_to(''))

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
        application = Application(definition='pipeline.yaml', matrix_tags='',
                                  tags='', validate_only=True, logging_config='')
        with patch('sys.exit') as mocked_exit:
            application.validate_document({})
            mocked_exit.assert_called_once_with(1)

    def test_validate_document(self):
        """Testing valid document."""
        document = {'pipeline': [{'stage(Test)': [{'tasks': [{'shell': {'script': 'echo "hello"'}}]}]}]}
        application = Application(definition='pipeline.yaml', matrix_tags='',
                                  tags='', validate_only=True, logging_config='')
        with patch('sys.exit') as mocked_exit:
            document = application.validate_document(document)
            mocked_exit.assert_not_called()
            assert_that(isinstance(document, dict), equal_to(True))
