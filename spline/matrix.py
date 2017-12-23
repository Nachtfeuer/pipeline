"""
   Matrix handles multiple pipelines (ordered or in parallel).

.. module:: tasks
    :platform: Unix
    :synopsis: Matrix handles multiple pipelines (ordered or in parallel).
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
# pylint: disable=no-member
import multiprocessing
from contextlib import closing

from .pipeline import Pipeline
from .tools.logger import Logger
from .tools.event import Event


def matrix_worker(data):
    """Run pipelines in parallel."""
    matrix = data['matrix']
    Logger.get_logger(__name__ + '.worker').info(
        "Processing pipeline for matrix entry '%s'", matrix['name'])
    pipeline = Pipeline(model=data['model'], env=matrix['env'],
                        tags=data['tags'])
    pipeline.hooks = data['hooks']
    return pipeline.process(data['pipeline'])


class MatrixProcessData(object):
    """Matrix process parameter."""

    def __init__(self):
        """Initializing defaults."""
        self.__pipeline = {}
        self.__model = {}
        self.__task_filter = []
        self.__hooks = None

    @property
    def pipeline(self):
        """Get pipeline definition."""
        return self.__pipeline

    @pipeline.setter
    def pipeline(self, value):
        """Set pipeline definition."""
        self.__pipeline = value

    @property
    def model(self):
        """Get model data."""
        return self.__model

    @model.setter
    def model(self, value):
        """Set model data."""
        self.__model = value

    @property
    def task_filter(self):
        """Get task filter (tags)."""
        return self.__task_filter

    @task_filter.setter
    def task_filter(self, value):
        """Set task filter."""
        self.__task_filter = value

    @property
    def hooks(self):
        """Get hooks."""
        return self.__hooks

    @hooks.setter
    def hooks(self, value):
        """Set hooks."""
        self.__hooks = value


class Matrix(object):
    """Matrix handles multiple pipelines (ordered or in parallel)."""

    def __init__(self, matrix, matrix_tags, parallel=False):
        """Initialize pipeline with matrix data, a model and the pipeline."""
        self.event = Event.create(__name__)
        self.logger = Logger.get_logger(__name__)
        self.matrix = matrix
        self.matrix_tags = matrix_tags
        self.parallel = parallel

    def can_process_matrix(self, entry):
        """:return: True when matrix entry can be processed."""
        if len(self.matrix_tags) == 0:
            return True

        count = 0
        if 'tags' in entry:
            for tag in self.matrix_tags:
                if tag in entry['tags']:
                    count += 1

        return count > 0

    def run_matrix_ordered(self, process_data):
        """Running pipelines one after the other."""
        output = []
        for entry in self.matrix:
            if self.can_process_matrix(entry):
                self.logger.info("Processing pipeline for matrix entry '%s'", entry['name'])
                pipeline = Pipeline(model=process_data.model, env=entry['env'],
                                    tags=process_data.task_filter)
                pipeline.hooks = process_data.hooks
                result = pipeline.process(process_data.pipeline)
                output += result['output']
                if not result['success']:
                    return {'success': False, 'output': output}
        return {'success': True, 'output': output}

    def run_matrix_in_parallel(self, process_data):
        """Running pipelines in parallel."""
        worker_data = [{'matrix': entry, 'pipeline': process_data.pipeline,
                        'model': process_data.model, 'tags': process_data.task_filter,
                        'hooks': process_data.hooks} for entry in self.matrix
                       if self.can_process_matrix(entry)]
        output = []
        success = True
        with closing(multiprocessing.Pool(multiprocessing.cpu_count())) as pool:
            for result in pool.map(matrix_worker, worker_data):
                output += result['output']
                if not result['success']:
                    success = False
        return {'success': success, 'output': output}

    def process(self, process_data):
        """Process the pipeline per matrix item."""
        if self.parallel:
            return self.run_matrix_in_parallel(process_data)
        return self.run_matrix_ordered(process_data)
