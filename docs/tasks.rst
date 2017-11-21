The Tasks
=========

It's a list of tasks basically meaning a shell as Bash script or runnning
inside a Docker container. Tasks can be **ordered** or **parallel**.

Ordered tasks
-------------

Ordered tasks can written as ``- tasks:`` or as ``- tasks(ordered):``
(the way you prefer). It means the same: one shell script is executed after the other:

 ::

    - tasks(ordered):
        - shell:
            script: echo "hello world one!"
        - shell:
            script: echo "hello world two!"

Parallel tasks
--------------
All tasks are running in parallel as much as possible. The
Python module **multiprocessing** is used.

 ::

    - tasks(parallel):
        - shell:
            script: echo "hello world one!"
        - shell:
            script: echo "hello world two!"

**Please note**:
 - It's not a good idea to interrupt the pipeline with Ctrl-C
 - (Example:) When you have 4 cpus but more than 4 tasks it might happen
   that the tasks do not finish in time constraints as you expect. It
   seems that one task is assigned to one cpu only at a time.
 - When one task fails the pipeline stops after all tasks has been
   finished.
 - When using multiple enviroment blocks tasks run in parallel only
   between two of those "env" blocks.

Environment variables
---------------------
Besides a tasks the list also may contain one or more blocks for environment variables.

::

    - env:
        a: "hello"
        b: "world"

The last block overwrites the previous one; existing variables
are overwriten, new ones are added.
