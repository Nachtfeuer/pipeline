The Docker Container Script
===========================

Simple Example
--------------
The Docker container block **is basically the same** as the shell block with the exception
that a simple wrapper code is injected for Running the Docker container. Assume
following block as an example:

 - it runs a Docker container.
 - since no image is specified `centos:7` is used (as default)
 - after the injected Bash code has finished the Docker container will be automatically removed.

::

    - docker(container):
        script: |
            yum -y install epel-release > /dev/null 2>&1
            yum -y install figlet  > /dev/null 2>&1
            figlet -f standard "docker" | sed -e 's: :.:g'
        tags:
            - no-image

The code snippet you can find in the tests:

::

    $ PYTHONPATH=$PWD python scripts/pipeline --definition=tests/pipeline-015.yaml --tags=no-image
    2017-10-29 12:33:59,091 - pipeline.application - Running with Python 2.7.13 (default, Jan 19 2017, 14:48:08) [GCC 6.3.0 20170118]
    2017-10-29 12:33:59,104 - pipeline.application - Running on platform Linux-4.9.0-3-amd64-x86_64-with-debian-9.1
    2017-10-29 12:33:59,104 - pipeline.application - Processing pipeline definition 'tests/pipeline-015.yaml'
    2017-10-29 12:33:59,135 - pipeline.application - Schema validation for 'tests/pipeline-015.yaml' succeeded
    2017-10-29 12:33:59,137 - pipeline.components.stage - Processing pipeline stage 'test'
    2017-10-29 12:33:59,137 - pipeline.components.tasks - Processing group of tasks
    2017-10-29 12:33:59,138 - pipeline.components.tasks - Processing Bash code: start
    2017-10-29 12:33:59,146 - pipeline.components.bash - Running script /tmp/pipeline-script-z3eXdd.sh
    2017-10-29 12:34:16,404 - pipeline.components.tasks -  | ....._............_.............
    2017-10-29 12:34:16,404 - pipeline.components.tasks -  | ..__|.|.___...___|.|._____._.__.
    2017-10-29 12:34:16,405 - pipeline.components.tasks -  | ./._`.|/._.\./.__|.|/./._.\.'__|
    2017-10-29 12:34:16,405 - pipeline.components.tasks -  | |.(_|.|.(_).|.(__|...<..__/.|...
    2017-10-29 12:34:16,405 - pipeline.components.tasks -  | .\__,_|\___/.\___|_|\_\___|_|...
    2017-10-29 12:34:16,405 - pipeline.components.tasks -  | ................................
    2017-10-29 12:34:16,405 - pipeline.components.tasks -  |
    2017-10-29 12:34:16,405 - pipeline.components.bash - Exit code has been 0

Specifying an image
-------------------
You also can specify an image:

::

    - docker(container):
        image: centos:7.3.1611
        script: cat /etc/redhat-release
        tags:
            - with-image

Here's an extract of the output:

::

    2017-10-29 12:46:06,080 - pipeline.components.bash - Running script /tmp/pipeline-script-36Ga0I.sh
    2017-10-29 12:46:07,583 - pipeline.components.tasks -  | CentOS Linux release 7.3.1611 (Core)
    2017-10-29 12:46:07,583 - pipeline.components.tasks -  |

How to find a Docker container
------------------------------
 - Each Docker container gets additional labels:
   - **pipeline** - which contains the PID of the pipeline.
   - **pipeline-stage** - pipeline stage in which the Docker container has been created.
   - **context** - always "pipeline"
   - **creator** - the PID of the shell which created the Docker container.
 - with those information you have some control for being able to query a concrete container without knowing the Docker container name (you need not worry about container names since Docker does it for you).
 - If you create multiple Docker container per stage then (TODO) there will be a label that can be
   adjusted via the yaml to reduce the query to the right container.
 - Have a look at the examples [docker.yaml](examples/docker.yaml).

Mounts
------
For good reasons various number of mounts have been minimized to the most essential ones:
 - one mount (always) for the script mechanism (you shouldn't care)
 - one mount (on demand) if you need to exchange things with the host

The next example does activate the second mount which maps $PWD as `/mnt/host` inside
the Docker container. Here I write a file to the host and another script dumps it
and removes the file afterwards.

::

    - docker(container):
        script: |
            echo "hello world" > /mnt/host/hello.txt
            chown ${UID}:$(GID} /mnt/host/hello.txt
        mount: true

    - shell:
        script: |
            cat hello.txt
            rm -f hello.txt


**Please note:** Usually the Docker user is root (by default) and when you copy
content to the host the caller might fail on removing that files and folders because
of missing permissions. That's why the user id and group id is always passed to the
container allowing you to adjust the permissions correctly.


"With" attribute
----------------
It's exactly the same as for `shell <shell.rst>`_ - please read the details there.


Conditional tasks
-----------------
The field **when** allows you to define a condition; when evaluated as true then
the task is executed otherwise not. More details you can read in the separate
section `Conditional Tasks`.
