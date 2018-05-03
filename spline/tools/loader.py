"""Yaml specific loader for including other yaml files."""
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
# pylint: disable=too-many-ancestors
import os
from yaml import SafeLoader, ScalarNode, safe_load
from yaml import load as yaml_load


class Loader(SafeLoader):
    """Yaml specific loader for including other yaml files."""

    def __init__(self, stream):
        """Initialize loader for specific includes."""
        super(Loader, self).__init__(stream)
        Loader.add_constructor('!include', Loader.include)

    def include(self, node):
        """Include the defined yaml file."""
        result = None
        if isinstance(node, ScalarNode):
            result = Loader.include_file(self.construct_scalar(node))
        else:
            raise RuntimeError("Not supported !include on type %s" % type(node))
        return result

    @staticmethod
    def include_file(filename):
        """Load another yaml file (no recursion)."""
        if os.path.isfile(filename):
            with open(filename) as handle:
                return safe_load(handle)
        raise RuntimeError("Include file %s doesn't exist!" % filename)

    @staticmethod
    def load(filename):
        """"Load yaml file with specific include loader."""
        if os.path.isfile(filename):
            with open(filename) as handle:
                return yaml_load(handle, Loader=Loader)  # nosec
        raise RuntimeError("File %s doesn't exist!" % filename)
