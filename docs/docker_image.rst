The Docker Image Script
===========================

Simple example
--------------
The next example demonstrates one way on how to create a
docker image for Python 3.6.

::

      - docker(image):
          name: python
          tag: "3.6"
          unique: no
          script: |
            FROM centos:7
            RUN yum -y install yum-utils git
            RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
            RUN yum -y install python36u python36u-pip
            RUN pip3.6 install tox

When you run this (see examples folder for docker-image.yaml) then last
lines should look like following:

::

    2017-12-22 09:20:15,179 - spline.components.tasks -  | Installing collected packages: py, six, pluggy, virtualenv, tox
    2017-12-22 09:20:15,339 - spline.components.tasks -  |   Running setup.py install for pluggy: started
    2017-12-22 09:20:15,665 - spline.components.tasks -  |     Running setup.py install for pluggy: finished with status 'done'
    2017-12-22 09:20:15,800 - spline.components.tasks -  | Successfully installed pluggy-0.6.0 py-1.5.2 six-1.11.0 tox-2.9.1 virtualenv-15.1.0
    2017-12-22 09:20:16,588 - spline.components.tasks -  |  ---> 29abbe7ec073
    2017-12-22 09:20:16,601 - spline.components.tasks -  | Removing intermediate container 5ceeb0cf5b89
    2017-12-22 09:20:16,601 - spline.components.tasks -  | Successfully built 29abbe7ec073
    2017-12-22 09:20:16,608 - spline.components.tasks -  | Successfully tagged python:3.6
    2017-12-22 09:20:16,610 - spline.components.bash - Exit code has been 0
    2017-12-22 09:20:16,611 - spline.components.tasks - Processing Bash code: finished

You can verify afterwards:

::

    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    python              3.6                 29abbe7ec073        9 minutes ago       605MB
    $ docker run --rm -i python:3.6 bash -c "python3.6 -V"
    Python 3.6.3

The option "unique"
-------------------
In the example above **unique** has been set to **no**.
The default is **yes** which injects the pid of the spline tool
into the name. The idea is to allow multiple images generated in
parallel without conflicts.

Dockerfile
----------
The **script** field represents the Dockerfile and please refer
to the official Documentation if you need to know more.
However Jinja2 templating is supported:

::

      - docker(image):
          name: python
          tag: "3.6"
          unique: no
          script: "{{ model.templates.dockerfiles.py36 }}"

**Please note**: you also can use jinja templaring in the tag.


The compete example - as already mentioned - in the examples folder.


Conditional tasks
-----------------
The field **when** allows you to define a condition; when evaluated as true then
the task is executed otherwise not. More details you can read in the separate
section `Conditional Tasks`.
