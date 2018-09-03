"""
Provide simple query tool.

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


class Select(object):
    """Select a sequence and do operation like filtering on it."""

    def __init__(self, *args):
        """
        Initialize with data that can be queried.

        >>> Select(1, 2, 3, 4).where(lambda n: n % 2 == 0).build()
        [2, 4]
        >>> Select(1, 2, 3, 4).transform(lambda n: n * 2).build()
        [2, 4, 6, 8]
        """
        self.sequence = Select.flatten(*args)
        self.filter_functions = []
        self.transform_functions = []

    @staticmethod
    def flatten(*sequence):
        """Flatten nested sequences into one."""
        result = []
        for entry in sequence:
            if isinstance(entry, list):
                result += Select.flatten(*entry)
            elif isinstance(entry, tuple):
                result += Select.flatten(*entry)
            else:
                result.append(entry)
        return result

    def where(self, filter_function):
        """Register a filter function."""
        self.filter_functions.append(filter_function)
        return self

    def transform(self, transform_function):
        """Register transfrom function."""
        self.transform_functions.append(transform_function)
        return self

    def build(self):
        """Do the query."""
        result = []
        for entry in self.sequence:
            ignore = False
            for filter_function in self.filter_functions:
                if not filter_function(entry):
                    ignore = True
                    break
            if not ignore:
                value = entry
                for transform_function in self.transform_functions:
                    value = transform_function(value)
                result.append(value)
        return result
