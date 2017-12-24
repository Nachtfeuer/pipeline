Quickstart
==========

Usage
-----
That installs the spline tool including all of its dependencies:

::

    pip install spline


When you have a pipeline definition (example: pipeline.yaml) then you can run it with:

::

    spline --definition=pipeline.yaml


Some simple examples you can see in the example folder of
the project repository and also spline itself provides
that file (exception: Docker tests are skipped).

The minimum structure of a pipeline definition file should look
like following:

::

    pipeline:
        - stage(Example):
            - tasks(ordered):
                - shell:
                    script: echo "hello world!"

The output:

::

    $ spline --definition=minimum.yaml
    2017-11-18 11:24:25,875 - spline.application - Running with Python 2.7.13 (default, Jan 19 2017, 14:48:08) [GCC 6.3.0 20170118]
    2017-11-18 11:24:25,883 - spline.application - Running on platform Linux-4.9.0-3-amd64-x86_64-with-debian-9.1
    2017-11-18 11:24:25,884 - spline.application - Processing pipeline definition 'minimum.yaml'
    2017-11-18 11:24:25,908 - spline.application - Schema validation for 'minimum.yaml' succeeded
    2017-11-18 11:24:25,934 - spline.components.stage - Processing pipeline stage 'Example'
    2017-11-18 11:24:25,934 - spline.components.tasks - Processing group of tasks
    2017-11-18 11:24:25,934 - spline.components.tasks - Processing Bash code: start
    2017-11-18 11:24:25,942 - spline.components.bash - Running script /tmp/pipeline-script-D3N3F9.sh
    2017-11-18 11:24:25,948 - spline.components.tasks -  | hello world!
    2017-11-18 11:24:25,949 - spline.components.tasks -  |
    2017-11-18 11:24:25,950 - spline.components.bash - Exit code has been 0
    2017-11-18 11:24:25,950 - spline.components.tasks - Processing Bash code: finished

Development
-----------

::

    git clone https://github.com/Nachtfeuer/pipeline.git
    cd pipeline
    ./unittests.sh
    # OR tox -e py35 OR tox -e py36 (see tox.ini)
    tox -e py27

For the purpose to test a specific Python version that does not
exist on your system you can choose one of following commands:

::

    spline --definition=pipeline.yaml --matrix-tags=py27
    spline --definition=pipeline.yaml --matrix-tags=py33
    spline --definition=pipeline.yaml --matrix-tags=py34
    spline --definition=pipeline.yaml --matrix-tags=py35
    spline --definition=pipeline.yaml --matrix-tags=py36
    spline --definition=pipeline.yaml --matrix-tags=pypy
    spline --definition=pipeline.yaml --matrix-tags=pypy3

If you leave away those tags it will run for all Python versions.
A special note on Python 3.6.x: I have provided two ways to deal
with it:

  - *init_py36_compile*: A concrete package is downloaded and built.
    You have to rename it to *init_py36* to use it (rename the other).
  - *init_py36*: It currently download ready made CentOS 7 packages;
    you save time with it.

The *init_py36* is the name that is constructed via the matrix so ensure
you have the one you prefer.
