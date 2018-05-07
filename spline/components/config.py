"""Config classes with validation."""
# Copyright (c) 2017 Thomas Lehmann
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
# pylint: disable=too-many-instance-attributes
import logging
from schema import Schema, SchemaError, And, Or, Optional, Regex
from spline.tools.adapter import Adapter


class ShellConfig(object):
    """Config data for Bash based objects."""

    @staticmethod
    def schema():
        """Provide schema for shell configuration."""
        return Schema({
            'script': And(Or(type(' '), type(u' ')), len),
            Optional('title', default=''): str,
            Optional('model', default={}): {Optional(And(str, len)): object},
            Optional('env', default={}): {Optional(And(str, len)): And(str, len)},
            Optional('item', default=None): object,
            Optional('dry_run', default=False): bool,
            Optional('debug', default=False): bool,
            Optional('strict', default=False): bool,
            Optional('variables', default={}): {
                Optional(And(Or(type(' '), type(u' ')), len, Regex(r'([a-zA-Z][_a-zA-Z]*)'))):
                    Or(type(' '), type(u' '))
            },
            Optional('temporary_scripts_path', default=''): Or(type(''), type(u'')),
            Optional('internal', default=False): bool
        })

    def __init__(self, **kwargs):
        """Initializing and validating fields."""
        try:
            arguments = Adapter(ShellConfig.schema().validate(kwargs))
            self.script = arguments.script
            self.title = arguments.title
            self.model = arguments.model.data
            self.env = arguments.env.data
            self.item = arguments.item
            self.dry_run = arguments.dry_run
            self.debug = arguments.debug
            self.strict = arguments.strict
            self.variables = arguments.variables.data
            self.temporary_scripts_path = arguments.temporary_scripts_path
            self.internal = arguments.internal
        except SchemaError as exception:
            logging.getLogger(__name__).error(exception)
            raise RuntimeError(str(exception))


class ApplicationOptions(object):
    """Application wide configuation (usually via command line options)."""

    SCHEMA = {
        'definition': And(str, len),
        Optional('matrix_tags', default=''): Or(type(''), type(u'')),
        Optional('tags', default=''): Or(type(''), type(u'')),
        Optional('validate_only', default=False): bool,
        Optional('dry_run', default=False): bool,
        Optional('event_logging', default=False): bool,
        Optional('logging_config', default=''): Or(type(''), type(u'')),
        Optional('debug', default=False): bool,
        Optional('strict', default=False): bool,
        Optional('report', default='off'):
            And(str, lambda s: s in ['off', 'json', 'html']),
        Optional('temporary_scripts_path', default=''): Or(type(''), type(u''))
    }

    def __init__(self, **kwargs):
        """
        Initializing and validating fields.

        Args:
            kwargs (dict): application command line options.
        """
        try:
            arguments = Adapter(Schema(ApplicationOptions.SCHEMA).validate(kwargs))
            self.definition = arguments.definition
            self.matrix_tags = [entry for entry in arguments.matrix_tags.split(',') if len(entry) > 0]
            self.tags = [entry for entry in arguments.tags.split(',') if len(entry) > 0]
            self.validate_only = arguments.validate_only
            self.dry_run = arguments.dry_run
            self.event_logging = arguments.event_logging
            self.logging_config = arguments.logging_config
            self.debug = arguments.debug
            self.strict = arguments.strict
            self.report = arguments.report
            self.temporary_scripts_path = arguments.temporary_scripts_path
        except SchemaError as exception:
            logging.getLogger(__name__).error(exception)
            raise RuntimeError(str(exception))
