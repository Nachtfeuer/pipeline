"""Manage report data."""
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
import logging
from schema import Schema, SchemaError, And, Optional, Regex

from .adapter import Adapter
from .decorators import singleton
from .query import Select


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

    SCHEMA = {
        'stage': And(str, len),
        'timestamp': int,
        'status': And(str, lambda s: s in ['started', 'succeed', 'failed']),
        # optional matrix
        Optional('matrix', default='default'): And(str, len),
        # optional information
        Optional('information', default={}): And(len, {
            Regex(r'([a-z][_a-z]*)'): object
        })
    }
    """Schema for data in CollectorUpdate."""

    def __init__(self, **kwargs):
        """
        Initializing and validating fields.

        Args:
            kwargs (dict): application command line options.

        Raises:
            RuntimeError: when validation of parameters has failed.
        """
        try:
            arguments = Adapter(Schema(CollectorUpdate.SCHEMA).validate(kwargs))
            self.matrix = arguments.matrix
            self.stage = arguments.stage
            self.timestamp = arguments.timestamp
            self.status = arguments.status
            self.information = arguments.information.data
        except SchemaError as exception:
            logging.getLogger(__name__).error(exception)
            raise RuntimeError(str(exception))


class CollectorStage(object):
    """
    Represents one item stored in Collector as stage per matrix.

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

    EVENT_ITEM = {
        'timestamp': And(int, lambda n: n > 0),
        Optional('information', default={}): And(len, {
            Regex(r'([a-z][_a-z]*)'): object
        })
    }
    """Schema for event items."""

    SCHEMA = {
        'stage': And(str, len),
        'status': And(str, lambda s: s in ['started', 'succeeded', 'failed']),
        Optional('events', default=[]): And(len, [EVENT_ITEM])
    }
    """Schema for data in CollectorStage."""

    def __init__(self, **kwargs):
        """
        Initializing and validating fields.

        Args:
             kwargs (dict): application command line options.

        Raises:
            RuntimeError: when validation of parameters has failed.
        """
        try:
            arguments = Adapter(Schema(CollectorStage.SCHEMA).validate(kwargs))
            self.stage = arguments.stage
            self.status = arguments.status
            self.events = arguments.events
        except SchemaError as exception:
            logging.getLogger(__name__).error(exception)
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
            item = Schema(CollectorStage.EVENT_ITEM).validate({
                'timestamp': timestamp, 'information': information
            })
            self.events.append(item)
        except SchemaError as exception:
            logging.getLogger(__name__).error(exception)
            raise RuntimeError(str(exception))


@singleton
class Collector(object):
    """
    Central collection of pipeline process data.

    Attributes:
        data (dict): the key is the matrix name and each value is a list of stages.
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
        if matrix_name in self.data:
            result = Select(self.data[matrix_name]).where(
                lambda entry: entry.stage == stage_name).build()
            return result[0] if len(result) > 0 else None
        return None

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
            stage.add(item.timestamp, item.information)
        else:
            stage = CollectorStage(stage=item.stage, status=item.status)
            stage.add(item.timestamp, item.information)
            self.data[item.matrix].append(stage)
