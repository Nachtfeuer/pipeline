"""Tasks is a group of tasks/shells with no name."""
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
# pylint: disable=no-member
import multiprocessing
from contextlib import closing
from spline.components.bash import Bash
from spline.components.docker import Container, Image
from spline.components.script import Script
from spline.components.config import ShellConfig
from spline.tools.logger import Logger
from spline.tools.event import Event
from spline.tools.adapter import Adapter
from spline.tools.filters import render
from spline.tools.condition import Condition


def get_creator_by_name(name):
    """Get creator function by name."""
    return {'docker(container)': Container.creator,
            'shell': Bash.creator, 'docker(image)': Image.creator,
            'python': Script.creator}[name]


def worker(data):
    """Running on shell via multiprocessing."""
    creator = get_creator_by_name(data['creator'])
    shell = creator(data['entry'],
                    ShellConfig(script=data['entry']['script'],
                                title=data['entry']['title'] if 'title' in data['entry'] else '',
                                model=data['model'], env=data['env'], item=data['item'],
                                dry_run=data['dry_run'], debug=data['debug'], variables=data['variables']))
    output = []
    for line in shell.process():
        output.append(line)
        Logger.get_logger(__name__ + '.worker').info(" | %s", line)
    return {'id': data['id'], 'success': shell.success, 'output': output}


class Tasks(object):
    """Class for procressing a list of tasks."""

    def __init__(self, pipeline, parallel):
        """Initializing with referenz to pipeline main object."""
        self.event = Event.create(__name__)
        self.pipeline = pipeline
        self.parallel = parallel if not pipeline.options.dry_run else False
        self.logger = Logger.get_logger(__name__)
        self.next_task_id = 1

    def get_merged_env(self):
        """Copying and merging environment variables."""
        env = self.pipeline.data.env_list[0].copy()
        env.update(self.pipeline.data.env_list[1].copy())
        env.update(self.pipeline.data.env_list[2].copy())
        return env

    def prepare_shell_data(self, shells, key, entry):
        """Prepare one shell or docker task."""
        if self.can_process_shell(entry):
            if key in ['python']:
                entry['type'] = key

            for item in entry['with'] if 'with' in entry else ['']:
                shells.append({
                    'id': self.next_task_id,
                    'creator': key,
                    'entry': entry,
                    'model': self.pipeline.model,
                    'env': self.get_merged_env(),
                    'item': item,
                    'dry_run': self.pipeline.options.dry_run,
                    'debug': self.pipeline.options.debug,
                    'variables': self.pipeline.variables})
                self.next_task_id += 1

    def get_parallel_mode(self):
        """Logging helper for visualizing parallel state."""
        if self.pipeline.options.dry_run:
            return "disabled"
        return "yes" if self.parallel else "no"

    def process(self, document):
        """Processing a group of tasks."""
        self.logger.info("Processing group of tasks (parallel=%s)", self.get_parallel_mode())
        self.pipeline.data.env_list[2] = {}

        output, shells = [], []
        result = Adapter({'success': True, 'output': []})
        for task_entry in document:
            key, entry = list(task_entry.items())[0]
            if key == "env":
                result = Adapter(self.process_shells(shells))
                output += result.output
                shells = []
                if not result.success:
                    break

                self.pipeline.data.env_list[2].update(entry)

            elif key in ['shell', 'docker(container)', 'docker(image)', 'python']:
                self.prepare_shell_data(shells, key, entry)

        if result.success:
            result = Adapter(self.process_shells(shells))
            output += result.output
            self.event.delegate(result.success)

        return {'success': result.success, 'output': output}

    def process_shells_parallel(self, shells):
        """Processing a list of shells parallel."""
        output = []
        success = True
        with closing(multiprocessing.Pool(multiprocessing.cpu_count())) as pool:
            for result in [Adapter(entry) for entry in pool.map(worker, [shell for shell in shells])]:
                output += result.output
                the_shell = [shell for shell in shells if shell['id'] == result.id][0]
                self.__handle_variable(the_shell['entry'], result.output)
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
                                 model=shell['model'], env=shell['env'], item=shell['item'],
                                 dry_run=shell['dry_run'], debug=shell['debug'],
                                 variables=shell['variables'])
            result = Adapter(self.process_shell(get_creator_by_name(shell['creator']), entry, config))
            output += result.output
            self.__handle_variable(entry, result.output)
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
        count = 0
        condition = render(entry['when'], variables=self.pipeline.variables,
                           model=self.pipeline.model, env=self.get_merged_env())

        if Condition.evaluate("" if condition is None else condition):
            if len(self.pipeline.options.tags) == 0:
                return True

            if 'tags' in entry:
                for tag in self.pipeline.options.tags:
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
            config = ShellConfig(script=self.pipeline.data.hooks.cleanup,
                                 model=self.pipeline.model, env=env,
                                 dry_run=self.pipeline.options.dry_run,
                                 debug=self.pipeline.options.debug)
            cleanup_shell = Bash(config)
            for line in cleanup_shell.process():
                output.append(line)
                self.logger.info(" | %s", line)
        return output

    def __handle_variable(self, shell_entry, output):
        """
        Saving output for configured variable name.

        Args:
            shell_entry(dict): shell based configuration (shell, docker container or Python).
            output: list of strings representing output of last shell
        """
        if 'variable' in shell_entry:
            variable_name = shell_entry['variable']
            self.pipeline.variables[variable_name] = "\n".join(output)
