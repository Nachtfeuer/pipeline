"""
   Pipeline is list of stages.

.. module:: hooks
    :platform: Unix, Windows
    :synopis: Pipeline is list of stages.
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
import re

from components.bash import Bash
from components.stage import Stage


class PipelineData(object):
    """Class for keeping pipeline data."""

    def __init__(self, pipeline, tags=[], hooks=None):
        """Initializing pipeline with definition (loaded from a yaml file)."""
        self.pipeline = pipeline
        self.env_list = [{}, {}, {}]
        self.tags = tags
        self.hooks = hooks


class Pipeline(object):
    """Class for processing a pipeline definition."""

    def __init__(self, pipeline, env={}, tags=[], hooks=None):
        """Initializing pipeline with definition (loaded from a yaml file)."""
        self.data = PipelineData(pipeline, tags, hooks)
        self.data.env_list[0].update(env)

    def run(self):
        """Processing the whole pipeline definition."""
        for entry in self.data.pipeline:
            key = entry.keys()[0]
            if key == "env":
                self.data.env_list[0].update(entry[key])
                logging.debug("Updating environment at level 0 with %s",
                              self.data.env_list[0])
                continue

            if key.startswith("stage"):
                stage = Stage(self, re.match(r"stage\((?P<title>.*)\)", key).group("title"))
                stage.process(entry[key])

        if len(self.data.hooks.cleanup) > 0:
            env = self.data.env_list[0].copy()
            env.update({'PIPELINE_RESULT': 'SUCCESS'})
            env.update({'PIPELINE_SHELL_EXIT_CODE': '0'})
            cleanup_shell = Bash(self.data.hooks.cleanup, env)
            for line in cleanup_shell.process():
                logging.info(" | %s", line)
