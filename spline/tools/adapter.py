"""
   Iterating Python data more easily.

.. module:: walk
    :platform: all
    :synopis: iterating Python data more easily.
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


class Adapter(object):
    """
    Adapting of Pythonic data.

    >>> data = Adapter({'person':{'name': 'Hercule', 'surname': 'Poirot'}})
    >>> data.person.name == 'Hercule'
    True
    >>> data.person.surname == 'Poirot'
    True
    """

    def __init__(self, data):
        """initializer walker with data."""
        self.data = data

    def __getattr__(self, key):
        """Organizing walking of dictionaries via direct field access."""
        if key in self.data:
            value = self.data[key]
            if isinstance(value, dict):
                return Adapter(value)
            return value
        else:
            value = getattr(self.data, key)
            if callable(value):
                return value
        return None

    def __str__(self):
        """string representation of the underlying object."""
        return str(self.data)

    def __len__(self):
        """len of the underlying object."""
        return len(self.data)
