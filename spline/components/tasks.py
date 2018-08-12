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
import os
import multiprocessing
from contextlib import closing
import ast
from spline.components.bash import Bash
from spline.components.docker import Container, Image
from spline.components.packer import Packer
from spline.components.ansible import Ansible
from spline.components.script import Script
from spline.components.config import ShellConfig
from spline.tools.logger import Logger
from spline.tools.event import Event
from spline.tools.adapter import Adapter
from spline.tools.filters import render
from spline.tools.condition import Condition


def get_creator_by_name(name):
    """
    Get creator function by name.

    Args:
        name (str): name of the creator function.

    Returns:
        function: creater function.
    """
    return {'docker(container)': Container.creator,
            'shell': Bash.creator, 'docker(image)': Image.creator,
            'python': Script.creator, 'packer': Packer.creator,
            'ansible(simple)': Ansible.creator}[name]


def worker(data):
    """Running on shell via multiprocessing."""
    creator = get_creator_by_name(data['creator'])
    shell = creator(data['entry'],
                    ShellConfig(script=data['entry']['script'],
                                title=data['entry']['title'] if 'title' in data['entry'] else '',
                                model=data['model'], env=data['env'], item=data['item'],
                                dry_run=data['dry_run'], debug=data['debug'], strict=data['strict'],
                                variables=data['variables'],
                                temporary_scripts_path=data['temporary_scripts_path']))
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

    def get_merged_env(self, include_os=False):
        """
        Copying and merging environment variables.

        Args:
            include_os (bool): when true then include the environment variables (default: False)

        Returns:
            dict: environment variables as defined in the pipeline
                  (optional including system environment variables).
        """
        env = {}
        if include_os:
            env.update(os.environ.copy())
        for level in range(3):
            env.update(self.pipeline.data.env_list[level].copy())
        return env

    def prepare_shell_data(self, shells, key, entry):
        """Prepare one shell or docker task."""
        if self.can_process_shell(entry):
            if key in ['python']:
                entry['type'] = key

            if 'with' in entry and isinstance(entry['with'], str):
                rendered_with = ast.literal_eval(render(entry['with'],
                                                        variables=self.pipeline.variables,
                                                        model=self.pipeline.model,
                                                        env=self.get_merged_env(include_os=True)))
            elif 'with' in entry:
                rendered_with = entry['with']
            else:
                rendered_with = ['']

            for item in rendered_with:
                shells.append({
                    'id': self.next_task_id,
                    'creator': key,
                    'entry': entry,
                    'model': self.pipeline.model,
                    'env': self.get_merged_env(),
                    'item': item,
                    'dry_run': self.pipeline.options.dry_run,
                    'debug': self.pipeline.options.debug,
                    'strict': self.pipeline.options.strict,
                    'variables': self.pipeline.variables,
                    'temporary_scripts_path': self.pipeline.options.temporary_scripts_path})
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

            if (not self.parallel or key == 'env') and len(shells) > 0:
                result = Adapter(self.process_shells(shells))
                output += result.output
                shells = []
                if not result.success:
                    break

            if key == 'env':
                self.pipeline.data.env_list[2].update(entry)

            elif key in ['shell', 'docker(container)', 'docker(image)', 'python',
                         'packer', 'ansible(simple)']:
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
                                 dry_run=shell['dry_run'], debug=shell['debug'], strict=shell['strict'],
                                 variables=shell['variables'],
                                 temporary_scripts_path=shell['temporary_scripts_path'])
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
                           model=self.pipeline.model, env=self.get_merged_env(include_os=True))

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
                                 debug=self.pipeline.options.debug,
                                 strict=self.pipeline.options.strict,
                                 temporary_scripts_path=self.pipeline.options.temporary_scripts_path)
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
