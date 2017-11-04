"""
   Executing a bash script.

.. module:: bash
    :platform: Unix
    :synopis: Executing a bash script.
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
from jinja2 import Template
from ..tools.logger import Logger
from ..tools.event import Event


class Bash(object):
    """Wrapper for Bash execution."""

    def __init__(self, script, title='', env=None):
        """Initialize with Bash code and optional environment variables."""
        self.event = Event.create(__name__)
        self.logger = Logger.get_logger(__name__)
        self.success = False

        template = Template(script)
        rendered_script = template.render(env=env)
        self.temp_filename = Bash.create_file_for(rendered_script)

        if len(title) > 0:
            self.logger.info(title)
        self.logger.info("Running script %s", self.temp_filename)

        self.args = shlex.split("bash %s" % self.temp_filename)
        self.stdout = subprocess.PIPE
        self.stderr = subprocess.STDOUT
        self.shell = False
        self.env = os.environ.copy()
        self.env.update({} if env is None else env)
        self.env.update({'PIPELINE_BASH_FILE': self.temp_filename})
        self.exit_code = 0

    @staticmethod
    def creator(shell_parameters, env):
        """Creator function for creating an instance of a Bash."""
        title = '' if 'title' not in shell_parameters else shell_parameters['title']
        return Bash(script=shell_parameters['script'], title=title, env=env)

    @staticmethod
    def create_file_for(script):
        """Create a temporary, executable bash file."""
        temp = tempfile.NamedTemporaryFile(
            prefix="pipeline-script-", mode='w+t', suffix=".sh", delete=False)
        if os.path.isfile(script):
            content = str(open(script).read())
            temp.writelines(content)
        else:
            temp.writelines("#!/bin/bash\n" + script)
        temp.close()
        # make Bash script executable
        os.chmod(temp.name, 0777)
        return temp.name

    def process(self):
        """Running the Bash code."""
        try:
            process = subprocess.Popen(
                self.args, stdout=self.stdout, stderr=self.stderr, shell=self.shell, env=self.env)
            out, _ = process.communicate()
            for line in out.split("\n"):
                yield line
            self.exit_code = process.returncode
            self.logger.info("Exit code has been %d", process.returncode)
            self.success = True if process.returncode == 0 else False
        except OSError as exception:
            self.exit_code = 1
            yield str(exception)
        finally:
            # removing script
            os.remove(self.temp_filename)

            if self.exit_code == 0:
                self.event.succeeded()
            else:
                self.event.failed(exit_code=self.exit_code)
