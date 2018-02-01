"""Testing of class Logger."""
# pylint: disable=no-self-use, invalid-name
import unittest
import logging
from io import StringIO
from mock import patch
from hamcrest import assert_that, equal_to
from spline.tools.logger import Logger, NoLogger
from spline.tools.stream import stdout_redirector


class TestLogger(unittest.TestCase):
    """Testing of class Logger."""

    def test_no_logger(self):
        """Testing retrieval of NoLogger instance."""
        logger = Logger.get_logger(None)
        assert_that(isinstance(logger, NoLogger), equal_to(True))

        f = StringIO()
        with stdout_redirector(f):
            logger.info("hello")
            logger.warning("hello")
            logger.severe("hello")
        assert_that(len(f.getvalue()), equal_to(0))
        f.close()

    def test_configure_default(self):
        """Testing function Logger.configure_default."""
        logging_format = "%(asctime)-15s - %(name)s - %(message)s"
        logging_level = logging.DEBUG

        with patch('logging.basicConfig') as mocked_logging_basicConfig:
            Logger.configure_default(logging_format, logging_level)
            mocked_logging_basicConfig.assert_called_with(
                format=logging_format, level=logging_level)

        assert_that(Logger.use_external_configuration, equal_to(False))

    def test_configure_by_file(self):
        """Testing function Logger.configure_default."""
        logging_config_filename = "logging.conf"

        with patch('logging.config.fileConfig') as mocked_logging_config_fileConfig:
            Logger.configure_by_file(logging_config_filename)
            mocked_logging_config_fileConfig.assert_called_with(
                logging_config_filename)
            assert_that(Logger.use_external_configuration, equal_to(True))
            Logger.use_external_configuration = False

    def test_get_logger(self):
        """Testing function Logger.get_logger for real logger."""
        with patch('logging.getLogger') as mocked_logging_get_logger:
            Logger.get_logger('test')
            mocked_logging_get_logger.assert_called_with('test')

    def test_get_logger_with_external_configuration(self):
        """Testing function Logger.get_logger for real logger."""
        Logger.use_external_configuration = True
        with patch('logging.getLogger') as mocked_logging_get_logger:
            logger = Logger.get_logger('test')
            mocked_logging_get_logger.assert_called_with('test')
            assert_that(logger.propagate, equal_to(False))
        Logger.use_external_configuration = False
