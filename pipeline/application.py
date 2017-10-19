"""
   Represents the main entry point for the pipeline tool.

.. module:: hooks
    :platform: Unix, Windows
    :synopis: Stage is a named group in a pipeline.
.. moduleauthor:: Thomas Lehmann <thomas.lehmann.private@gmail.com>

   =======
   License
   =======
   Copyright (c) 2017 Thomas Lehmann

   Permission is hereby granted, free of charge, to any person obtaining a copy of this
   software and associated documentation files (the "Software"), to deal in the Software
   without restriction, including without limitation the rights to use, copy, modify, merge,
   publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
   to whom the Software is furnished to do so, subject to the following conditions:
   The above copyright notice and this permission notice shall be included in all copies
   or substantial portions of the Software.
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
   DAMAGES OR OTHER LIABILITY,
   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys
import platform
import logging

from pipeline import Pipeline
from components.hooks import Hooks

import click
import yaml


class Application(object):
    """Pipeline application."""

    def __init__(self, definition="", tags=""):
        """Initialize application with definition and tags."""
        self.definition = definition
        self.tags = tags
        self.setup_logging()

    def setup_logging(self):
        """Setup of application logging."""
        logging_format = "%(asctime)-15s %(message)s"
        logging.basicConfig(format=logging_format, level=logging.DEBUG)

    def run(self):
        """Processing the pipeline."""
        logging.info("Running with Python %s", sys.version.replace("\n", ""))
        logging.info("Running on platform %s", platform.platform())
        logging.info("Processing pipeline definition '%s'", self.definition)

        document = yaml.load(open(self.definition).read())
        tag_list = [] if len(self.tags) == 0 else self.tags.split(",")

        hooks = Hooks()
        if 'hooks' in document:
            if 'cleanup' in document['hooks']:
                hooks.cleanup = document['hooks']['cleanup']['script']

        if 'matrix' in document:
            matrix = document['matrix']
            for entry in matrix:
                logging.info("Processing pipeline for matrix entry '%s'", entry['name'])
                pipeline = Pipeline(document['pipeline'], env=entry['env'], tags=tag_list, hooks=hooks)
                pipeline.run()
        else:
            pipeline = Pipeline(document['pipeline'], tags=tag_list, hooks=hooks)
            pipeline.run()


@click.command()
@click.option('--definition', help="Pipeline definition in yaml format")
@click.option('--tags', default='', help="Comma separated list of tags")
def main(definition="", tags=""):
    """Pipeline tool."""
    application = Application(definition, tags)
    application.run()

if __name__ == "__main__":
    main()
