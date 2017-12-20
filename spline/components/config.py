"""
   Config classes with validation.

.. module:: config
    :platform: all
    :synopsis: Config classes with validation.
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
from schema import Schema, SchemaError, And, Optional
from ..tools.adapter import Adapter


class ShellConfig(object):
    """Config data for Bash based objects."""

    SCHEMA = {
        'script': And(str, len),
        Optional('title', default=''): str,
        Optional('model', default={}): {Optional(And(str, len)): object},
        Optional('env', default={}): {Optional(And(str, len)): And(str, len)},
        Optional('item', default=None): object
    }

    def __init__(self, **kwargs):
        """Initializing and validating fields."""
        try:
            arguments = Adapter(Schema(ShellConfig.SCHEMA).validate(kwargs))
            self.script = arguments.script
            self.title = arguments.title
            self.model = arguments.model.data
            self.env = arguments.env.data
            self.item = arguments.item
        except SchemaError as exception:
            logging.getLogger(__name__).error(exception)
            raise RuntimeError(str(exception))
