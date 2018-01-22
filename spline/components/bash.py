"""
Executing a bash script.

License::

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
# pylint: disable=too-many-instance-attributes
import sys
import os
import shlex
import subprocess  # nosec
import tempfile


from spline.tools.filters import render
from spline.tools.logger import Logger
from spline.tools.event import Event


class Bash(object):
    """Wrapper for Bash execution."""

    def __init__(self, config):
        """
        Initialize with Bash code and optional environment variables.

        @type  config: ShellConfig
        @param config: options for configuring Bash environment and behavior
        """
        self.event = Event.create(__name__)
        self.logger = Logger.get_logger(__name__)
        self.config = config
        self.success = True
        self.env = os.environ.copy()
        self.env.update(config.env)

        if len(config.title) > 0:
            self.logger.info(config.title)

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

    def update_script_filename(self, filename):
        """Writing current script path and filename into environment variables."""
        self.env.update({'PIPELINE_BASH_FILE': filename})

    def create_file_for(self, script):
        """
        Create a temporary, executable bash file.

        It also does render given script (string) with the model and
        the provided environment variables and optional also an item
        when using the B{with} field.

        @type script: str
        @param script: either pather and filename or Bash code.
        @rtype: str
        @return: path and filename of a temporary file.
        """
        temp = tempfile.NamedTemporaryFile(
            prefix="pipeline-script-", mode='w+t', suffix=".sh", delete=False)

        self.update_script_filename(temp.name)
        rendered_script = render(script, model=self.config.model, env=self.env, item=self.config.item,
                                 variables=self.config.variables)
        if rendered_script is None:
            self.success = False
            temp.close()
            os.remove(temp.name)
            return None

        to_file_map = {2: lambda s: s.encode('utf-8'), 3: lambda s: s}

        if all(ord(ch) < 128 for ch in rendered_script) and os.path.isfile(rendered_script):
            content = str(open(rendered_script).read())
            temp.writelines(content)
        else:
            temp.write(u"#!/bin/bash\n%s" % ("set -x\n" if self.config.debug else ''))
            temp.write(to_file_map[sys.version_info.major](rendered_script))
        temp.close()
        # make Bash script executable
        os.chmod(temp.name, 777)  # nosec
        return temp.name

    def process_script(self, filename):
        """Running the Bash code."""
        try:
            process = subprocess.Popen(
                shlex.split("bash %s" % filename),
                stdout=self.stdout, stderr=self.stderr,
                shell=self.shell, env=self.env)  # nosec

            for line in iter(process.stdout.readline, ' '):
                if not line:
                    break
                yield line[0:-1].decode('utf-8')
            process.wait()
            self.exit_code = process.returncode
            self.success = (process.returncode == 0)
            if process.returncode == 0:
                self.logger.info("Exit code has been %d", process.returncode)
            else:
                self.logger.error("Exit code has been %d", process.returncode)
        except OSError as exception:
            self.exit_code = 1
            yield str(exception)

    def process(self):
        """Running the Bash code."""
        temp_filename = self.create_file_for(self.config.script)
        if temp_filename is not None:
            if self.config.dry_run:
                self.logger.info("Dry run mode for script %s", temp_filename)
                for line in open(temp_filename):
                    yield line[0:-1] if line[-1] == '\n' else line
            else:
                self.logger.info("Running script %s", temp_filename)
                for line in self.process_script(temp_filename):
                    yield line

            # removing script
            os.remove(temp_filename)

        if self.exit_code == 0:
            self.event.succeeded()
        else:
            self.event.failed(exit_code=self.exit_code)
