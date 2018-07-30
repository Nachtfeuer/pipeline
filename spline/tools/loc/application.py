"""Represent the main entry point for the pipeline tool."""
# Copyright (c) 2018 Thomas Lehmann
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
# pylint: disable=no-self-use
import sys
import os
import platform
import logging
import multiprocessing
import re

import click
from spline.tools.logger import Logger


class Application(object):
    """Spline loc application."""

    def __init__(self, options):
        """
        Initialize application with command line options.

        Args:
            options (ApplicationOptions): given command line options.
        """
        self.options = options
        self.logging_level = logging.DEBUG
        self.setup_logging()
        self.logger = Logger.get_logger(__name__)

    def setup_logging(self):
        """Setup of application logging."""
        logging_format = "%(asctime)-15s - %(name)s - %(message)s"
        Logger.configure_default(logging_format, self.logging_level)

    @staticmethod
    def walk_files_for(supported_extensions):
        """
        Iterating files for given extensions.

        Args:
            supported_extensions (list): supported file extentsion for which to check loc and com.

        Returns:
            str: yield each full path and filename found.
        """
        for root, _, files in os.walk(os.getcwd()):
            for filename in files:
                if os.path.splitext(filename)[1] in supported_extensions:
                    yield os.path.join(root, filename)

    def analyse(self, path_and_filename):
        """
        Find out lines of code and lines of comments.

        Args:
            path_and_filename (str): path and filename to parse  for loc and com.

        Returns:
            int, int: loc and com for given file.
        """
        pattern = r'([ ]*#[^\n]*|""".*?""")'
        with open(path_and_filename) as handle:
            content = handle.read()
            loc = content.count('\n') + 1
            com = 0
            for match in re.findall(pattern, content, re.DOTALL):
                com += match.count('\n') + 1

            return loc, com

    def run(self):
        """Processing the pipeline."""
        self.logger.info("Running with Python %s", sys.version.replace("\n", ""))
        self.logger.info("Running on platform %s", platform.platform())
        self.logger.info("Current cpu count is %d", multiprocessing.cpu_count())

        for path_and_filename in Application.walk_files_for(['.py']):
            loc, com = self.analyse(path_and_filename)
            print(path_and_filename, loc, com, float(com) / float(loc))


@click.command()
def main(**options):
    """Spline loc tool."""
    application = Application(options)
    application.run()


if __name__ == "__main__":
    main()
