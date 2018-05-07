Spline
======

.. image:: https://img.shields.io/pypi/v/spline.svg
    :target: https://pypi.python.org/pypi/spline/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/spline.svg
    :target: https://pypi.python.org/pypi/spline/
    :alt: Python Versions

.. image:: https://img.shields.io/pypi/format/spline.svg
    :target: https://pypi.python.org/pypi/spline/
    :alt: Format

.. image:: https://img.shields.io/pypi/l/spline.svg
    :target: https://pypi.python.org/pypi/spline/
    :alt: License

.. image:: https://img.shields.io/pypi/l/spline.svg
    :target: https://pypi.python.org/pypi/spline/
    :alt: License

.. image:: https://img.shields.io/coveralls/github/Nachtfeuer/pipeline.svg
    :target: https://coveralls.io/github/Nachtfeuer/pipeline?branch=master

Motivation
----------
Implementing coded pipelines with Jenkins you have to deal with
Groovy, Jenkinsfile and a so called DSL which allows you interfacing
with Jenkins and its plugins. However the whole setup is usually designed
to run somewhere remote fetching a revision of your code and running
the pipeline on it. Creating or extending such a pipeline locally running
on your current code is - finally - not comfortable: that setup forces
you a lot to split into Groovy and Bash scripts that allow you to run
things locally which increases complexity even more.

Also you are not flexible in terms of environments. You cannot
run same pipeline in Travis CI (and such tools). 

**Spline is a way to get out of this**: You can run the whole pipeline
via command line on your machine. Also you can run matrix builds and
you can filter for certain tasks of your interest. The pipeline for the
spline tool itself supporting a lot Python version can be defined
in one file with roughly 170 lines of yaml code only. Integration into
Jenkinsfile and/or Travis CI isn't that hard anymore.


Quickstart
----------
Installation can be simply done with (optional with --upgrade for updating the installed version):

::

    pip install spline

You require a pipeline definition file (Yaml). As an
example feel free to do following:

::

    sudo pip install spline
    git clone https://github.com/Nachtfeuer/pipeline.git
    cd pipeline
    pipeline --definition=pipeline.yaml --matrix-tags=py36

When the file in your project is `pipeline.yaml`you als can leave out
the `--definition` parameter.

If you leave out the matrix tag filter then spline will run
all python version as defined in the matrix (see badges too).

Features
--------
 - automatic schema validation for yaml file
 - matrix based pipeline
 - pipeline stages (named groups)
 - shell script execution: inline and file
 - environment variables merged across each level: matrix, pipeline, stage, and tasks
 - support for model data (a dictionary of anything you need)
 - cleanup hook
 - filtered execution via tags (matrix and/or tasks)
 - supporting Jinja templating in scripts (also nested inside model)
 - support for Docker containers and Docker images
 - support for the Packer tool
 - execution time on each level: pipeline, stage, tasks and shell (event logging)
 - usable by Jenkinsfile as well as by a `.travis.yml` (or other pipelines).
 - dry run and debug support
 - support for Python scripts
 - support for task variables
 - support for conditional tasks
 - enabled for code reuse: !include statement

Documentation
-------------
For further details about what you can do please read the
documentation. You have two options:

 - follow the links on the Github main page: https://github.com/Nachtfeuer/pipeline
 - follow the link to read the docs: http://spline.readthedocs.io/en/master/
 - presentation: https://gitpitch.com/Nachtfeuer/pipeline/master

About Names
------------
 - **spline**: (**s**)hell oriented (**p**)ipe(**line**)
 - **Nachtfeuer**: A demon (finally) fighting for the good side in a great fantasy (https://www.amazon.de/dp/B00946NO6I).
