"""
Stage is a named group in a pipeline.

License::

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
import re
from spline.components.tasks import Tasks
from spline.tools.logger import Logger
from spline.tools.event import Event


class Stage(object):
    """Class for representing a named group (title)."""

    def __init__(self, pipeline, title):
        """Initializing with reference to pipeline main object."""
        matrix = 'default'

        if 'PIPELINE_MATRIX' in pipeline.data.env_list[0]:
            matrix = pipeline.data.env_list[0]['PIPELINE_MATRIX']

        # providing title of stage and name of matrix to the event
        self.event = Event.create(__name__, matrix=matrix, stage=title, report=pipeline.options.report)

        self.logger = Logger.get_logger(__name__)
        self.pipeline = pipeline
        self.title = title
        self.pipeline.data.env_list[1].update({'PIPELINE_STAGE': self.title})

    def process(self, stage):
        """Processing one stage."""
        self.logger.info("Processing pipeline stage '%s'", self.title)
        output = []
        for entry in stage:
            key = list(entry.keys())[0]
            if key == "env":
                self.pipeline.data.env_list[1].update(entry[key])
                self.logger.debug("Updating environment at level 1 with %s",
                                  self.pipeline.data.env_list[1])
                continue

            # if not "env" then it must be "tasks" (schema):
            tasks = Tasks(self.pipeline, re.match(r"tasks\(parallel\)", key) is not None)
            result = tasks.process(entry[key])
            for line in result['output']:
                output.append(line)
            if not result['success']:
                self.event.failed()
                return {'success': False, 'output': output}

        self.event.succeeded()
        return {'success': True, 'output': output}
