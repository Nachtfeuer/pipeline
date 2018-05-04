"""Wrapper for packer configuration and tool."""
# Copyright (c) 2018 Thomas Lehmann
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
# pylint: disable=useless-super-delegation
import os
from spline.components.bash import Bash
from spline.tools.filters import render
from spline.tools.stream import write_temporary_file


class Packer(Bash):
    """
    Wrapper for packer configuration and tool.

    .. inheritance-diagram:: Image
    """

    def __init__(self, config):
        """Initialize with Bash code (do not call it directly)."""
        super(Packer, self).__init__(config)

    @staticmethod
    def creator(_, config):
        """Creator function for creating an instance of a Packer image script."""
        packer_script = render(config.script, model=config.model, env=config.env,
                               variables=config.variables, item=config.item)
        filename = "packer.dry.run.see.comment"

        if not config.dry_run:
            # writing Packer file (JSON)
            filename = write_temporary_file(packer_script, 'packer-', '.json')
            packer_script = ''

        # rendering the Bash script for generating the Packer image
        template_file = os.path.join(os.path.dirname(__file__), 'templates/packer-image.sh.j2')

        with open(template_file) as handle:
            template = handle.read()
            config.script = render(template, debug=config.debug,
                                   packer_content=packer_script,
                                   packer_filename=filename)

        return Packer(config)
