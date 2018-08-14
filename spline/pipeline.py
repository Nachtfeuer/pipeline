"""Pipeline is list of stages."""
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
import os
import re

from spline.components.bash import Bash
from spline.components.stage import Stage
from spline.components.config import ShellConfig
from spline.tools.logger import Logger
from spline.tools.event import Event


class PipelineData(object):
    """Class for keeping pipeline data."""

    def __init__(self, hooks=None):
        """Initializing pipeline with definition (loaded from a yaml file)."""
        self.pid = str(os.getpid())
        self.env_list = [{'PIPELINE_PID': self.pid}, {}, {}]
        self.hooks = hooks


class Pipeline(object):
    """Class for processing a pipeline definition."""

    def __init__(self, model=None, env=None, options=None):
        """
        Initializing pipeline with definition (loaded from a yaml file).

        Args:
            model (dict): if you have a model defined in your pipeline definition (yaml)
            env (dict): the env as defined (if) per matrix
            options (dict): command line options for spline
        """
        self.event = Event.create(__name__)
        self.options = options
        self.model = {} if not isinstance(model, dict) else model
        self.data = PipelineData()
        self.data.env_list[0].update([] if env is None else env)
        self.logger = Logger.get_logger(__name__)
        self.variables = {}

    @property
    def hooks(self):
        """Get hooks."""
        return self.data.hooks

    @hooks.setter
    def hooks(self, value):
        """Set hooks."""
        self.data.hooks = value

    def cleanup(self):
        """Run cleanup script of pipeline when hook is configured."""
        if self.data.hooks and len(self.data.hooks.cleanup) > 0:
            env = self.data.env_list[0].copy()
            env.update({'PIPELINE_RESULT': 'SUCCESS', 'PIPELINE_SHELL_EXIT_CODE': '0'})
            config = ShellConfig(script=self.data.hooks.cleanup, model=self.model,
                                 env=env, dry_run=self.options.dry_run,
                                 debug=self.options.debug, strict=self.options.strict,
                                 temporary_scripts_path=self.options.temporary_scripts_path)
            cleanup_shell = Bash(config)
            for line in cleanup_shell.process():
                yield line

    def process(self, pipeline):
        """Processing the whole pipeline definition."""
        output = []
        for entry in pipeline:
            key = list(entry.keys())[0]
            # an environment block can be repeated
            if key == "env":
                self.data.env_list[0].update(entry[key])
                self.logger.debug("Updating environment at level 0 with %s",
                                  self.data.env_list[0])
                continue

            # after validation it can't be anything else but a stage
            # and the title is inside the round brackets:
            stage = Stage(self, re.match(r"stage\((?P<title>.*)\)", key).group("title"))
            result = stage.process(entry[key])
            output += result['output']
            if not result['success']:
                return {'success': False, 'output': output}

        # logging the output of the cleanup shell when registered
        for line in self.cleanup():
            output.append(line)
            self.logger.info(" | %s", line)

        self.event.succeeded()
        return {'success': True, 'output': output}
