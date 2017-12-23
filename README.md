# Welcome to spline - the pipeline tool

[![Build Status](https://travis-ci.org/Nachtfeuer/pipeline.svg?branch=master)](https://travis-ci.org/Nachtfeuer/pipeline)
[![PyPI version](https://img.shields.io/pypi/v/spline.svg)](https://pypi.python.org/pypi/spline)
[![PyPI format](https://img.shields.io/pypi/format/spline.svg)](https://pypi.python.org/pypi/spline)
[![PyPI versions](https://img.shields.io/pypi/pyversions/spline.svg)](https://pypi.python.org/pypi/spline)
[![PyPI license](https://img.shields.io/pypi/l/spline.svg)](https://pypi.python.org/pypi/spline)
[![Read The Docs](https://readthedocs.org/projects/spline/badge/?version=latest)](http://spline.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/Nachtfeuer/pipeline/badge.svg?branch=master&service=github)](https://coveralls.io/github/Nachtfeuer/pipeline?branch=master)
[![BCH compliance](https://bettercodehub.com/edge/badge/Nachtfeuer/pipeline?branch=master)](https://bettercodehub.com/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/96262e26f41546b684e88f40a9c0176d)](https://www.codacy.com/app/thomas.lehmann.private/pipeline?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Nachtfeuer/pipeline&amp;utm_campaign=Badge_Grade)
[![Known Vulnerabilities](https://snyk.io/test/github/nachtfeuer/pipeline/badge.svg)](https://snyk.io/test/github/nachtfeuer/pipeline)


**Table Of Content**:  
[Motivation](docs/motivation.rst)  
[Quickstart](docs/quickstart.rst)  
[Example](docs/example.rst)  
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
 - parallel tasks execution
 - pipeline stages (named groups)
 - shell script execution: inline and file
 - environment variables merged across each level: matrix, pipeline, stage, and tasks
 - support for model data (a dictionary of anything you need)
 - cleanup hook
 - filtered execution via tags
 - supporting Jinja templating in Bash scripts (also nested inside model)
 - support for Docker containers and Docker images
 - execution time on each level: pipeline, stage, tasks and shell (event logging)
 - documentation here and also at read the docs
 - usable by Jenkinsfile as well as by a `.travis.yml` (or other pipelines).

## <a name="links">Interesting Links</a>

 - https://github.com/keleshev/schema
 - https://github.com/bats-core/bats-core
 - https://pypi.python.org/pypi/PyHamcrest
 - http://nose.readthedocs.io/en/latest/
 - https://pypi.python.org/pypi/bandit
