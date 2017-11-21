# Welcome to the pipeline tool

[![Build Status](https://travis-ci.org/Nachtfeuer/pipeline.svg?branch=master)](https://travis-ci.org/Nachtfeuer/pipeline)
[![PyPI version](https://badge.fury.io/py/spline.png)](https://badge.fury.io/py/spline)
[![Read The Docs](https://readthedocs.org/projects/spline/badge/?version=latest)](http://spline.readthedocs.io/en/latest/?badge=latest)
[![Known Vulnerabilities](https://snyk.io/test/github/nachtfeuer/pipeline/badge.svg)](https://snyk.io/test/github/nachtfeuer/pipeline)
[![BCH compliance](https://bettercodehub.com/edge/badge/Nachtfeuer/pipeline?branch=master)](https://bettercodehub.com/)

**Table Of Content**:  
[Motivation](docs/motivation.rst)  
[Quickstart](docs/quickstart.rst)  
[Matrix](docs/matrix.rst)  
[The Model](docs/model.rst)  
[The Pipeline](docs/pipeline.rst)  
[Pipeline Stages](docs/stages.rst)  
[Tasks](docs/tasks.rst)  
[The Shell](docs/shell.rst)  
[Environment Variables](docs/env.rst)  
[Docker Container](docs/docker_container.rst)  
[Hooks](docs/hooks.rst)  
[Event Logging](docs/event_logging.rst)  
[Links](#links)  

**Features**:
 - Python support for 2.7.x, 3.3.x 3.4.x, 3.5.x and 3.6.x
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
 - execution time on each level: pipeline, stage, tasks and shell (event logging)
 - support for model data (a dictionary of anything you need)
 - documentation also at read the docs
 - usable by Jenkinsfile as well as by a `.travis.yml` (or other pipelines).

## <a name="links">Links</a>

 - http://pykwalify.readthedocs.io/en/unstable/
 - http://pykwalify.readthedocs.io/en/unstable/partial-schemas.html
 - https://github.com/bats-core/bats-core
