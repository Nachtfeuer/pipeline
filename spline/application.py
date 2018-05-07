"""Represent the main entry point for the pipeline tool."""
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
# pylint: too-many-instance-attributes
import sys
import platform
import os
import logging
import multiprocessing

import click

from spline.matrix import Matrix, MatrixProcessData
from spline.pipeline import Pipeline
from spline.components.hooks import Hooks
from spline.components.config import ApplicationOptions
from spline.tools.loader import Loader
from spline.tools.logger import Logger
from spline.tools.filters import find_matrix
from spline.tools.event import Event
from spline.tools.report.collector import Collector
from spline.tools.version import VersionsCheck, VersionsReport
from spline.validation import Validator


class Application(object):
    """Pipeline application."""

    def __init__(self, options):
        """
        Initialize application with command line options.

        Args:
            options (ApplicationOptions): given command line options.
        """
        self.event = Event.create(__name__)
        self.options = options
        self.logging_level = logging.DEBUG
        self.setup_logging()
        self.logger = Logger.get_logger(__name__)

    def setup_logging(self):
        """Setup of application logging."""
        is_custom_logging = len(self.options.logging_config) > 0
        is_custom_logging = is_custom_logging and os.path.isfile(self.options.logging_config)
        is_custom_logging = is_custom_logging and not self.options.dry_run

        if is_custom_logging:
            Logger.configure_by_file(self.options.logging_config)
        else:
            logging_format = "%(asctime)-15s - %(name)s - %(message)s"
            if self.options.dry_run:
                logging_format = "%(name)s - %(message)s"
            Logger.configure_default(logging_format, self.logging_level)

    def validate_document(self, definition):
        """
        Validate given pipeline document.

        The method is trying to load, parse and validate the spline document.
        The validator verifies the Python structure B{not} the file format.

        Args:
            definition (str): path and filename of a yaml file containing a valid spline definition.

        Returns:
            dict: loaded and validated spline document.

        Note:
            if validation fails the application does exit!

        See Also:
            spline.validation.Validator
        """
        initial_document = {}
        try:
            initial_document = Loader.load(definition)
        except RuntimeError as exception:
            self.logger.error(str(exception))
            sys.exit(1)

        document = Validator().validate(initial_document)
        if document is None:
            self.logger.info("Schema validation for '%s' has failed", definition)
            sys.exit(1)
        self.logger.info("Schema validation for '%s' succeeded", definition)
        return document

    def run_matrix(self, matrix_definition, document):
        """
        Running pipeline via a matrix.

        Args:
            matrix_definition (dict): one concrete matrix item.
            document (dict): spline document (complete) as loaded from yaml file.
        """
        matrix = Matrix(matrix_definition, 'matrix(parallel)' in document)

        process_data = MatrixProcessData()
        process_data.options = self.options
        process_data.pipeline = document['pipeline']
        process_data.model = {} if 'model' not in document else document['model']
        process_data.hooks = Hooks(document)

        return matrix.process(process_data)

    def shutdown(self, collector, success):
        """Shutdown of the application."""
        self.event.delegate(success)
        if collector is not None:
            collector.queue.put(None)
            collector.join()
        if not success:
            sys.exit(1)

    def run(self, definition):
        """Processing the pipeline."""
        self.logger.info("Running with Python %s", sys.version.replace("\n", ""))
        self.logger.info("Running on platform %s", platform.platform())
        self.logger.info("Current cpu count is %d", multiprocessing.cpu_count())
        self.logger.info("Processing pipeline definition '%s'", definition)

        document = self.validate_document(definition)
        if self.options.validate_only:
            self.logger.info("Stopping after validation as requested!")
            return []

        self.provide_temporary_scripts_path()

        versions = VersionsCheck().process(document)
        VersionsReport().process(versions)

        collector = Application.create_and_run_collector(document, self.options)
        matrix = find_matrix(document)
        output = []
        if len(matrix) == 0:
            model = {} if 'model' not in document else document['model']
            pipeline = Pipeline(model=model, options=self.options)
            pipeline.hooks = Hooks(document)
            result = pipeline.process(document['pipeline'])
        else:
            result = self.run_matrix(matrix, document)

        output = result['output']
        self.shutdown(collector, success=result['success'])
        return output

    def provide_temporary_scripts_path(self):
        """When configured trying to ensure that path does exist."""
        if len(self.options.temporary_scripts_path) > 0:
            if os.path.isfile(self.options.temporary_scripts_path):
                self.logger.error("Error: configured script path seems to be a file!")
                # it's ok to leave because called before the collector runs
                sys.exit(1)

            if not os.path.isdir(self.options.temporary_scripts_path):
                os.makedirs(self.options.temporary_scripts_path)

    @staticmethod
    def create_and_run_collector(document, options):
        """Create and run collector process for report data."""
        collector = None
        if not options.report == 'off':
            collector = Collector()
            collector.store.configure(document)
            Event.configure(collector_queue=collector.queue)
            collector.start()
        return collector


@click.command()
@click.option('--definition', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              metavar='<path/filename>',
              default='pipeline.yaml', help="Pipeline definition in yaml format (default: pipeline.yaml)")
@click.option('--tags', type=click.STRING, default='', metavar="tag[,tag,...]",
              help="Comma separated list of tags for filtering individual tasks")
@click.option('--matrix-tags', type=click.STRING, default='', metavar="tag[,tag,...]",
              help="Comma separated list of tags for filtering individual matrix runs")
@click.option('--validate-only', is_flag=True, default=False,
              help="When used validates given pipeline definition only")
@click.option('--logging-config', default="", type=click.STRING,
              help="Path and filename of logging configuration")
@click.option('--event-logging', is_flag=True, default=False,
              help="When enabled then it does log event details")
@click.option('--dry-run', is_flag=True, default=False,
              help="When enabled then no Bash script is executed but shown")
@click.option('--debug', is_flag=True, default=False,
              help="When enabled then using 'set -x' for debugging Bash scripts")
@click.option('--strict', is_flag=True, default=False,
              help="When enabled then using strict mode for Bash")
@click.option('--report', default='off', type=click.Choice(['off', 'html']),
              help="Adjusting report and format (default: off)")
@click.option('--temporary-scripts-path', default='', type=str, metavar='<path>',
              help="When not set using system temp path, otherwise defined one")
def main(**kwargs):
    """The Pipeline tool."""
    options = ApplicationOptions(**kwargs)
    Event.configure(is_logging_enabled=options.event_logging)
    application = Application(options)
    application.run(options.definition)


if __name__ == "__main__":
    main()
