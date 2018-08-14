"""Executing a bash script."""
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
# pylint: disable=too-many-instance-attributes
import contextlib
import sys
import os
import shlex
import subprocess  # nosec
import tempfile


from spline.tools.filters import render
from spline.tools.logger import Logger
from spline.tools.event import Event


@contextlib.contextmanager
def managed_process(process):
    """Wrapper for subprocess.Popen to work across various Python versions, when using the with syntax."""
    try:
        yield process
    finally:
        for stream in [process.stdout, process.stdin, process.stderr]:
            if stream:
                stream.close()
        process.wait()


class Bash(object):
    """Wrapper for Bash execution."""

    def __init__(self, config):
        """
        Initialize with Bash code and optional environment variables.

        Args:
            config(ShellConfig): options for configuring Bash environment and behavior
        """
        self.event = Event.create(__name__)
        self.logger = Logger.get_logger(__name__)
        self.config = config
        self.success = True
        self.env = {}
        self.env.update(config.env)

        self.stdout = subprocess.PIPE
        self.stderr = subprocess.STDOUT
        self.shell = False
        self.exit_code = 0

    @staticmethod
    def creator(_, config):
        """
        Creator function for creating an instance of a Bash.

        Args:
            config (ShellConfig): options for configuring Bash environment and behavior

        Returns:
            Bash: instance of class Bash
        """
        return Bash(config)

    def update_environment_variables(self, filename):
        """Updating OS environment variables and current script path and filename."""
        self.env.update(os.environ.copy())
        self.env.update({'PIPELINE_BASH_FILE': filename})

    def get_temporary_scripts_path(self):
        """
        Get path for temporary scripts.

        Returns:
            str: path for temporary scripts or None if not set
        """
        result = None
        if len(self.config.temporary_scripts_path) > 0:
            if os.path.isdir(self.config.temporary_scripts_path):
                result = self.config.temporary_scripts_path
        return result

    def create_file_for(self, script):
        """
        Create a temporary, executable bash file.

        It also does render given script (string) with the model and
        the provided environment variables and optional also an item
        when using the B{with} field.

        Args:
            script (str): either pather and filename or Bash code.

        Returns:
            str: path and filename of a temporary file.
        """
        temp = tempfile.NamedTemporaryFile(
            prefix="pipeline-script-", mode='w+t', suffix=".sh", delete=False,
            dir=self.get_temporary_scripts_path())

        self.update_environment_variables(temp.name)
        rendered_script = render(script, model=self.config.model, env=self.env, item=self.config.item,
                                 variables=self.config.variables)
        if rendered_script is None:
            self.success = False
            temp.close()
            os.remove(temp.name)
            return None

        to_file_map = {2: lambda s: s.encode('utf-8'), 3: lambda s: s}

        if all(ord(ch) < 128 for ch in rendered_script) and os.path.isfile(rendered_script):
            with open(rendered_script) as handle:
                content = str(handle.read())
                temp.writelines(content)
        else:
            temp.write(u"#!/bin/bash\n%s" % self.render_bash_options())
            temp.write(to_file_map[sys.version_info.major](rendered_script))
        temp.close()
        # make Bash script executable
        os.chmod(temp.name, 0o700)
        return temp.name

    def render_bash_options(self):
        """Rendering Bash options."""
        options = ''
        if self.config.debug:
            options += "set -x\n"
        if self.config.strict:
            options += "set -euo pipefail\n"
        return options

    def process_script(self, filename):
        """Running the Bash code."""
        try:
            with managed_process(subprocess.Popen(shlex.split("bash %s" % filename),
                                                  stdout=self.stdout, stderr=self.stderr,
                                                  shell=self.shell, env=self.env)) as process:  # nosec
                for line in iter(process.stdout.readline, ' '):
                    if not line:
                        break
                    yield line[0:-1].decode('utf-8')
                process.wait()
                self.exit_code = process.returncode
                self.success = (process.returncode == 0)
                if not self.config.internal:
                    if process.returncode == 0:
                        self.logger.info("Exit code has been %d", process.returncode)
                    else:
                        self.logger.error("Exit code has been %d", process.returncode)
        except OSError as exception:
            self.exit_code = 1
            self.success = False
            yield str(exception)

    def process_file(self, filename):
        """Processing one file."""
        if self.config.dry_run:
            if not self.config.internal:
                self.logger.info("Dry run mode for script %s", filename)
            with open(filename) as handle:
                for line in handle:
                    yield line[0:-1] if line[-1] == '\n' else line
        else:
            if not self.config.internal:
                self.logger.info("Running script %s", filename)
            for line in self.process_script(filename):
                yield line

    def process(self):
        """Running the Bash code."""
        temp_filename = self.create_file_for(self.config.script)

        if len(self.config.title) > 0:
            self.logger.info(render(self.config.title, model=self.config.model, env=self.env,
                                    item=self.config.item, variables=self.config.variables))

        if temp_filename is not None:
            try:
                for line in self.process_file(temp_filename):
                    yield line
            finally:
                # removing script
                os.remove(temp_filename)

        if not self.config.internal:
            if self.exit_code == 0:
                self.event.succeeded()
            else:
                self.event.failed(exit_code=self.exit_code)
