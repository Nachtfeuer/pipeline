"""Provide custom Jinja2 filters."""
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
from jinja2 import Environment
from jinja2.exceptions import TemplateSyntaxError, UndefinedError
from spline.tools.logger import Logger


def render(value, **kwargs):
    """
    Use Jinja2 rendering for given text an key key/values.

    Args:
        value (str): the template to be rendered.
        kwargs (dict): named parameters representing available variables
                       inside the template.

    >>> model = {"message": "hello world 1!"}
    >>> rendered_text = render("{{model.message}}", model=model)
    >>> rendered_text == 'hello world 1!'
    True
    >>> model = {"message": "hello world 2!", "template": "{{ model.message }}"}
    >>> rendered_text = render("{{ model.template|render(model=model) }}", model=model)
    >>> rendered_text == 'hello world 2!'
    True

    The pipeline process is all about Bash code (inside and outside Docker) and
    autoescaping wouldn't help. Usually the pipeline runs in a isolated environment
    and there should not be any injection from outside; that's why: nosec.
    """
    try:
        environment = Environment(autoescape=False)  # nosec
        environment.filters['render'] = render
        environment.filters['docker_environment'] = docker_environment
        environment.filters['find_matrix'] = find_matrix
        environment.filters['find_stages'] = find_stages
        template = environment.from_string(value)
        return template.render(**kwargs)
    except UndefinedError as exception:
        Logger.get_logger(__name__).error("render(undefined): %s", exception)
    except TemplateSyntaxError as exception:
        Logger.get_logger(__name__).error("render(syntax error): %s", exception)
    return None


def docker_environment(env):
    """
    Transform dictionary of environment variables into Docker -e parameters.

    >>> result = docker_environment({'param1': 'val1', 'param2': 'val2'})
    >>> result in ['-e "param1=val1" -e "param2=val2"', '-e "param2=val2" -e "param1=val1"']
    True
    """
    return ' '.join(
        ["-e \"%s=%s\"" % (key, value.replace("$", "\\$").replace("\"", "\\\"").replace("`", "\\`"))
         for key, value in env.items()])


def find_matrix(document):
    """
    Find  **matrix** in document.

    The spline syntax allows following definitions:
        - **'matrix'** - ordered execution of each pipeline (short form)
        - **'matrix(ordered)'** - ordered execution of each pipeline (more readable form)
        - **'matrix(parallel)'** - parallel execution of each pipeline

    Args:
        document (dict): validated spline document loaded from a yaml file.

    Returns:
        list: matrix as a part of the spline document or an empty list if not given.

    >>> find_matrix({})
    []
    >>> find_matrix({'matrix': [1]})
    [1]
    >>> find_matrix({'matrix(ordered)': [2]})
    [2]
    >>> find_matrix({'matrix(parallel)': [3]})
    [3]
    """
    return document['matrix'] if 'matrix' in document \
        else document['matrix(ordered)'] if 'matrix(ordered)' in document \
        else document['matrix(parallel)'] if 'matrix(parallel)' in document \
        else []


def find_stages(document):
    """
    Find  **stages** in document.

    Args:
        document (dict): validated spline document loaded from a yaml file.

    Returns:
        list: stages as a part of the spline document or an empty list if not given.

    >>> find_stages({'pipeline': [{'stage(Prepare)':1}, {'stage(Build)':1}, {'stage(Deploy)':2}]})
    ['Prepare', 'Build', 'Deploy']
    """
    names = []
    if 'pipeline' in document:
        for entry in document['pipeline']:
            # each entry is dictionary with one key only
            key, _ = list(entry.items())[0]
            if key.startswith("stage("):
                names.append(key.replace('stage(', '').replace(')', ''))
    return names
