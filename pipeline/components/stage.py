"""
   Stage is a named group in a pipeline.

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
import logging
from tasks import Tasks


class Stage(object):
    """Class for representing a name group (title)."""

    def __init__(self, pipeline, title):
        """Initializing with referenz to pipeline main object."""
        self.pipeline = pipeline
        self.title = title

    def process(self, stage):
        """Processing one stage."""
        logging.info("Processing pipeline stage '%s'", self.title)
        for entry in stage:
            key = entry.keys()[0]
            if key == "env":
                self.pipeline.data.env_list[1].update(entry[key])
                logging.debug("Updating environment at level 1 with %s",
                              self.pipeline.data.env_list[1])
                continue

            if key == "tasks":
                tasks = Tasks(self.pipeline)
                tasks.process(entry[key])
                continue
