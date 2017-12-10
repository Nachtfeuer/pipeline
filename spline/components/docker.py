"""
   Generic Docker container handling.

.. module:: docker
    :platform: Unix
    :synopsis: Generic Docker container handling.
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
from .bash import Bash


class Container(Bash):
    """Run Docker container and custom Bash code with one script."""

    TEMPLATE = """
if [ $# -eq 0 ]; then
    BACKGROUND_MODE=-i
    MOUNT=

    if [ "%(background)s" == "true" ]; then
        BACKGROUND_MODE=-d
    fi

    if [ "%(mount)s" == "true" ]; then
        MOUNT="-v $PWD:/mnt/host"
    fi

    docker run --rm=%(remove)s \
        -v $(dirname ${PIPELINE_BASH_FILE_ORIGINAL}):/root/scripts ${MOUNT} \
        -e UID=$(id -u) -e GID=$(id -g) {{ env|docker_environment }} \
        --label="pipeline=${PIPELINE_PID}" \
        --label="pipeline-stage=${PIPELINE_STAGE}" \
        --label="creator=$$" \
        --label="context=pipeline" \
        ${BACKGROUND_MODE} %(image)s \
        ${PIPELINE_BASH_FILE} INIT
else
    %(script)s
fi
"""

    def __init__(self, script, title='', model=None, env=None):
        """Initialize with Bash code and optional environment variables."""
        super(Container, self).__init__(script, title, model, env)

    def update_script_filename(self, filename):
        """Writing current script path and filename into environment variables."""
        self.env.update({'PIPELINE_BASH_FILE_ORIGINAL': filename})
        filename = os.path.join('/root/scripts', os.path.basename(filename))
        self.env.update({'PIPELINE_BASH_FILE': filename})

    @staticmethod
    def creator(shell_parameters, model, env):
        """Creator function for creating an instance of a Bash."""
        title = '' if 'title' not in shell_parameters else shell_parameters['title']
        image = 'centos:7' if 'image' not in shell_parameters else shell_parameters['image']
        remove = True if 'remove' not in shell_parameters else shell_parameters['remove']
        background = False if 'background' not in shell_parameters else shell_parameters['background']
        mount = False if 'mount' not in shell_parameters else shell_parameters['mount']

        wrapped_script = Container.TEMPLATE % {
            'image': image,
            'remove': str(remove).lower(),
            'background': str(background).lower(),
            'mount': str(mount).lower(),
            'script': shell_parameters['script']
        }
        return Container(script=wrapped_script, title=title, model=model, env=env)
