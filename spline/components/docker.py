"""
   Generic Docker image and container handling.

.. module:: docker
    :platform: Unix
    :synopsis: Generic Docker image and  container handling.
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


class Container(Bash):
    """Run Docker container and custom Bash code with one script."""

    @contract(config='is_shell_config')
    def __init__(self, config):
        """Initialize with Bash code and optional environment variables."""
        super(Container, self).__init__(config)

    def update_script_filename(self, filename):
        """Writing current script path and filename into environment variables."""
        self.env.update({'PIPELINE_BASH_FILE_ORIGINAL': filename})
        filename = os.path.join('/root/scripts', os.path.basename(filename))
        self.env.update({'PIPELINE_BASH_FILE': filename})

    @staticmethod
    @contract(config='is_shell_config')
    def creator(entry, config):
        """Creator function for creating an instance of a Bash."""
        template_file = os.path.join(os.path.dirname(__file__), 'templates/docker-container.sh.j2')
        template = open(template_file).read()
        wrapped_script = render(template, container={
            'image': 'centos:7' if 'image' not in entry else entry['image'],
            'remove': True if 'remove' not in entry else str(entry['remove']).lower(),
            'background': False if 'background' not in entry else str(entry['background']).lower(),
            'mount': False if 'mount' not in entry else str(entry['mount']).lower(),
            'script': config.script
        })

        config.script = wrapped_script
        return Container(config)


class Image(Bash):
    """Create Docker image and custom Bash code with one script."""

    @contract(config='is_shell_config')
    def __init__(self, config):
        """Initialize with Bash code (do not call it directly)."""
        super(Image, self).__init__(config)

    @staticmethod
    @contract(config='is_shell_config')
    def creator(entry, config):
        """Creator function for creating an instance of a Docker image script."""
        # writing Dockerfile
        dockerfile = render(config.script, model=config.model, env=config.env, item=config.item)

        temp = tempfile.NamedTemporaryFile(
            prefix="dockerfile-", mode='w+t', delete=False)
        temp.writelines(dockerfile)
        temp.close()

        # rendering the Bash script for generating the Docker image
        name = entry['name'] + "-%s" % os.getpid() if entry['unique'] else entry['name']
        template_file = os.path.join(os.path.dirname(__file__), 'templates/docker-image.sh.j2')
        template = open(template_file).read()
        config.script = render(template, name=name, tag=entry['tag'], dockerfile=temp.name)

        return Image(config)
