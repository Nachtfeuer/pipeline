"""
   Provide custom jinja filters.

.. module:: filters
    :platform: Unix
    :synopis: Provide custom jinja filters.
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
from jinja2 import Environment


def render(value, **kwargs):
    """
    Use Jinja2 rendering for given text an key key/values.

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
    environment = Environment(autoescape=False)  # nosec
    environment.filters['render'] = render
    environment.filters['docker_environment'] = docker_environment
    template = environment.from_string(value)
    return template.render(**kwargs)


def docker_environment(env):
    """
    Transform dictionary of environment variables into Docker -e parameters.

    >>> result = docker_environment({'param1': 'val1', 'param2': 'val2'})
    >>> result in ['-e "param1=val1" -e "param2=val2"', '-e "param2=val2" -e "param1=val1"']
    True
    """
    return ' '.join(["-e \"%s=%s\"" % (key, value) for key, value in env.items()])
