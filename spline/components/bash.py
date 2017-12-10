"""
   Executing a bash script.

.. module:: bash
    :platform: Unix
    :synopsis: Executing a bash script.
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
# pylint: disable=too-many-instance-attributes
import os
import shlex
import subprocess
import tempfile
from ..tools.filters import render
from ..tools.logger import Logger
from ..tools.event import Event


class Bash(object):
    """Wrapper for Bash execution."""

    def __init__(self, script, title='', model=None, env=None):
        """Initialize with Bash code and optional environment variables."""
        self.event = Event.create(__name__)
        self.logger = Logger.get_logger(__name__)
        self.success = False
        self.script = script
        self.model = model
        self.env = os.environ.copy()
        self.env.update({} if env is None else env)

        if len(title) > 0:
            self.logger.info(title)

        self.stdout = subprocess.PIPE
        self.stderr = subprocess.STDOUT
        self.shell = False
        self.exit_code = 0

    @staticmethod
    def creator(shell_parameters, model, env):
        """Creator function for creating an instance of a Bash."""
        title = '' if 'title' not in shell_parameters else shell_parameters['title']
        return Bash(script=shell_parameters['script'], title=title, model=model, env=env)

    def update_script_filename(self, filename):
        """Writing current script path and filename into environment variables."""
        self.env.update({'PIPELINE_BASH_FILE': filename})

    def create_file_for(self, script):
        """Create a temporary, executable bash file."""
        temp = tempfile.NamedTemporaryFile(
            prefix="pipeline-script-", mode='w+t', suffix=".sh", delete=False)

        self.update_script_filename(temp.name)
        rendered_script = render(script, model=self.model, env=self.env)

        if os.path.isfile(rendered_script):
            content = str(open(rendered_script).read())
            temp.writelines(content)
        else:
            temp.writelines("#!/bin/bash\n" + rendered_script)
        temp.close()
        # make Bash script executable
        os.chmod(temp.name, 777)
        return temp.name

    def process(self):
        """Running the Bash code."""
        try:
            temp_filename = self.create_file_for(self.script)
            self.logger.info("Running script %s", temp_filename)
            args = shlex.split("bash %s" % temp_filename)

            process = subprocess.Popen(
                args, stdout=self.stdout, stderr=self.stderr, shell=self.shell, env=self.env)
            out, _ = process.communicate()
            for line in out.split(b"\n"):
                yield line.decode('ascii')
            self.exit_code = process.returncode
            if process.returncode == 0:
                self.logger.info("Exit code has been %d", process.returncode)
                self.success = True
            else:
                self.logger.error("Exit code has been %d", process.returncode)
                self.success = False
        except OSError as exception:
            self.exit_code = 1
            yield str(exception)
        finally:
            # removing script
            os.remove(temp_filename)

            if self.exit_code == 0:
                self.event.succeeded()
            else:
                self.event.failed(exit_code=self.exit_code)
