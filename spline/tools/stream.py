"""
Stream utilitites.

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
import sys
import tempfile
from contextlib import contextmanager

if sys.version_info.major == 3:
    from io import StringIO as Stream
else:
    from io import BytesIO as Stream


@contextmanager
def stdout_redirector():
    """
    Simplify redirect of stdout.

    Taken from here: https://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
    """
    old_stdout = sys.stdout
    sys.stdout = Stream()
    try:
        yield sys.stdout
    finally:
        sys.stdout.close()
        sys.stdout = old_stdout


def write_temporary_file(content, prefix='', suffix=''):
    """
    Generating a temporary file with content.

    Args:
        content (str): file content (usually a script, Dockerfile, playbook or config file)
        prefix (str): the filename starts with this prefix (default: no prefix)
        suffix (str): the filename ends with this suffix (default: no suffix)

    Returns:
        str: name of the temporary file

    Note:
        You are responsible for the deletion of the file.
    """
    temp = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, mode='w+t', delete=False)
    temp.writelines(content)
    temp.close()
    return temp.name
