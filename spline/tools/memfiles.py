"""Module memfiles."""
# Copyright (c) 2018 Thomas Lehmann
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
import os
import json
from base64 import b64encode, b64decode
from zlib import compress, decompress


class InMemoryFiles(object):
    """
    In Memory file storage.

    The compression functionality allows
    to transfer the files via client/server communication.

    >>> memfiles1 = InMemoryFiles()
    >>> memfiles1.add_path(os.path.dirname(__file__), lambda fp: fp.endswith(".py"))
    >>> data = memfiles1.to_compressed()
    >>> memfiles2 = InMemoryFiles.from_compressed(data)
    >>> assert memfiles1.files == memfiles2.files
    """

    def __init__(self):
        """Initialize empty dictionary of files (the path and filename is the key)."""
        self.files = {}

    def add_path(self, path, path_filter=None):
        """
        Adding all files from given path to the object.

        Args:
            path (str): valid, existing directory
        """
        for root, _, files in os.walk(path):
            for filename in files:
                full_path_and_filename = os.path.join(root, filename)
                if path_filter is None or path_filter(full_path_and_filename):
                    relative_path_and_filename = full_path_and_filename.replace(path + '/', '')
                    with open(full_path_and_filename, 'rb') as handle:
                        self.files[relative_path_and_filename] = b64encode(handle.read()).decode('utf-8')

    def save(self, path):
        """
        Saving stored files at a given path (relative paths are added).

        Args:
            path (str): root path where to save the files.
        """
        for relative_path_and_filename, content in self.files.items():
            full_path_and_filename = os.path.join(path, relative_path_and_filename)
            full_path = os.path.dirname(full_path_and_filename)

            if not os.path.isdir(full_path):
                os.makedirs(full_path)

            with open(full_path_and_filename, 'wb') as handle:
                handle.write(b64decode(content))

    def to_json(self):
        """
        Convert file storage into JSON data.

        Returns:
            str: file storaged converted into JSON data
        """
        return json.dumps(self.files)

    @staticmethod
    def from_json(data):
        """
        Convert JSON into a in memory file storage.

        Args:
            data (str): valid JSON with path and filenames and
                        the base64 encoding of the file content.

        Returns:
            InMemoryFiles: in memory file storage
        """
        memfiles = InMemoryFiles()
        memfiles.files = json.loads(data)
        return memfiles

    def to_compressed(self, compression_level=6):
        """
        Return file storage data compressed.

        Args:
            compression_level (int): default compression level = 6

        Returns:
            str: compressed file storage.
        """
        return compress(self.to_json().encode('utf-8'), compression_level)

    @staticmethod
    def from_compressed(data):
        """
        Convert compressed data into a new in memory file storage instance.

        Args:
            data (str): compressed data (from a previous call of `to_compressed`)

        Returns:
            InMemoryFiles: in memory file storage with data
        """
        return InMemoryFiles.from_json(decompress(data).decode('utf-8'))
