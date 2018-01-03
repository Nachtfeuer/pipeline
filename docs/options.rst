Command Line Options
====================

Dry run mode
------------
Using the option **--dry-run** you get a tool that help
you to analyse your pipeline with following rules when
the option is set:

 - parallelism (matrix and tasks) is disabled
 - custom logging is disabled
 - the default logging is adjusted to have no timestamps
 - using **docker(image)** tasks the Dockerfile is printed as
   Bash comment; the Dockerfile is not written as a file.
 - The cleanup hooks are also not executed but logged.

As an example a **docker(image)** task might look similar to
following output:

::

    $ spline --definition=examples/docker-image.yaml --dry-run
    spline.application - Running with Python 2.7.13 (default, Jan 19 2017, 14:48:08) [GCC 6.3.0 20170118]
    spline.application - Running on platform Linux-4.9.0-3-amd64-x86_64-with-debian-9.1
    spline.application - Processing pipeline definition 'examples/docker-image.yaml'
    spline.application - Schema validation for 'examples/docker-image.yaml' succeeded
    spline.components.stage - Processing pipeline stage 'Example'
    spline.components.tasks - Processing group of tasks (parallel=disabled)
    spline.components.tasks - Processing Bash code: start
    spline.components.bash - Dry run mode for script /tmp/pipeline-script-TRd8fF.sh
    spline.components.tasks -  | #!/bin/bash
    spline.components.tasks -  | # Dockerfile:
    spline.components.tasks -  | # >>
    spline.components.tasks -  | # FROM centos:7
    spline.components.tasks -  | # RUN yum -y install yum-utils git
    spline.components.tasks -  | # RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
    spline.components.tasks -  | # RUN yum -y install python36u python36u-pip
    spline.components.tasks -  | # RUN pip3.6 install tox
    spline.components.tasks -  | #
    spline.components.tasks -  | # <<
    spline.components.tasks -  | # for visibility in logging
    spline.components.tasks -  | echo "docker build -t python:3.6 < dockerfile.dry.run.see.comment"
    spline.components.tasks -  | # trying to build docker image
    spline.components.tasks -  | docker build -t python:3.6 - < dockerfile.dry.run.see.comment
    spline.components.tasks -  | docker_error=$?
    spline.components.tasks -  | # cleanup
    spline.components.tasks -  | rm -f
    spline.components.tasks -  | # give back result
    spline.components.tasks -  | exit ${docker_error}
    spline.components.tasks - Processing Bash code: finished
