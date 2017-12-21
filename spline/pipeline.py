"""
   Pipeline is list of stages.

.. module:: pipeline
    :platform: Unix
    :synopsis: Pipeline is list of stages.
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
# pylint: disable=too-many-arguments
import os
import re

from .components.bash import Bash
from .components.stage import Stage
from .components.config import ShellConfig
from .tools.logger import Logger
from .tools.event import Event


class PipelineData(object):
    """Class for keeping pipeline data."""

    def __init__(self, pipeline, tags=None, hooks=None):
        """Initializing pipeline with definition (loaded from a yaml file)."""
        self.pid = str(os.getpid())
        self.pipeline = pipeline
        self.env_list = [{'PIPELINE_PID': self.pid}, {}, {}]
        self.tags = [] if tags is None else tags
        self.hooks = hooks


class Pipeline(object):
    """Class for processing a pipeline definition."""

    def __init__(self, pipeline, model=None, env=None, tags=None, hooks=None):
        """Initializing pipeline with definition (loaded from a yaml file)."""
        self.event = Event.create(__name__)
        self.model = {} if not isinstance(model, dict) else model
        self.data = PipelineData(pipeline, [] if tags is None else tags, hooks)
        self.data.env_list[0].update([] if env is None else env)
        self.logger = Logger.get_logger(__name__)

    def cleanup(self):
        """Run cleanup script of pipeline when hook is configured."""
        if self.data.hooks and len(self.data.hooks.cleanup) > 0:
            env = self.data.env_list[0].copy()
            env.update({'PIPELINE_RESULT': 'SUCCESS'})
            env.update({'PIPELINE_SHELL_EXIT_CODE': '0'})
            config = ShellConfig(script=self.data.hooks.cleanup, model=self.model, env=env)
            cleanup_shell = Bash(config)
            for line in cleanup_shell.process():
                yield line

    def run(self):
        """Processing the whole pipeline definition."""
        output = []
        for entry in self.data.pipeline:
            key = list(entry.keys())[0]
            if key == "env":
                self.data.env_list[0].update(entry[key])
                self.logger.debug("Updating environment at level 0 with %s",
                                  self.data.env_list[0])
                continue

            if key.startswith("stage"):
                stage = Stage(self, re.match(r"stage\((?P<title>.*)\)", key).group("title"))
                result = stage.process(entry[key])
                output += result['output']
                if not result['success']:
                    return {'success': False, 'output': output}

        for line in self.cleanup():
            output.append(line)
            self.logger.info(" | %s", line)

        self.event.succeeded()
        return {'success': True, 'output': output}
