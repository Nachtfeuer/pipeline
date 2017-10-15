# Welcome to the pipeline tool

[![Build Status](https://travis-ci.org/Nachtfeuer/pipeline.svg?branch=master)](https://travis-ci.org/Nachtfeuer/pipeline)

**Work in progress; not yet for use; stay tuned**

# Motivation

Most pipelines are working in context of the tool like Jenkins and Travis CI.
You cannot run a Jenkinsfile locally without mocking things since the used DSL
refer to installed Jenkins plugins. Similar is also valid for a  .travis.yml.

However it would be great when I could define a pipeline
that is capable of running locally. Of course I would like to have some well
known features of the existing pipelines and some that do not exist. Following
features will be considered for now:

 - matrix based pipeline (done)
 - pipeline stages (done)
 - shell scrip execution: inline and file (done)
 - environment variables merged across each level: matrix, pipeline, stage, and tasks (done)
 - parallel execution (todo)
 - execution time on each level: pipeline, stage, tasks and shell (todo)
 - automatic schema validation for yaml file (schema is there but validation is still manual)
 - cleanup hooks (todo)
 - filtered execution via tags (done)
 - one report (todo):
    - one html only
    - simple
    - nice
    - compact

It can be used by Jenkinsfile as well as by a `.travis.yml` (or other pipelines).

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