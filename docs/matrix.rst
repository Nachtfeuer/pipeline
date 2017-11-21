The Pipeline matrix
===================
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


