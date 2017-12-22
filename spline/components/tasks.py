"""
   Tasks is a group of tasks/shells with no name.

.. module:: tasks
    :platform: Unix
    :synopsis: Tasks is a group of tasks/shells with no name.
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
from .bash import Bash
from .docker import Container, Image
from .config import ShellConfig
from ..tools.logger import Logger
from ..tools.event import Event
from ..tools.adapter import Adapter


def get_creator_by_name(name):
    """Get creator function by name."""
    return {'docker(container)': Container.creator,
            'shell': Bash.creator, 'docker(image)': Image.creator}[name]


def worker(data):
    """Running on shell via multiprocessing."""
    creator = get_creator_by_name(data['creator'])
    shell = creator(data['entry'],
                    ShellConfig(script=data['entry']['script'],
                                title=data['entry']['title'] if 'title' in data['entry'] else '',
                                model=data['model'], env=data['env'], item=data['item']))
    output = []
    for line in shell.process():
        output.append(line)
        Logger.get_logger(__name__ + '.worker').info(" | %s", line)
    return {'success': shell.success, 'output': output}


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

    def prepare_shell_data(self, shells, key, entry):
        """Prepare one shell or docker task."""
        if self.can_process_shell(entry):

            for item in entry['with'] if 'with' in entry else ['']:
                shells.append({
                    'creator': key,
                    'entry': entry,
                    'model': self.pipeline.model,
                    'env': self.get_merged_env(),
                    'item': item})

    def process(self, tasks):
        """Processing a group of tasks."""
        self.logger.info("Processing group of tasks (parallel=%s)", self.parallel)
        self.pipeline.data.env_list[2] = {}

        output = []
        shells = []
        for task_entry in tasks:
            key, entry = list(task_entry.items())[0]
            if key == "env":
                result = Adapter(self.process_shells(shells))
                output += result.output
                shells = []
                if not result.success:
                    break

                self.pipeline.data.env_list[2].update(entry)
                self.logger.debug("Updating environment at level 2 with %s",
                                  self.pipeline.data.env_list[2])

            elif key in ['shell', 'docker(container)', 'docker(image)']:
                self.prepare_shell_data(shells, key, entry)

        result = Adapter(self.process_shells(shells))
        output += result.output
        if result.success:
            self.event.succeeded()

        return {'success': result.success, 'output': output}

    def process_shells_parallel(self, shells):
        """Processing a list of shells parallel."""
        output = []
        success = True
        with closing(multiprocessing.Pool(multiprocessing.cpu_count())) as pool:
            for result in [Adapter(entry) for entry in pool.map(worker, [shell for shell in shells])]:
                output += result.output
                if not result.success:
                    success = False
        if success:
            self.logger.info("Parallel Processing Bash code: finished")
            return {'success': True, 'output': output}

        for line in self.run_cleanup(shells[0]['env'], 99):
            output.append(line)
        self.logger.error("Pipeline has failed: immediately leaving!")
        self.event.failed()
        return {'success': False, 'output': output}

    def process_shells_ordered(self, shells):
        """Processing a list of shells one after the other."""
        output = []
        for shell in shells:
            entry = shell['entry']
            config = ShellConfig(script=entry['script'], title=entry['title'] if 'title' in entry else '',
                                 model=shell['model'], env=shell['env'], item=shell['item'])
            result = Adapter(self.process_shell(get_creator_by_name(shell['creator']), entry, config))
            output += result.output
            if not result.success:
                return {'success': False, 'output': output}
        return {'success': True, 'output': output}

    def process_shells(self, shells):
        """Processing a list of shells."""
        result = {'success': True, 'output': []}
        if self.parallel and len(shells) > 1:
            result = self.process_shells_parallel(shells)
        elif len(shells) > 0:
            result = self.process_shells_ordered(shells)
        return result

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

    def process_shell(self, creator, entry, config):
        """Processing a shell entry."""
        self.logger.info("Processing Bash code: start")

        output = []
        shell = creator(entry, config)
        for line in shell.process():
            output.append(line)
            self.logger.info(" | %s", line)

        if shell.success:
            self.logger.info("Processing Bash code: finished")
            return {'success': True, 'output': output}

        for line in self.run_cleanup(config.env, shell.exit_code):
            output.append(line)

        self.logger.error("Pipeline has failed: leaving as soon as possible!")
        self.event.failed()
        return {'success': False, 'output': output}

    def run_cleanup(self, env, exit_code):
        """Run cleanup hook when configured."""
        output = []
        if self.pipeline.data.hooks and len(self.pipeline.data.hooks.cleanup) > 0:
            env.update({'PIPELINE_RESULT': 'FAILURE'})
            env.update({'PIPELINE_SHELL_EXIT_CODE': str(exit_code)})
            config = ShellConfig(script=self.pipeline.data.hooks.cleanup, model=self.pipeline.model, env=env)
            cleanup_shell = Bash(config)
            for line in cleanup_shell.process():
                output.append(line)
                self.logger.info(" | %s", line)
        return output
