"""
   Generic script that can handle script languages like Python.

.. module:: script
    :platform: Unix
    :synopsis: Generic script that can handle script languages like Python.
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
# pylint: disable=useless-super-delegation
import os
import tempfile

from contracts import contract

from .bash import Bash
from ..tools.filters import render


class Script(Bash):
    """Run scripts like Python in a Bash environment."""

    @contract(config='is_shell_config')
    def __init__(self, config):
        """Initialize with Bash code and optional environment variables."""
        super(Script, self).__init__(config)

    @staticmethod
    @contract(config='is_shell_config')
    def creator(entry, config):
        """Preparing and creating script."""
        script = render(config.script, model=config.model, env=config.env, item=config.item)

        temp = tempfile.NamedTemporaryFile(prefix="script-", suffix=".py", mode='w+t', delete=False)
        temp.writelines(script)
        temp.close()

        language = 'python' if 'type' not in entry else entry['type']
        template_file = os.path.join(os.path.dirname(__file__), 'templates/%s-script.sh.j2' % language)
        template = open(template_file).read()

        config.script = render(template, script=temp.name)
        return Script(config)
