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
from spline.version import VERSION


setup(name='spline',
      version=VERSION,
      description='(s)hell oriented (p)ipe(line) tool (CI/CD)',
      long_description="(s)hell oriented (p)ipe(line) tool using yaml definition file (CI/CD)",
      author='Thomas Lehmann',
      author_email='thomas.lehmann.private@gmail.com',
      license="MIT",
      install_requires=["click", "pyaml", "jinja2", "pykwalify"],
      packages=['spline', 'spline.components', 'spline.tools'],
      scripts=['scripts/spline'],
      package_data={'spline': ['schema.yaml']},
      keywords="pipeline tool ci/cd bash docker",
      url="https://github.com/Nachtfeuer/pipeline",
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Unix",
          "Environment :: Console",
          "Topic :: Utilities"
      ])
