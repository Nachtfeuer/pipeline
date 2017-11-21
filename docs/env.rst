The Environment Variables
=========================

::

    pipeline:
    - env:
        a: "hello"

    - stage(Environment Variables):
        - env:
            b: "world"

        - tasks(ordered):
            - env:
                c: "for all"

            - shell:
                script: |
                    echo "a=$a"
                    echo "b=$b"
                    echo "c=$c"

An extract from the output when running the pipeline:

::

    2017-11-20 18:47:08,209 - spline.components.bash - Running script /tmp/pipeline-script-w2MUih.sh
    2017-11-20 18:47:08,215 - spline.components.tasks -  | a=hello
    2017-11-20 18:47:08,215 - spline.components.tasks -  | b=world
    2017-11-20 18:47:08,216 - spline.components.tasks -  | c=for all

All defined variables are merged together:

 - first all environment variables on pipeline level are taken
 - in the resulting dictionary all environment variables from stage level are used for updating. New variables
   are added and existing variables are overwritten.
 - in the resulting dictionary all environment variables from tasks level are used for updating. New variables
   are added and existing variables are overwritten.

**Please note**: All values have to be strings.

In a Bash script you also can refer to the variables using
Jinja templating like ``{{ env.a }}``.