# Welcome to spline - the pipeline tool

[![PyPI version](https://img.shields.io/pypi/v/spline.svg)](https://pypi.python.org/pypi/spline)
[![PyPI format](https://img.shields.io/pypi/format/spline.svg)](https://pypi.python.org/pypi/spline)
[![PyPI versions](https://img.shields.io/pypi/pyversions/spline.svg)](https://pypi.python.org/pypi/spline)
[![PyPI license](https://img.shields.io/pypi/l/spline.svg)](https://pypi.python.org/pypi/spline)
[![Read The Docs](https://readthedocs.org/projects/spline/badge/?version=latest)](http://spline.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/Nachtfeuer/pipeline/badge.svg?branch=master&service=github)](https://coveralls.io/github/Nachtfeuer/pipeline?branch=master)
[![BCH compliance](https://bettercodehub.com/edge/badge/Nachtfeuer/pipeline?branch=master)](https://bettercodehub.com/)
[![Known Vulnerabilities](https://snyk.io/test/github/nachtfeuer/pipeline/badge.svg)](https://snyk.io/test/github/nachtfeuer/pipeline)

---

**Important note**:

Since change in my job I didn't had the chance to continue on this project. My main new project is
here https://github.com/thomas-lehmann-private/hyperion-task-processor which is planned to be
a improved task processing tool; step by step those one will be capable to have more functionality across all platforms
(powershell, batch, bash, JShell, Groovy, Kotlin, Docker, ... features depend on platform). It's fully written in Java. Stay tuned.

---

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
[Include](docs/include.rst)  
[Event Logging](docs/event_logging.rst)  
[Tool: spline-loc](docs/spline_loc.rst)  
[How to contact?](#contact)  
[Links](#links)  

**Features**:
 - Python support for 2.7.x, 3.4.x, 3.5.x, 3.6.x, PyPy and PyPy3
 - automatic schema validation for yaml file
 - matrix based pipeline with tags
 - ordered and parallel pipelines (matrix)
 - ordered and parallel tasks execution
 - pipeline stages (named groups)
 - shell script execution: inline and file
 - environment variables merged across each level: matrix, pipeline, stage, and tasks
 - support for model data (a dictionary of anything you need)
 - cleanup hook
 - filtered execution via tags
 - supporting Jinja templating in Bash scripts (also nested inside model)
 - support for Docker containers and Docker images
 - support for the Packer tool
 - execution time on each level: pipeline, stage, tasks and shell (event logging)
 - documentation here and also at read the docs
 - usable by Jenkinsfile as well as by a `.travis.yml` (or other pipelines).
 - dry run and debug support
 - support for Python scripts
 - support for task variables
 - support for conditional tasks
 - enabled for code reuse: !include statement

## <a name="contact">How to contact?</a>
 - https://groups.google.com/forum/#!forum/spline-the-pipeline-tool
 - https://github.com/Nachtfeuer/pipeline/issues


## <a name="links">Interesting Links</a>

 - https://github.com/keleshev/schema
 - https://github.com/bats-core/bats-core
 - https://pypi.python.org/pypi/PyHamcrest
 - https://pypi.python.org/pypi/bandit
 - https://www.contributor-covenant.org/
 - http://ddt.readthedocs.io/en/latest/index.html
 - http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
 - https://pymotw.com/2/multiprocessing/communication.html
 - https://regex101.com/
 - https://www.packer.io/intro/index.html
