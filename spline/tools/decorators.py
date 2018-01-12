"""
Decorator tools.

License::

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


def singleton(the_class):
    """
    Decorator for a class to make a singleton out of it.

    @type the_class: class
    @param the_class: the class that should work as a singleton
    @rtype: decorator
    @return: decorator
    """
    class_instances = {}

    def get_instance(*args, **kwargs):
        """
        Creating or just return the one and only class instance.

        The singleton depends on the parameters used in __init__
        @type args: list
        @param args: positional arguments of the constructor.
        @type kwargs: dict
        @param kwargs: named parameters of the constructor.
        @rtype: decorated class type
        @return: singleton instance of decorated class.
        """
        key = (the_class, args, str(kwargs))
        if key not in class_instances:
            class_instances[key] = the_class(*args, **kwargs)
        return class_instances[key]

    return get_instance
