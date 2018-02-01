"""Validation for the pipeline data format."""
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
import logging
from schema import Schema, SchemaError, Optional, Regex, And, Or
from spline.tools.condition import Condition


class Validator(object):
    """Validator for the Pythonic pipeline definition."""

    SCHEMA = {
        # optional matrix part of the schema
        Optional(Regex(r'((matrix\(parallel\)|matrix\(ordered\)|matrix))')): And(len, [{
            'name': And(str, len),
            Optional('env'): And(len, {
                Regex(r'([a-zA-Z][_a-zA-Z]*)'): And(str, len)
            }),
            Optional('tags'): And(len, [And(str, len)])
        }]),
        # optional model part of the schema
        Optional('model'): And(len, {
            Regex(r'([a-z][_a-z]*)'): object
        }),
        # optional hooks part of the schema
        Optional('hooks'): {
            'cleanup': {
                'script': And(str, len)
            }
        },
        # mandatory pipeline part of the schema
        'pipeline': And(len, [Or(
            # optional environment variables in a pipeline
            {'env': And(len, {
                Regex(r'([a-zA-Z][_a-zA-Z]*)'): And(str, len)
            })},
            {Regex(r'(stage\(.+\))'): And(len, [Or(
                # optional environment variables in a stage
                {'env': And(len, {
                    Regex(r'([a-zA-Z][_a-zA-Z]*)'): And(str, len)
                })},
                # optional tasks
                {Regex(r'((tasks\(parallel\)|matrix\(tasks\)|tasks))'): And(len, [
                    # optional environment variables
                    {Optional('env'): And(len, {
                        Regex(r'([a-zA-Z][_a-zA-Z]*)'): And(str, len)
                    })},
                    # optional shell task
                    {Optional('shell'): {
                        'script': And(Or(type(' '), type(u' ')), len),
                        Optional('title'): And(str, len),
                        Optional('tags'): And([And(str, len)], len),
                        Optional('with'): And(len, [object]),
                        Optional('variable'):
                            And(Or(type(' '), type(u' ')), len, Regex(r'([a-zA-Z][_a-zA-Z]*)')),
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }},
                    # optional Docker container task
                    {Optional('docker(container)'): {
                        'script': And(str, len),
                        Optional('image'): And(str, len),
                        Optional('title'): And(str, len),
                        Optional('mount', default=False): bool,
                        Optional('background', default=False): bool,
                        Optional('remove', default=True): bool,
                        Optional('tags'): And([And(str, len)], len),
                        Optional('with'): And(len, [object]),
                        Optional('variable'):
                            And(Or(type(' '), type(u' ')), len, Regex(r'([a-zA-Z][_a-zA-Z]*)')),
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }},
                    # optional Docker image task
                    {Optional('docker(image)'): {
                        'script': And(str, len),
                        'name': And(str, len),
                        'tag': And(str, len),
                        Optional('unique', default=True): bool,
                        Optional('tags'): And([And(str, len)], len),
                        Optional('with'): And(len, [object]),
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }},
                    # optional Python script
                    {Optional('python'): {
                        'script': And(str, len),
                        Optional('title'): And(str, len),
                        Optional('tags'): And([And(str, len)], len),
                        Optional('with'): And(len, [object]),
                        Optional('variable'):
                            And(Or(type(' '), type(u' ')), len, Regex(r'([a-zA-Z][_a-zA-Z]*)')),
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }}
                ])}  # end of tasks
            )])},  # end of stage
        )])  # end of pipeline
    }  # end of schema

    @staticmethod
    def validate(data):
        """Validate data against the schema."""
        try:
            return Schema(Validator.SCHEMA).validate(data)
        except SchemaError as exception:
            logging.getLogger(__name__).error(exception)
            return None
