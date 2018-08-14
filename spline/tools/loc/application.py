"""Represent the main entry point for the spline loc tool."""
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
# pylint: disable=no-self-use, cell-var-from-loop,unnecessary-lambda
import sys
import os
import platform
import logging
import multiprocessing
import re

import click
from yaml import safe_load

from spline.tools.logger import Logger
from spline.tools.adapter import Adapter
from spline.tools.query import Select
from spline.tools.table import pprint


class Application(object):
    """Spline loc application for counting loc, com and calculating ratio, failing by threshold."""

    def __init__(self, **options):
        """
        Initialize application with command line options.

        Args:
            options (ApplicationOptions): given command line options.
        """
        self.options = options
        self.logging_level = logging.DEBUG
        self.setup_logging()
        self.logger = Logger.get_logger(__name__)
        self.results = []

    def setup_logging(self):
        """Setup of application logging."""
        logging_format = "%(asctime)-15s - %(name)s - %(message)s"
        Logger.configure_default(logging_format, self.logging_level)

    def load_configuration(self):
        """Loading configuration."""
        filename = os.path.join(os.path.dirname(__file__), 'templates/spline-loc.yml.j2')
        with open(filename) as handle:
            return Adapter(safe_load(handle)).configuration

    @staticmethod
    def ignore_path(path):
        """
        Verify whether to ignore a path.

        Args:
            path (str): path to check.

        Returns:
            bool: True when to ignore given path.
        """
        ignore = False
        for name in ['.tox', 'dist', 'build', 'node_modules', 'htmlcov']:
            if path.find(name) >= 0:
                ignore = True
                break
        return ignore

    @staticmethod
    def walk_files_for(paths, supported_extensions):
        """
        Iterating files for given extensions.

        Args:
            supported_extensions (list): supported file extentsion for which to check loc and com.

        Returns:
            str: yield each full path and filename found.
        """
        for path in paths:
            for root, _, files in os.walk(path):
                if Application.ignore_path(root.replace(path, '')):
                    continue

                for filename in files:
                    extension = os.path.splitext(filename)[1]
                    if extension in supported_extensions:
                        yield path, os.path.join(root, filename), extension

    def analyse(self, path_and_filename, pattern):
        """
        Find out lines of code and lines of comments.

        Args:
            path_and_filename (str): path and filename to parse  for loc and com.
            pattern (str): regex to search for line commens and block comments

        Returns:
            int, int: loc and com for given file.
        """
        with open(path_and_filename) as handle:
            content = handle.read()
            loc = content.count('\n') + 1
            com = 0
            for match in re.findall(pattern, content, re.DOTALL):
                com += match.count('\n') + 1

            return max(0, loc - com), com

    def run(self):
        """Processing the pipeline."""
        self.logger.info("Running with Python %s", sys.version.replace("\n", ""))
        self.logger.info("Running on platform %s", platform.platform())
        self.logger.info("Current cpu count is %d", multiprocessing.cpu_count())

        configuration = self.load_configuration()
        paths = [os.path.abspath(path) for path in Adapter(self.options).path]
        supported_extension = [
            ext.strip() for entry in configuration for ext in Adapter(entry).extension.split()]

        for path, path_and_filename, extension in Application.walk_files_for(paths, supported_extension):
            entry = Select(*configuration) \
                .where(lambda entry: extension in Adapter(entry).extension.split()) \
                .transform(lambda entry: Adapter(entry)) \
                .build()[0]
            # parsing file with regex to get loc and com values
            # 100 lines of code (total) with 50 lines of comments means: loc=50, com=50
            # the ratio would be then: 1.0
            loc, com = self.analyse(path_and_filename, entry.regex)
            ratio = float(com) / float(loc) if loc > 0 and com < loc else 1.0

            self.results.append({
                'type': entry.type,
                'file': path_and_filename.replace(path + '/', ''),
                'loc': loc,
                'com': com,
                'ratio': "%.2f" % ratio
            })
        # for the table we are mainly interested in ratio below defined threshold
        # (except you want to see all of your code: --show-all)
        ppresults = Select(*self.results).where(
            lambda entry: float(Adapter(entry).ratio) < Adapter(self.options).threshold or
            Adapter(self.options).show_all).build()

        # print out results in table format
        pprint(ppresults, keys=['ratio', 'loc', 'com', 'file', 'type'])

        if Adapter(self.options).average:
            all_ratio = Select(*self.results).transform(lambda entry: float(Adapter(entry).ratio)).build()
            avg_ratio = float(sum(all_ratio)) / float(len(all_ratio)) if len(all_ratio) > 0 else 1.0
            self.logger.info('average ratio is %.2f for %d files', avg_ratio, len(all_ratio))
            return avg_ratio >= Adapter(self.options).threshold

        # providing results (mainly for unittesting)
        return len(Select(*self.results).where(
            lambda entry: float(Adapter(entry).ratio) < Adapter(self.options).threshold).build()) == 0


def main(**options):
    """Spline loc tool."""
    application = Application(**options)
    # fails application when your defined threshold is higher than your ratio of com/loc.
    if not application.run():
        sys.exit(1)
    return application


@click.command()
@click.option('--path', type=str, default=[os.getcwd()], multiple=True,
              help="Path where to parse files")
@click.option('-t', '--threshold', type=float, default=0.5,
              help="Expected Ratio between documentation and code (default: 0.5)")
@click.option('-s', '--show-all', is_flag=True, default=False,
              help="When enabled then showing statistic for all files")
@click.option('-a', '--average', is_flag=True, default=False,
              help='When set use the average com/loc of all files against threshold (default: false)')
def click_main(**options):
    """Spline loc tool - application entry point."""
    main(**options)


if __name__ == "__main__":
    click_main()
