"""
   Provide schema validation.

.. module:: filters
    :platform: Unix
    :synopis: Provide schema validation.
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
from pykwalify.core import Core
from pykwalify.errors import SchemaError
from .logger import Logger


def validate_schema(definition, schema_file):
    """Validate definition agains schema file."""
    logging.getLogger('pykwalify.core').setLevel(logging.WARNING)
    logging.getLogger('pykwalify.rule').setLevel(logging.WARNING)
    core = Core(source_file=definition, schema_files=[schema_file])
    try:
        core.validate(raise_exception=True)
        return True
    except SchemaError as exception:
        for line in str(exception).split("\n"):
            Logger.get_logger(__name__).error(line)
    return False
