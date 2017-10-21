"""
   Tasks is a group of tasks/shells with no name.

.. module:: hooks
    :platform: Unix, Windows
    :synopis: Tasks is a group of tasks/shells with no name.
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
import logging
from .bash import Bash


class Tasks(object):
    """Class for procressing a list of tasks."""

    def __init__(self, pipeline):
        """Initializing with referenz to pipeline main object."""
        self.pipeline = pipeline
        self.logger = logging.getLogger(__name__)

    def process(self, tasks):
        """Processing a group of tasks."""
        self.logger.info("Processing group of tasks")
        for entry in tasks:
            key = entry.keys()[0]
            if key == "env":
                self.pipeline.data.env_list[2].update(entry[key])
                self.logger.debug("Updating environment at level 2 with %s",
                                  self.pipeline.data.env_list[2])
                continue

            if key == "shell":
                self.process_shell(entry, key)
                continue

    def process_shell(self, entry, key):
        """Processing a shell entry."""
        if len(self.pipeline.data.tags) > 0:
            count = 0
            if 'tags' in entry[key]:
                for tag in self.pipeline.data.tags:
                    if tag in entry[key]['tags']:
                        count += 1

            if count == 0:
                return

        # copying and merging environment variables
        env = self.pipeline.data.env_list[0].copy()
        env.update(self.pipeline.data.env_list[1].copy())
        env.update(self.pipeline.data.env_list[2].copy())

        self.logger.info("Processing Bash code: start")
        shell = Bash(entry[key]['script'], env)
        for line in shell.process():
            self.logger.info(" | %s", line)

        if shell.success:
            self.logger.info("Processing Bash code: finished")
        else:
            if len(self.pipeline.data.hooks.cleanup) > 0:
                env.update({'PIPELINE_RESULT': 'FAILURE'})
                env.update({'PIPELINE_SHELL_EXIT_CODE': str(shell.exit_code)})
                cleanup_shell = Bash(self.pipeline.data.hooks.cleanup, env)
                for line in cleanup_shell.process():
                    self.logger.info(" | %s", line)
            self.logger.error("Pipeline has failed: immediately leaving!")
            sys.exit(shell.exit_code)
