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
are available:

**env**

  Gives you access to the environment variables as defined when the
  spline tool has been started; in addition you can add environment
  variables or overwrite existing ones. Please note that the value
  is always a string.

**model**

  The model is a dictionary (map) with keys and the values can be
  any valid yaml construct that results in a valid Python data
  hierarchy.

**variables**

  You can specify a field **variable** on each shell and the output of the
  Bash will be stored under the defined name. However a special note
  on this: when you define a task block for parallel tasks then one task
  cannot access a variable by another parallel task in same execution block;
  but when such tasks are separated by an **env** entry each task after that
  entry is able to use it also those run in parallel too. More on this you
  can read in the chapter about tasks.

Here's a simple example for the access:

::

    - tasks:
        - env:
            count: "3"

        - shell:
            script: echo "{{ env.USER }}"
            variable: user

        - shell:
            script: |
                {% for c in range(env.count|int) %}
                echo "{{ c+1 }}:{{ env.message }}"
                {% endfor %}
                echo "USER={{ variables.user }}"
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

"With" attribute
----------------
Using the **with** attribute you can run same task as often as many entries you provide.
The entries are representing a list but the item can be any valid yaml structure; in the
example a dictionary is used:

::

    - shell:
        script: |
            echo "{{ item.message }}: start"
            sleep {{ item.time }}
            echo "{{ item.message }}: done"
        with:
            - message: first
              time: 3
            - message: second
              time: 2
            - message: third
              time: 1

Finally all generated tasks (shell or docker container) are added to the
list of tasks to be processed and it depends on the setup of the **tasks**
block whether those tasks are executed in **order** or in **parallel**.
Please have a look and try the example **with.yaml** in the repository.

Colors
------
Colors are working fine!

::

    - shell:
        script: |
            echo -e "\e[31mRed World\e[0m"
            echo -e "\e[33mOrange World\e[0m"
            echo -e "\e[34mBlue World\e[0m"
            echo -e "\e[35mMagenta World\e[0m"

Conditional tasks
-----------------
The field **when** allows you to define a condition; when evaluated as true then
the task is executed otherwise not. More details you can read in the separate
section `Conditional Tasks`.
