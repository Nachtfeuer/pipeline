"""Provide configured logger."""
# Copyright (c) 2017 Thomas Lehmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import logging.config


class NoLogger(object):
    """A logger that does nothing."""

    def info(self, *args, **kwargs):
        """Hide information messages."""
        pass

    def warning(self, *args, **kwargs):
        """Hide warning messages."""
        pass

    def severe(self, *args, **kwargs):
        """Hide severe messages."""
        pass


class Logger(object):
    """Wrapper for logging calls."""

    use_external_configuration = False

    @staticmethod
    def configure_by_file(filename):
        """Read logging configuration from an external file."""
        logging.config.fileConfig(filename)
        Logger.use_external_configuration = True

    @staticmethod
    def configure_default(logging_format, level):
        """Default configuration."""
        logging.basicConfig(format=logging_format, level=level)

    @staticmethod
    def get_logger(name):
        """Get a logger by name."""
        if name is None:
            return NoLogger()

        logger = logging.getLogger(name)
        if Logger.use_external_configuration:
            logger.propagate = False
        return logger
