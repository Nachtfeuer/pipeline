"""Manage report data."""
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
import os
from multiprocessing import Process, Queue
from datetime import datetime
from schema import Schema, SchemaError, And, Optional, Regex

from spline.tools.logger import Logger
from spline.tools.report.generator import generate
from spline.tools.adapter import Adapter
from spline.tools.query import Select


class CollectorUpdate(object):
    """
    Represents an update event.

    Attributes:

        matrix(str): the optional name of the pipeline matrix item.
        stage(str): the name/title of the pipeline stage.
        status (str): one of ``started``, ``succeeded``, ``failed``.
        timestamp(int): unix timestamp when the event occured.
        information(dict): free definable information

    Example:

    >>> update = CollectorUpdate(stage='Build', status='started',
    ...                          timestamp=1515645192, information={'step': 'compile'})
    >>> update.stage
    'Build'
    >>> update.status
    'started'
    >>> update.timestamp
    1515645192
    >>> update.information
    {'step': 'compile'}
    """

    @staticmethod
    def schema_complete():
        """Schema for data in CollectorUpdate."""
        return Schema({
            'stage': And(str, len),
            'timestamp': int,
            'status': And(str, lambda s: s in ['started', 'succeeded', 'failed']),
            # optional matrix
            Optional('matrix', default='default'): And(str, len),
            # optional information
            Optional('information', default={}): {
                Optional(Regex(r'([a-z][_a-z]*)')): object
            }
        })

    def __init__(self, **kwargs):
        """
        Initializing and validating fields.

        Args:
            kwargs (dict): application command line options.

        Raises:
            RuntimeError: when validation of parameters has failed.
        """
        try:
            arguments = Adapter(CollectorUpdate.schema_complete().validate(kwargs))
            self.matrix = arguments.matrix
            self.stage = arguments.stage
            self.timestamp = arguments.timestamp
            self.status = arguments.status
            self.information = arguments.information.data
        except SchemaError as exception:
            Logger.get_logger(__name__).error(exception)
            raise RuntimeError(str(exception))


class CollectorStage(object):
    """
    Represent one item stored in Collector as stage per matrix.

    Attributes:

        stage(str): the name/title of the pipeline stage.
        status (str): one of ``started``, ``succeeded``, ``failed``.
        events (list): list with timestamps and information.

    Example:

    >>> stage = CollectorStage(stage='Build', status='started')
    >>> stage.add(timestamp=1515645192, information={'step': 'compile'})
    >>> stage.status
    'started'
    >>> stage.events[0]['timestamp']
    1515645192
    >>> stage.events[0]['information']
    {'step': 'compile'}
    """

    @staticmethod
    def schema_event_items():
        """Schema for event items."""
        return {
            'timestamp': And(int, lambda n: n > 0),
            Optional('information', default={}): {
                Optional(Regex(r'([a-z][_a-z]*)')): object
            }
        }

    @staticmethod
    def schema_complete():
        """Schema for data in CollectorStage."""
        return Schema({
            'stage': And(str, len),
            'status': And(str, lambda s: s in ['started', 'succeeded', 'failed']),
            Optional('events', default=[]): And(len, [CollectorStage.schema_event_items()])
        })

    def __init__(self, **kwargs):
        """
        Initializing and validating fields.

        Args:
             kwargs (dict): application command line options.

        Raises:
            RuntimeError: when validation of parameters has failed.
        """
        try:
            arguments = Adapter(CollectorStage.schema_complete().validate(kwargs))
            self.stage = arguments.stage
            self.status = arguments.status
            self.events = arguments.events
        except SchemaError as exception:
            Logger.get_logger(__name__).error(exception)
            raise RuntimeError(str(exception))

    def add(self, timestamp, information):
        """
        Add event information.

        Args:
            timestamp (int): event timestamp.
            information (dict): event information.

        Raises:
            RuntimeError: when validation of parameters has failed.
        """
        try:
            item = Schema(CollectorStage.schema_event_items()).validate({
                'timestamp': timestamp, 'information': information
            })
            self.events.append(item)
        except SchemaError as exception:
            Logger.get_logger(__name__).error(exception)
            raise RuntimeError(str(exception))

    def duration(self):
        """
        Calculate how long the stage took.

        Returns:
            float: (current) duration of the stage
        """
        duration = 0.0
        if len(self.events) > 0:
            first = datetime.fromtimestamp(self.events[0]['timestamp'])
            last = datetime.fromtimestamp(self.events[-1]['timestamp'])
            duration = (last - first).total_seconds()
        return duration


class Store(object):
    """
    Central collection of pipeline process data.

    Attributes:
        data (dict): the key is the matrix name and each value represents a list of stages.
    """

    def __init__(self):
        """
        Initialize collector with a map.

        The map represents the matrix name; when there is
        no matrix the name will be adjusted to 'default'.

        The collector is a singleton being used by the event
        class to update the collector.
        """
        self.data = {}
        self.document = {}

    def configure(self, document):
        """
        Provide the spline document.

        The template(s) can use the document to extract information
        like matrixes and stages.

        Args:
            document (dict): spline document
        """
        self.document = document

    def count_matrixes(self):
        """
        Count number of registered matrixes.

        Returns:
            int: number of registered matrixes.
        """
        return len(self.data)

    def count_stages(self, matrix_name):
        """
        Number of registered stages for given matrix name.

        Parameters:
            matrix_name (str): name of the matrix

        Returns:
            int: number of reported stages for given matrix name.
        """
        return len(self.data[matrix_name]) if matrix_name in self.data else 0

    def clear(self):
        """Reset the content to have no data anymore."""
        self.data = {}

    def get_stage(self, matrix_name, stage_name):
        """
        Get Stage of a concrete matrix.

        Attributes:
            matrix_name (str): name of the matrix
            stage_name (str): name of the stage.

        Returns:
            CollectorStage: when stage has been found or None.
        """
        found_stage = None
        if matrix_name in self.data:
            result = Select(self.data[matrix_name]).where(
                lambda entry: entry.stage == stage_name).build()
            found_stage = result[0] if len(result) > 0 else None
        return found_stage

    def get_duration(self, matrix_name):
        """
        Get duration for a concrete matrix.

        Args:
            matrix_name (str): name of the Matrix.

        Returns:
            float: duration of concrete matrix in seconds.
        """
        duration = 0.0
        if matrix_name in self.data:
            duration = sum([stage.duration() for stage in self.data[matrix_name]])
        return duration

    def update(self, item):
        """
        Add a collector item.

        Args:
            item (CollectorUpdate): event data like stage, timestampe and status.
        """
        if item.matrix not in self.data:
            self.data[item.matrix] = []

        result = Select(self.data[item.matrix]).where(
            lambda entry: entry.stage == item.stage).build()

        if len(result) > 0:
            stage = result[0]
            stage.status = item.status
            stage.add(item.timestamp, item.information)
        else:
            stage = CollectorStage(stage=item.stage, status=item.status)
            stage.add(item.timestamp, item.information)
            self.data[item.matrix].append(stage)


class Collector(Process):  # pylint: disable=too-many-ancestors
    """Process that does collect updates updating the report data."""

    def __init__(self):
        """Initialize collector with the store and a queue."""
        super(Collector, self).__init__()
        self.store = Store()
        self.queue = Queue()

    def run(self):
        """Collector main loop."""
        while True:
            data = self.queue.get()
            if data is None:
                Logger.get_logger(__name__).info("Stopping collector process ...")
                break

            # updating the report data
            self.store.update(data)
            # writing the report
            generate(self.store, 'html', os.getcwd())
