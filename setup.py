"""
Package setup.

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
import os
from setuptools import setup
from pipeline import VERSION


def read(fname):
    """ reading a file from current path of this file. """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pipeline',
      version=VERSION,
      description='pipeine tool',
      long_description="pipeline tool",
      author='Thomas Lehmann',
      author_email='thomas.lehmann.private@gmail.com',
      license="MIT",
      install_requires=["click", "pyaml"],
      packages=['pipeline', 'pipeline.components'],
      data_files=[('concept', ['scripts/pipeline'])],
      keywords="pipeline tool ci/cd",
      url="https://github.com/Nachtfeuer/pipeline",
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Unix"
      ])
