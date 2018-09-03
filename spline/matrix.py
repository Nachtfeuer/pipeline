"""
Matrix handles multiple pipelines (ordered or in parallel).

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
# pylint: disable=no-member
import multiprocessing
from contextlib import closing

from spline.pipeline import Pipeline
from spline.tools.logger import Logger
from spline.tools.event import Event


def matrix_worker(data):
    """
    Run pipelines in parallel.

    Args:
        data(dict): parameters for the pipeline (model, options, ...).
    Returns:
        dict: with two fields: success True/False and captured output (list of str).
    """
    matrix = data['matrix']
    Logger.get_logger(__name__ + '.worker').info(
        "Processing pipeline for matrix entry '%s'", matrix['name'])

    env = matrix['env'].copy()
    env.update({'PIPELINE_MATRIX': matrix['name']})

    pipeline = Pipeline(model=data['model'], env=env, options=data['options'])
    pipeline.hooks = data['hooks']
    return pipeline.process(data['pipeline'])


class MatrixProcessData(object):
    """Matrix process parameter."""

    def __init__(self):
        """Initializing defaults."""
        self.__pipeline = {}
        self.__model = {}
        self.__options = None
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
    def options(self):
        """Get application options."""
        return self.__options

    @options.setter
    def options(self, value):
        """Set application options."""
        self.__options = value

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

    def __init__(self, matrix, parallel=False):
        """Initialize pipeline with matrix data."""
        self.event = Event.create(__name__)
        self.logger = Logger.get_logger(__name__)
        self.matrix = matrix
        self.parallel = parallel

    @staticmethod
    def can_process_matrix(entry, matrix_tags):
        """
        Check given matrix tags to be in the given list of matric tags.

        Args:
            entry (dict): matrix item (in yaml).
            matrix_tags (list): represents --matrix-tags defined by user in command line.
        Returns:
            bool: True when matrix entry can be processed.
        """
        if len(matrix_tags) == 0:
            return True

        count = 0
        if 'tags' in entry:
            for tag in matrix_tags:
                if tag in entry['tags']:
                    count += 1

        return count > 0

    def run_matrix_ordered(self, process_data):
        """
        Running pipelines one after the other.

        Returns
            dict: with two fields: success True/False and captured output (list of str).
        """
        output = []
        for entry in self.matrix:
            env = entry['env'].copy()
            env.update({'PIPELINE_MATRIX': entry['name']})

            if Matrix.can_process_matrix(entry, process_data.options.matrix_tags):
                self.logger.info("Processing pipeline for matrix entry '%s'", entry['name'])
                pipeline = Pipeline(model=process_data.model, env=env,
                                    options=process_data.options)
                pipeline.hooks = process_data.hooks
                result = pipeline.process(process_data.pipeline)
                output += result['output']
                if not result['success']:
                    return {'success': False, 'output': output}
        return {'success': True, 'output': output}

    def run_matrix_in_parallel(self, process_data):
        """Running pipelines in parallel."""
        worker_data = [{'matrix': entry, 'pipeline': process_data.pipeline,
                        'model': process_data.model, 'options': process_data.options,
                        'hooks': process_data.hooks} for entry in self.matrix
                       if Matrix.can_process_matrix(entry, process_data.options.matrix_tags)]
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
        if self.parallel and not process_data.options.dry_run:
            return self.run_matrix_in_parallel(process_data)
        return self.run_matrix_ordered(process_data)
