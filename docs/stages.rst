Pipeline stages
===============
Each stage is a list of tasks blocks. It also may have environment blocks.

::
    - stage(one):
        - env:
            mode: test

        - tasks(ordered):
            - shell:
                script: echo "{{ env.mode }}: script one"

        - tasks(ordered):
            - shell:
                script: echo "{{ env.mode }}: script two"

The stage name in the round brackets can be any text. It's assumed that a 
stage should reflect the individual phases of the a CI/CD pipeline including (unordered):
 - preparation
 - build
 - unittests
 - static code analysis
 - packaging
 - integration/regression tests
 - image creation (docker, AWS, ...)
 - deployment
