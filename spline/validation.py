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
    """
    Validator for the Pythonic pipeline definition.

     - validates matrix, hooks, model and pipeline as main items in yaml.
     - validates parallel or ordered in matrix and tasks
     - support for Bash, Python, Docker, Packer and Ansible tasks
    """

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
        # you may have any value (any yaml structure as value)
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
                        Optional('with'): And(len, Or(type(' '), type(u' '), [object])),
                        # when set store output of shell task into a variable with this name
                        # can be referenced in jinja templating with {{ variables.name }}
                        Optional('variable'):
                            And(Or(type(' '), type(u' ')), len, Regex(r'([a-zA-Z][_a-zA-Z]*)')),
                        # condition when to run the task
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }},
                    # optional Docker container task
                    {Optional('docker(container)'): {
                        'script': And(str, len),
                        # docker image name and docker tag (version)
                        Optional('image'): And(str, len),
                        # the title is printed to the logs (when given)
                        Optional('title'): And(str, len),
                        # when set the mount will be -v $PWD:/mnt/host
                        Optional('mount', default=False): bool,
                        # when set using -d option (docker run)
                        Optional('background', default=False): bool,
                        # when set using --rm option (docker run)
                        Optional('remove', default=True): bool,
                        # when set using --network= option (docker run)
                        Optional('network', default=''): And(str, len),
                        # when set using --labels= option (docker run)
                        Optional('labels'): And(len, {
                            Regex(r'(UL[_A-Z]*)'): And(str, len)
                        }),
                        # when defined used for --tags option (spline --tags=)
                        Optional('tags'): And([And(str, len)], len),
                        Optional('with'): And(len, [object]),
                        # when set store output of docker container task into a variable with this name
                        # can be referenced in jinja templating with {{ variables.name }}
                        Optional('variable'):
                            And(Or(type(' '), type(u' ')), len, Regex(r'([a-zA-Z][_a-zA-Z]*)')),
                        # condition when to run the task
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
                        # condition when to run the task
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }},
                    # optional Python script
                    {Optional('python'): {
                        'script': And(str, len),
                        Optional('title'): And(str, len),
                        Optional('tags'): And([And(str, len)], len),
                        Optional('with'): And(len, [object]),
                        # when set store output of python task into a variable with this name
                        # can be referenced in jinja templating with {{ variables.name }}
                        Optional('variable'):
                            And(Or(type(' '), type(u' ')), len, Regex(r'([a-zA-Z][_a-zA-Z]*)')),
                        # condition when to run the task
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }},
                    # optional Packer task
                    {Optional('packer'): {
                        'script': And(str, len),
                        Optional('tags'): And([And(str, len)], len),
                        Optional('with'): And(len, [object]),
                        # condition when to run the task
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }},
                    # optional Ansible task
                    {Optional('ansible(simple)'): {
                        'script': And(str, len),
                        'inventory': And(str, len),
                        Optional('limit', default=''): And(str, len),
                        Optional('tags'): And([And(str, len)], len),
                        Optional('with'): And(len, [object]),
                        # condition when to run the task
                        Optional('when', default=''): And(str, Condition.is_valid)
                    }}
                ])}  # end of tasks
            )])},  # end of stage
        )])  # end of pipeline
    }  # end of schema

    @staticmethod
    def validate(data):
        """
        Validate data against the schema.

        Args:
            data(dict): data structure to validate.

        Returns:
            dict: data as provided and defaults where defined in schema.
        """
        try:
            return Schema(Validator.SCHEMA).validate(data)
        except SchemaError as exception:
            logging.getLogger(__name__).error(exception)
            return None
