The Model
=========

Introduction
------------
The model is a flexible way to define data.
For the moment you can define it only once at
global level:

::

    model:
        max-number: 100

    pipeline:
        - stage(Calculate Primes):
            - tasks(ordered):
                - shell:
                    script: |
                        function is_prime() {
                            n=$1
                            if [ "${n}" -lt 2 ]; then return; fi
                            if [ "$(expr $n % 2)" -eq 0 ]; then
                                if [ "${n}" == "2" ]; then echo "yes"; fi
                                return;
                            fi
                            d=$(echo "sqrt(${n})"|bc)
                            for k in $(seq 3 2 ${d}); do
                                if [ "$(expr $n % $k)" -eq 0 ]; then return; fi
                            done
                            echo "yes"
                        }

                        for n in $(seq 0 {{ model['max-number'] }}); do
                            if [ "$(is_prime ${n})" == "yes" ]; then
                                echo -n "${n} ";
                            fi
                        done
                    tags:
                        - embedded

The output looks like following:

::

    $ spline --definition=examples/primes.yaml --tags=embedded
    2017-11-20 05:53:45,150 - spline.application - Running with Python 2.7.13 (default, Jan 19 2017, 14:48:08) [GCC 6.3.0 20170118]
    2017-11-20 05:53:45,177 - spline.application - Running on platform Linux-4.9.0-3-amd64-x86_64-with-debian-9.1
    2017-11-20 05:53:45,177 - spline.application - Processing pipeline definition 'examples/primes.yaml'
    2017-11-20 05:53:45,210 - spline.application - Schema validation for 'examples/primes.yaml' succeeded
    2017-11-20 05:53:45,214 - spline.components.stage - Processing pipeline stage 'Calculate Primes'
    2017-11-20 05:53:45,214 - spline.components.tasks - Processing group of tasks
    2017-11-20 05:53:45,215 - spline.components.tasks - Processing Bash code: start
    2017-11-20 05:53:45,220 - spline.components.bash - Running script /tmp/pipeline-script-i6l5rx.sh
    2017-11-20 05:53:46,261 - spline.components.tasks -  | 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97
    2017-11-20 05:53:46,261 - spline.components.bash - Exit code has been 0
    2017-11-20 05:53:46,262 - spline.components.tasks - Processing Bash code: finished

As an alternative you also can do it like following:

::

    model:
        max-number: 100

    pipeline:
        - stage(Calculate Primes):
            - tasks(ordered):
                - shell:
                    script: examples/primes.sh {{ model['max-number'] }}
                    tags:
                        - file

For completeness:

::

    $ spline --definition=examples/primes.yaml --tags=file

Lists in yaml will be converted into Python lists and yaml dictionaries
will be converted into Python dictionaries. All basically as you would
expect.

Nested templates
----------------
The model also can be used for storing templates that can be injected into scripts.
You probably also would like to pass then the model and environment variables to it:

```
model:
    templates:
        script: |
            echo "{{ model.message }} {{ env.who }}!"
    message: "hello"

pipeline:
    - env:
        who: world

    - stage(Test):
        - tasks(ordered):
            - shell:
                script: "{{ model.templates.script|render(model=model, env=env) }}"
```

That's just a very simple example.
