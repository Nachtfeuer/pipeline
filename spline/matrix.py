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
    pipeline = Pipeline(data['pipeline'], model=data['model'], env=matrix['env'],
                        tags=data['tags'], hooks=data['hooks'])
    return pipeline.run()


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

    def run_matrix_ordered(self, pipeline_definition, model, tags, hooks):
        """Running pipelines one after the other."""
        output = []
        for entry in self.matrix:
            if self.can_process_matrix(entry):
                self.logger.info("Processing pipeline for matrix entry '%s'", entry['name'])
                pipeline = Pipeline(pipeline_definition, model=model, env=entry['env'],
                                    tags=tags, hooks=hooks)
                result = pipeline.run()
                output += result['output']
                if not result['success']:
                    return {'success': False, 'output': output}
        return {'success': True, 'output': output}

    def run_matrix_in_parallel(self, pipeline_definition, model, tags, hooks):
        """Running pipelines in parallel."""
        worker_data = [{'matrix': entry, 'pipeline': pipeline_definition, 'model': model,
                        'tags': tags, 'hooks': hooks} for entry in self.matrix
                       if self.can_process_matrix(entry)]
        output = []
        success = True
        with closing(multiprocessing.Pool(multiprocessing.cpu_count())) as pool:
            for result in pool.map(matrix_worker, worker_data):
                output += result['output']
                if not result['success']:
                    success = False
        return {'success': success, 'output': output}

    def process(self, pipeline, model, tags, hooks):
        """Process the pipeline per matrix item."""
        if self.parallel:
            return self.run_matrix_in_parallel(pipeline, model, tags, hooks)
        return self.run_matrix_ordered(pipeline, model, tags, hooks)
