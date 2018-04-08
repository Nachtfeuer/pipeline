Conditional Tasks
=================

Introduction
------------
Conditional tasks allow you to run certain tasks when the defined
condition evaluates to true only. At the moment you can use such conditions
on each task: shell, docker(container), docker(image) and python.

Data sources
------------
There are three sources of information
that can be used the moment (via Jinja templating):

 - model variables - constant definition in the yaml file.
 - task variables - see different type of tasks using the field **variable**
 - environment variables - see the **env** entry usable on **matrix**, **pipeline**, **stage** and **tasks**

Rules
-----
You have to comply some rules when using conditions. Following variants of conditions
are intended:

 - `{{ variables.cpu_count }} == 1` - comparison of two integers to be equal
 - `not {{ variables.cpu_count }} == 1` - comparison of two integers to be not equal
 - `{{ variables.cpu_count }} > 1` - comparison of one integer to be greater than another
 - `{{ variables.cpu_count }} >= 1` - comparison of one integer to be greater or equal than another
 - `{{ variables.cpu_count }} < 2` - comparison of one integer to be less than another
 - `{{ variables.cpu_count }} <= 2` - comparison of one integer to be less or equal than another
 - `"{{ env.BRANCH_NAME }}" == "master"` - comparison of two strings to be equal
 - `not "{{ env.BRANCH_NAME }}" == "master"` - comparison of two strings to be not equal
 - `{{ variables.cpu_count }} in [1, 2]` - integer contained in a list of integers
 - `{{ variables.cpu_count }} not in [1, 2]` - integer not ontained in a list of integers
 - `"{{ env.BRANCH_NAME }}" in ["master", "release"]` - comparison contained in a list of strings
 - `"{{ env.BRANCH_NAME }}" not in ["master", "release"]` - comparison not contained in a list of strings

**Please note**: all other combination that might work should **not** be considered. Future versions
of the spline tool will improve the condition checks to be more strict.

**Please note**: When the jinja templating finally produces a condition with wrong syntax
each thrown exception will evaluate the related condition to false. Please check the logs for details then.

Examples
--------
You can see examples in the file `conditions.yaml` of the tool repository;
here is an extract of it:

::

    - shell:
        script: echo "integer in integer list comparison"
        when: "{{ model.intval }} in [1234, 4321]"
    - shell:
        # task output should not be shown
        script: echo "integer not in integer list comparison"
        when: "{{ model.intval }} not in [1234, 4321]"
