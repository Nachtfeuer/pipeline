"""
   Provide event class for event logging and performance measurement.

.. module:: event
    :platform: Unix
    :synopis: Provide event class for event logging and performance measurement.
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
from datetime import datetime
from .logger import Logger


class Event(object):
    """Event mechanism for pipeline."""

    is_logging_enabled = False

    def __init__(self, context, timestamp, **kwargs):
        """Initialize event with optional additional information."""
        self.context = context
        self.created = timestamp
        self.finished = timestamp
        self.status = 'started'
        self.information = {}
        self.information.update(kwargs)

        if Event.is_logging_enabled:
            self.logger = Logger.get_logger(context + ".event")
        else:
            self.logger = Logger.get_logger(None)

    @staticmethod
    def configure(is_logging_enabled):
        """Global configuration for event handling."""
        Event.is_logging_enabled = is_logging_enabled

    @staticmethod
    def create(context, **kwargs):
        """Create event with optional additional information."""
        return Event(context, datetime.now(), **kwargs)

    def failed(self, **kwargs):
        """Finish event as failed with optional additional information."""
        self.finished = datetime.now()
        self.status = 'failed'
        self.information.update(kwargs)
        self.logger.info("Failed - took %f seconds.", self.duration())

    def succeeded(self, **kwargs):
        """Finish event as succeeded with optional additional information."""
        self.finished = datetime.now()
        self.status = 'succeeded'
        self.information.update(kwargs)
        self.logger.info("Succeeded - took %f seconds.", self.duration())

    def duration(self):
        """Calculate event duration."""
        return (self.finished - self.created).total_seconds()
