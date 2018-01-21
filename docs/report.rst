The one file report
===================

Introduction
------------
At the moment a one file HTML is supported only. On updates (stages) the
tool overwrites same file each time which current report data displaying
a table showing each matrix and each stage.

 - a green cell indicates a successful completed stage
 - a red cell indicates a failed stage
 - a yellow stage indicates a stage that has not been processed

Information as currently the state (started, succeeded and failed) and
the duration.

You enable it by using the command line option `--report` (default: off)

::

    spline --definition=examples/matrix.yaml --report=html

For the moment you cannot specify the output path and filename;
it will be written to current working directory as `pipeline.html`.


Example
-------
.. image:: images/pipeline.png


Multiprocessing
---------------
When running the matrixes in parallel then multiple processes are spawned.
Using Python multiprocessing each process does send information via a
queue to the collector (main process). The collector finally writes
the `pipeline.yaml` on each update.


Refresh
-------
The generated HTML does have a meta information that enforced refreshing of
the page each 5 seconds allowing to see the progress of your pipelines.

