The pipeline
============
The pipeline is a list of stages. It also may have environment blocks.

::

    pipeline:
    - env:
        mode: test

    - stage(one):
        - tasks(ordered):
        - shell:
            script: echo "{{ env.mode }}: script one"

    - stage(two):
        - tasks(ordered):
        - shell:
            script: echo "{{ env.mode }}: script two"

