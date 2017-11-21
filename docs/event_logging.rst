The Even logging
================
With the command line option `--event-logging` you enable additional logging that
measures execution time on the whole application, each pipeline, stage, tasks and docker/shell level.

::

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

