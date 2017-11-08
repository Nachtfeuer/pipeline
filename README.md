# Welcome to the pipeline tool

[![Build Status](https://travis-ci.org/Nachtfeuer/pipeline.svg?branch=master)](https://travis-ci.org/Nachtfeuer/pipeline)
[![PyPI version](https://badge.fury.io/py/spline.png)](https://badge.fury.io/py/spline)

**Table Of Content**:  
[Motivation](#motivation)  
[Quickstart](#quick-start)  
[The Pipeline Syntax](#pipeline-syntax)  
[The Matrix Block](#matrix-block)  
[The Pipeline Block](#pipeline-block)  
[The Stage Block](#stage-block)  
[The Tasks Block](#tasks-block)  
[The Shell (Task) Block](#shell-block)  
[The Environment Block](#environment-block)  
[The Docker Container Block](#docker-container-block)  
[The Cleanup Hook](#cleanup-hook)  
[Performance Logging](#event-logging)  
[Links](#links)  

# <a name="motivation">Motivation</a>

Most pipelines are working in context of the tool like Jenkins and Travis CI.
You cannot run a Jenkinsfile locally without mocking things since the used DSL
refer to installed Jenkins plugins. Similar is also valid for a  .travis.yml.

However it would be great when I could define a pipeline
that is capable of running locally. Of course it would be great to have some well
known features of the existing pipelines and some that do not exist. Following
features will be considered for now:

**Features**:
 - Python support for 2.7.x, 3.4.x, 3.5.x and 3.6.x
 - automatic schema validation for yaml file
 - matrix based pipeline with tags
 - parallel pipelines (matrix)
 - pipeline stages (names groups)
 - shell script execution: inline and file
 - environment variables merged across each level: matrix, pipeline, stage, and tasks
 - cleanup hook
 - filtered execution via tags
 - parallel tasks execution
 - supporting Jinja templating in Bash scripts
 - support for Docker containers
 - execution time on each level: pipeline, stage, tasks and shell

**Todo**:
 - support for templates / code snippets
 - one report:
    - one HTML file only
    - simple
    - nice
    - compact

It should be usable by Jenkinsfile as well as by a `.travis.yml` (or other pipelines).

# <a name="quick-start">Quick start</a>

```
# (s)hell oriented (p)ipe(line) tool.
pip install spline
```

Following dependencies are required only if you do not install the tool
but clone the repository:

```
pip install click pyaml pykwalify
```

Main focus for a quick start is developing on this
project. For **using** this pipeline tool there will
be another section.

```
git clone https://github.com/Nachtfeuer/pipeline.git
cd pipeline
./unittests.sh
tox -e pylint -e radon -e pep8 -e pep257 -e package
```

# <a name="pipeline-syntax">The Pipeline Syntax</a>

It's organized through a yaml file. Looking at the unittests of this
project the file `unittests.sh`could be implemented as a `unittests.yaml`
like following:

```
pipeline:
  - env:
      bats_url: https://github.com/bats-core/bats-core.git

  - stage(unittests):
    - tasks:
      - shell:
          script: |
            if [ ! -d bats-core ]; then
              echo "Downloading bats tool from ${bats_url}"
              git clone ${bats_url}
            fi

      - shell:
          script: |
            WORKSPACE=$PWD bats-core/bin/bats tests
```


```
./pipeline --definition=unittests.yaml
2017-10-16 05:35:56,977 Running with Python 2.7.13 (default, Jan 19 2017, 14:48:08) [GCC 6.3.0 20170118]
2017-10-16 05:35:56,983 Running on platform Linux-4.9.0-3-amd64-x86_64-with-debian-9.1
2017-10-16 05:35:56,987 Processing pipeline definition 'unittests.yaml'
2017-10-16 05:35:56,989 Updating environment at level 0 with {'bats_url': 'https://github.com/bats-core/bats-core.git'}
2017-10-16 05:35:56,990 Processing pipeline stage 'unittests'
2017-10-16 05:35:56,990 Processing group of tasks
2017-10-16 05:35:56,990 Processing Bash code: start
2017-10-16 05:35:56,992 Running script /tmp/pipeline-script-VmGqRs.sh
2017-10-16 05:35:58,325  | Downloading bats tool from https://github.com/bats-core/bats-core.git
2017-10-16 05:35:58,325  | Cloning into 'bats-core'...
2017-10-16 05:35:58,325  |
2017-10-16 05:35:58,325 Exit code has been 0
2017-10-16 05:35:58,326 Processing Bash code: finished
2017-10-16 05:35:58,326 Processing Bash code: start
2017-10-16 05:35:58,326 Running script /tmp/pipeline-script-N9jVvh.sh
2017-10-16 05:35:59,648  | 1..10
2017-10-16 05:35:59,649  | ok 1 /work/pipeline/tests/pipeline-001.bats :: Testing valid inline bash code
2017-10-16 05:35:59,649  | ok 2 /work/pipeline/tests/pipeline-002.bats :: Testing failing inline bash code
2017-10-16 05:35:59,649  | ok 3 /work/pipeline/tests/pipeline-003.bats :: Testing use of environment variables (pipeline level)
2017-10-16 05:35:59,649  | ok 4 /work/pipeline/tests/pipeline-004.bats :: Testing use of environment variables (stage level, merging)
2017-10-16 05:35:59,649  | ok 5 /work/pipeline/tests/pipeline-005.bats :: Testing use of environment variables (tasks level, merging)
2017-10-16 05:35:59,649  | ok 6 /work/pipeline/tests/pipeline-006.bats :: Testing valid bash file
2017-10-16 05:35:59,649  | ok 7 /work/pipeline/tests/pipeline-007.bats :: Testing valid matrix with two entries
2017-10-16 05:35:59,649  | ok 8 /work/pipeline/tests/pipeline-008.bats :: Testing filtering by first tag
2017-10-16 05:35:59,649  | ok 9 /work/pipeline/tests/pipeline-008.bats :: Testing filtering by second tag
2017-10-16 05:35:59,649  | ok 10 /work/pipeline/tests/pipeline-008.bats :: Testing filtering by both tags
2017-10-16 05:35:59,649  |
2017-10-16 05:35:59,649 Exit code has been 0
2017-10-16 05:35:59,649 Processing Bash code: finished
```

If you are wondering why I'm not using that in given `.travis.yml` then
the answer is simple: while build the pipeline tool is not yet verified
and might have problems producing wrong build results; that's why an
external test mechanism is better for this project.

## <a name="matrix-block">The Matrix Block</a>

A matrix basically has a name and assigned environment variables. The purpose is
to support that same pipeline can run for different parameters. Examples are
running with different compilers, interpreters or databases. In addition you can
specify tags which allow to filter for certain matrix runs.

```
matrix:
  - name: one
    env:
        mode: one
    tags:
        - first

  - name: two
    env:
        mode: two
    tags:
        - second
```

With this example you can filter for second matrix item like this:
```
pipeline --definition=example.yaml --matrix-tags=second
```


## <a name="pipeline-block">The Pipeline Block</a>

The pipeline is a list of stages. It also may have environment blocks.

```
pipeline:
  - env:
      mode: test

  - stage(one):
    - tasks(ordered):
      - shell:
        - script: echo "{{ env.mode }}: script one"

  - stage(two):
    - tasks(ordered):
      - shell:
        - script: echo "{{ env.mode }}: script two"
```

## <a name="stage-block">The Stage Block</a>

Each stage is a list of tasks blocks. It also may have environment blocks.

```
- stage(one):
  - env:
      mode: test

  - tasks(ordered):
    - shell:
      - script: echo "{{ env.mode }}: script one"

  - tasks(ordered):
    - shell:
      - script: echo "{{ env.mode }}: script two"
```


## <a name="tasks-block">The Tasks Block</a>

Each tasks block is a list of shell scripts. It also may have environment blocks.

```
- tasks(ordered):
  - env:
      mode: test

  - shell:
    - script: echo "{{ env.mode }}: script one"

  - shell:
    - script: echo "{{ env.mode }}: script two"
```

## <a name="shell-block">The Shell (Task) Block</a>

Each shell can have inline Bash code or refer to an external file.
A shell can break the pipeline when the exit code it not zero.
Also a shell may have a list of tags which allow to filter for those of interests.
The bash code also can have multiple lines as shown after here. Independent whether
the code is inline or via external final it will be copied into a temporary
file and those one will be executed only.

```
shell:
  script: |
    echo "hello world"
    exit 0
  tags:
    - test
    - simple
```
It's also possible to use Jinja templating but it does work only for the
yaml script text (not for external bash files). Currently it is restricted
for using environment variables.

```
- tasks:
  - env:
      count: "3"
  - shell:
      script: |
          {% for c in range(env.count|int) %}
          echo "{{ c+1 }}:{{ env.message }}"
          {% endfor %}
```

## <a name="environment-block">The Environment Block</a>

On all levels (pipeline, stages and tasks) you can have such environment blocks.
When a shell script is executed the environment is copied and overwritten in
mentioned order. As a base are all OS environment variables provided as they
exist when the pipeline has been started.

```
env:
  foo: hello
  bar: world
```

## <a name="docker-container-block">The Docker Container Block</a>

The Docker container block is basically the same as the shell block with the exception
that a simple wrapper code is injected for Running the Docker container. Assume
following block as an example:

 - it runs a Docker container.
 - since no image is specified `centos:7` is used (as default)
 - after the injected Bash code has finished the Docker container will be automatically removed.

```
- docker(container):
    script: |
      yum -y install epel-release > /dev/null 2>&1
      yum -y install figlet  > /dev/null 2>&1
      figlet -f standard "docker" | sed -e 's: :.:g'
    tags:
      - no-image
```

The code snippet you can find in the tests:

```
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
2017-10-29 12:34:16,405 - pipeline.components.tasks - Processing Bash code: finished
```

### Specifying an image
You also can specify an image:

```
- docker(container):
    image: centos:7.3.1611
    script: cat /etc/redhat-release
    tags:
      - with-image
```

Here's an extract of the output:

```
2017-10-29 12:46:06,080 - pipeline.components.bash - Running script /tmp/pipeline-script-36Ga0I.sh
2017-10-29 12:46:07,583 - pipeline.components.tasks -  | CentOS Linux release 7.3.1611 (Core)
2017-10-29 12:46:07,583 - pipeline.components.tasks -  |
```

### How to find a Docker container
 - Each Docker container gets additional labels:
   - **pipeline** - which contains the PID of the pipeline.
   - **pipeline-stage** - pipeline stage in which the Docker container has been created.
   - **context** - always "pipeline"
   - **creator** - the PID of the shell which created the Docker container.
 - with those information you have some control for being able to query a concrete container without knowing the Docker container name (you need not worry about container names since Docker does it for you).
 - If you create multiple Docker container per stage then (TODO) there will be a label that can be
   adjusted via the yaml to reduce the query to the right container.
 - Have a look at the examples [docker.yaml](examples/docker.yaml).

### Mounts
For good reasons various number of mounts have been minimized to the most essential ones:
 - one mount (always) for the script mechanism (you shouldn't care)
 - one mount (on demand) if you need to exchange things with the host

The next example does activate the second mount which maps $PWD as `/mnt/host` inside
the Docker container. Here I write a file to the host and another script dumps it
and removes the file afterwards.

```
- docker(container):
    script: |
      echo "hello world" > /mnt/host/hello.txt
      chown ${UID}:$(GID} /mnt/host/hello.txt
    mount: true

- shell:
    script: |
      cat hello.txt
      rm -f hello.txt
```

**Please note:** Usually the Docker user is root (by default) and when you copy
content to the host the caller might fail on removing that files and folders because
of missing permissions. That's why the user id and group id is always passed to the
container allowing you to adjust the permissions correctly.


## <a name="cleanup-hook">The cleanup hook</a>

It's basically same as for a shell script with a few differences only:

 - When the pipeline succeeds all variables from pipeline level are available.
 - When a shell script fails all variables on that level are available
 - Additionally the variable **PIPELINE_RESULT** can have the value **SUCCESS** or **FAILURE**.
 - Additionally the variable **PIPELINE_SHELL_EXIT_CODE** has the shell exit code
   of the failed shell or 0 (default)

```
hooks:
  cleanup:
    script: |
      echo "cleanup has been called!"
      echo "${message}"
      echo "PIPELINE_RESULT=${PIPELINE_RESULT}"
      echo "PIPELINE_SHELL_EXIT_CODE=${PIPELINE_SHELL_EXIT_CODE}"
```
## <a name="event-logging">Performance logging</a>
With the command line option `--event-logging` you enable additional logging that
measures execution time on the whole application, each pipeline, stage, tasks and docker/shell level.

```
$ PYTHONPATH=$PWD python scripts/pipeline --definition=examples/docker.yaml  --tags=using-mount --event-logging
2017-11-03 05:10:52,742 - pipeline.application - Running with Python 2.7.13 (default, Jan 19 2017, 14:48:08) [GCC 6.3.0 20170118]
2017-11-03 05:10:52,757 - pipeline.application - Running on platform Linux-4.9.0-3-amd64-x86_64-with-debian-9.1
2017-11-03 05:10:52,757 - pipeline.application - Processing pipeline definition 'examples/docker.yaml'
2017-11-03 05:10:52,824 - pipeline.application - Schema validation for 'examples/docker.yaml' succeeded
2017-11-03 05:10:52,841 - pipeline.components.stage - Processing pipeline stage 'example'
2017-11-03 05:10:52,842 - pipeline.components.tasks - Processing group of tasks
2017-11-03 05:10:52,842 - pipeline.components.tasks - Processing Bash code: start
2017-11-03 05:10:52,876 - pipeline.components.bash - Running script /tmp/pipeline-script-Ws20v5.sh
2017-11-03 05:10:54,173 - pipeline.components.tasks -  |
2017-11-03 05:10:54,173 - pipeline.components.bash - Exit code has been 0
2017-11-03 05:10:54,174 - pipeline.components.bash.event - Succeeded - took 1.331764 seconds.
2017-11-03 05:10:54,174 - pipeline.components.tasks - Processing Bash code: finished
2017-11-03 05:10:54,174 - pipeline.components.tasks - Processing Bash code: start
2017-11-03 05:10:54,176 - pipeline.components.bash - Running script /tmp/pipeline-script-sydNg5.sh
2017-11-03 05:10:54,191 - pipeline.components.tasks -  | hello world
2017-11-03 05:10:54,191 - pipeline.components.tasks -  |
2017-11-03 05:10:54,191 - pipeline.components.bash - Exit code has been 0
2017-11-03 05:10:54,191 - pipeline.components.bash.event - Succeeded - took 0.017044 seconds.
2017-11-03 05:10:54,192 - pipeline.components.tasks - Processing Bash code: finished
2017-11-03 05:10:54,192 - pipeline.components.tasks.event - Succeeded - took 1.349966 seconds.
2017-11-03 05:10:54,192 - pipeline.components.stage.event - Succeeded - took 1.350690 seconds.
2017-11-03 05:10:54,192 - pipeline.pipeline.event - Succeeded - took 1.351264 seconds.
2017-11-03 05:10:54,192 - pipeline.application.event - Succeeded - took 1.450534 seconds.
```

## <a name="links">Links</a>

 - http://pykwalify.readthedocs.io/en/unstable/
 - http://pykwalify.readthedocs.io/en/unstable/partial-schemas.html
 - https://github.com/bats-core/bats-core