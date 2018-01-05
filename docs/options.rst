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

Debug
-----
The option `--debug` adjust the Bash option `set -x` which activates the debug
mode in Bash. The primes example in the spline repository gives you a good example.
I'm just printing the first 20 lines:

::

    $ spline --definition=examples/primes.yaml --debug 2>&1 | head -20
    2018-01-05 19:31:12,023 - spline.application - Running with Python 2.7.13 (default, Jan 19 2017, 14:48:08) [GCC 6.3.0 20170118]
    2018-01-05 19:31:12,028 - spline.application - Running on platform Linux-4.9.0-3-amd64-x86_64-with-debian-9.1
    2018-01-05 19:31:12,028 - spline.application - Current cpu count is 4
    2018-01-05 19:31:12,029 - spline.application - Processing pipeline definition 'examples/primes.yaml'
    2018-01-05 19:31:12,032 - spline.application - Schema validation for 'examples/primes.yaml' succeeded
    2018-01-05 19:31:12,032 - spline.components.stage - Processing pipeline stage 'Calculate Primes'
    2018-01-05 19:31:12,033 - spline.components.tasks - Processing group of tasks (parallel=no)
    2018-01-05 19:31:12,033 - spline.components.tasks - Processing Bash code: start
    2018-01-05 19:31:12,043 - spline.components.bash - Running script /tmp/pipeline-script-5iRCsz.sh
    2018-01-05 19:31:12,050 - spline.components.tasks -  | ++ seq 0 100
    2018-01-05 19:31:12,051 - spline.components.tasks -  | + for n in $(seq 0 100)
    2018-01-05 19:31:12,052 - spline.components.tasks -  | ++ is_prime 0
    2018-01-05 19:31:12,052 - spline.components.tasks -  | ++ n=0
    2018-01-05 19:31:12,052 - spline.components.tasks -  | ++ '[' 0 -lt 2 ']'
    2018-01-05 19:31:12,052 - spline.components.tasks -  | ++ return
    2018-01-05 19:31:12,053 - spline.components.tasks -  | + '[' '' == yes ']'
    2018-01-05 19:31:12,053 - spline.components.tasks -  | + for n in $(seq 0 100)
    2018-01-05 19:31:12,053 - spline.components.tasks -  | ++ is_prime 1
    2018-01-05 19:31:12,053 - spline.components.tasks -  | ++ n=1
    2018-01-05 19:31:12,053 - spline.components.tasks -  | ++ '[' 1 -lt 2 ']'

