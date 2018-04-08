The Pipeline matrix
===================

Usage
-----
A matrix basically has a name and assigned environment variables. The purpose is
to support that same pipeline can run for different parameters. Examples are
running with different compilers, interpreters or databases. In addition you can
specify tags which allow to filter for certain matrix runs.

::

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


With this example you can filter for second matrix item like this:

::

    pipeline --definition=example.yaml --matrix-tags=second


Parallelization
---------------
While **matrix** as well as **matrix(ordered)** are representing ordered pipeline execution
you also can specify **matrix(parallel)**. Using parallel all specified matrix items (pipeines)
are running in parallel. Parallel matrixs and parallel tasks can be combined.

Be aware that parallelization works just as good as many cpu you have and as less competition.
