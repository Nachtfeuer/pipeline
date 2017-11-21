The Shell
=========

One line
--------
The shell is a yaml definition for executing a Bash script.

::

    - shell:
        script: echo "hello world!"

As an alternative when given script content is a valid path and filename
of an existing Bash script then those one will be taken. Please note
that the content of each script is copied into a temporary one and executed.

Multipe lines
-------------
You also can have multiple lines:

::

    - shell:
        script: |
            echo "hello world 1!"
            echo "hello world 2!"

Jinja templating supported
--------------------------
Jinja templating is supported. Currently two variables
are supported: **env** and **model**:

**env**

  Gives you access to the environment variables as defined when the
  spline tool has been started; in addition you can add environment
  variables or overwrite existing ones. Please note that the value
  is always a string.

**model**

  The model is a dictionary (map) with keys and the values can be
  any valid yaml construct that results in a valid Python data
  hierarchy.

Here's a simple example for the access:

::

    - tasks:
        - env:
            count: "3"

        - shell:
            script: |
                {% for c in range(env.count|int) %}
                echo "{{ c+1 }}:{{ env.message }}"
                {% endfor %}
                echo "USER={{ env.USER }}"
                echo "foo={{ model['foo'] }}"


More details on **env** and **model** you can see in a separate chapter.

Tags
----
Finally you can specify tags:

::

    - shell:
        script: echo "hello world!"
        tags:
            - simple
    - shell:
        script: echo "hello world!"
        tags:
            - test

Executing the spline tool you can specify **--tags=test** which
executes shells only with given tag. You also can specify a
comma separted list of tags to allow more shells: **--tags=test,simple**

One usecase might be to isolate a shell for testing purpose.
