# Welcome to the pipeline tool

[![Build Status](https://travis-ci.org/Nachtfeuer/pipeline.svg?branch=master)](https://travis-ci.org/Nachtfeuer/pipeline)

**Work in progress; not yet for use; stay tuned**

# Motivation

Most pipelines are working in context of the tool like Jenkins and Travis CI.
You cannot run a Jenkinsfile locally without mocking things since the used DSL
refer to installed Jenkins plugins. Similar is also valid for a  .travis.yml.

However it would be great when I could define a pipeline
that is capable of running locally. Of course it would be great to have some well
known features of the existing pipelines and some that do not exist. Following
features will be considered for now:

**Features**:
 - automatic schema validation for yaml file
 - matrix based pipeline
 - pipeline stages (names groups)
 - shell script execution: inline and file
 - environment variables merged across each level: matrix, pipeline, stage, and tasks
 - cleanup hook
 - filtered execution via tags

**Todo**:
 - parallel tasks execution
 - parallel pipelines (matrix)
 - execution time on each level: pipeline, stage, tasks and shell
 - one report:
    - one HTML file only
    - simple
    - nice
    - compact

It should be usable by Jenkinsfile as well as by a `.travis.yml` (or other pipelines).

# Quick start

Following dependencies are required:

```
pip install click pyaml pykwalify
```

Main focus for a quick start is developing on this
project. For **using** this pipeline tool there will
be another section.

```
git clone https://github.com/Nachtfeuer/pipeline.git
cd pipeline
./validate.sh
./unittests.sh
```

# The pipeline syntax

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

### The pipeline block

The pipeline is a list of stages. It also may have environment blocks.

### The stage block

Each stage is a list of tasks blocks. It also may have environment blocks.

### The tasks block

Each tasks block is a list of shell scripts. It also may have environment blocks.

### The shell (the task)

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

### The environment block

On all levels (pipeline, stages and tasks) you can have such environment blocks.
When a shell script is executed the environment is copied and overwritten in
mentioned order. As a base are all OS environment variables provided as they
exist when the pipeline has been started.

```
env:
  foo: hello
  bar: world
```

### The cleanup hook

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


# Some hints

The following code should print the loaded yaml just
basing on pure Python data (dict, list, str and so on).

```
python -c "import yaml;print(yaml.load(open('example.yaml').read()))"
```

# Links
 - http://pykwalify.readthedocs.io/en/unstable/
 - http://pykwalify.readthedocs.io/en/unstable/partial-schemas.html
 - https://github.com/bats-core/bats-core