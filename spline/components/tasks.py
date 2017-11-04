"""
   Tasks is a group of tasks/shells with no name.

.. module:: tasks
    :platform: Unix
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
# pylint: disable=no-member
import sys
import multiprocessing
from contextlib import closing
from .bash import Bash
from .docker import Container
from ..tools.logger import Logger
from ..tools.event import Event


def get_creator_by_name(name):
    """Get creator function by name."""
    return {'Container': Container.creator, 'Bash': Bash.creator}[name]


def worker(data):
    """Running on shell via multiprocessing."""
    creator = get_creator_by_name(data['creator'])
    shell = creator(data['entry'], data['env'])
    for line in shell.process():
        Logger.get_logger(__name__ + '.worker').info(" | %s", line)
    return shell.success


class Tasks(object):
    """Class for procressing a list of tasks."""

    def __init__(self, pipeline, parallel):
        """Initializing with referenz to pipeline main object."""
        self.event = Event.create(__name__)
        self.pipeline = pipeline
        self.parallel = parallel
        self.logger = Logger.get_logger(__name__)

    def get_merged_env(self):
        """Copying and merging environment variables."""
        env = self.pipeline.data.env_list[0].copy()
        env.update(self.pipeline.data.env_list[1].copy())
        env.update(self.pipeline.data.env_list[2].copy())
        return env

    def process(self, tasks):
        """Processing a group of tasks."""
        self.logger.info("Processing group of tasks")
        if self.parallel:
            self.logger.info("Run tasks in parallel")

        shells = []
        for entry in tasks:
            key = entry.keys()[0]
            if key == "env":
                self.process_shells(shells)
                shells = []

                self.pipeline.data.env_list[2].update(entry[key])
                self.logger.debug("Updating environment at level 2 with %s",
                                  self.pipeline.data.env_list[2])
                continue

            if key == "shell":
                if self.can_process_shell(entry[key]):
                    shells.append({
                        'creator': Bash.__name__, 'entry': entry[key], 'env': self.get_merged_env()})
                continue

            if key == "docker(container)":
                if self.can_process_shell(entry[key]):
                    shells.append({
                        'creator': Container.__name__, 'entry': entry[key], 'env': self.get_merged_env()})
                continue

        if len(shells) > 0:
            self.process_shells(shells)

        self.event.succeeded()

    def process_shells(self, shells):
        """Processing a list of shells."""
        if self.parallel:
            success = True
            with closing(multiprocessing.Pool(multiprocessing.cpu_count())) as pool:
                for result in pool.map(worker, [shell for shell in shells]):
                    if not result:
                        success = False
            if success:
                self.logger.info("Parallel Processing Bash code: finished")
            else:
                self.run_cleanup(shells[0]['env'], 99)
                self.logger.error("Pipeline has failed: immediately leaving!")
                self.event.failed()
                sys.exit(99)
        else:
            for shell in shells:
                self.process_shell(get_creator_by_name(shell['creator']), shell['entry'], shell['env'])

    def can_process_shell(self, entry):
        """:return: True when shell can be executed."""
        if len(self.pipeline.data.tags) == 0:
            return True

        count = 0
        if 'tags' in entry:
            for tag in self.pipeline.data.tags:
                if tag in entry['tags']:
                    count += 1

        return count > 0

    def process_shell(self, creator, entry, env):
        """Processing a shell entry."""
        self.logger.info("Processing Bash code: start")

        shell = creator(entry, env)
        for line in shell.process():
            self.logger.info(" | %s", line)

        if shell.success:
            self.logger.info("Processing Bash code: finished")
        else:
            self.run_cleanup(env, shell.exit_code)
            self.logger.error("Pipeline has failed: immediately leaving!")
            self.event.failed()
            sys.exit(shell.exit_code)

    def run_cleanup(self, env, exit_code):
        """Run cleanup hook when configured."""
        if len(self.pipeline.data.hooks.cleanup) > 0:
            env.update({'PIPELINE_RESULT': 'FAILURE'})
            env.update({'PIPELINE_SHELL_EXIT_CODE': str(exit_code)})
            cleanup_shell = Bash(self.pipeline.data.hooks.cleanup, '', env)
            for line in cleanup_shell.process():
                self.logger.info(" | %s", line)
