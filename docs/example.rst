Real Example
============

Python and tox
--------------
Like for Java using Maven or Gradle or using CMake for C++ is tox a tool for Python.
It does simplify the support for multiple Python version and the quite comfortable
description of the commands and its environments. The spline project has a complete
demo project for Python in folder **examples/python/primes**.

Quickstart
----------
You require spline >= 1.2. It's possible to run tox without parameters
but then you need to have all listed Python versions installed.
I usually have Python 2.7.x and Pyton 3.5.x on my machine so I could test
the project like following: **-e py27 -e py25**. 

::

    pip install spline tox --upgrade
    git clone https://github.com/Nachtfeuer/pipeline.git
    cd pipeline/examples/python/primes
    tox -e py27

The tox.ini covers:
 - pep8 (tox -e pep8)
 - pep257 (tox -e pep257)
 - pylint (tox -e pylint)
 - flake8 (tox -e flake8)
 - radon (tox -e radon)
 - nosetests (tox -e tests, tests with pyhamcrest, 100% coverage as limit)
 - packaging (tox -e package wheel file)

Using commands like **tox -e radon** it does use the
Python version on your host.

Spline and matrix build
-----------------------
However the different Python versions will introduce different
behavior (often) so you constantly have to verify. The spline tool does help
you with this by isolating builds into Docker containers; with
this you can test even locally **all** Python version also you
have just one Python version on your machine.

So let's start with the matrix definition:

::

    matrix:
    - name: Python 2.7
        env: {PYTHON_VERSION: py27}
    - name: Python 3.5
        env: {PYTHON_VERSION: py35}

Keeping it simple (demo) I defined just two Python versions
but with given examples it's pretty easy to add more. The
given setup will inject the environment variable **PYTHON_VERSION**
to be used as filter.

The model
---------
The next step is to define a **model**:

::

    model:
        templates:
            init_py27: |
                yum -y install centos-release-scl yum-utils git
                yum-config-manager --enable rhel-server-rhscl-7-rpms
                yum -y install python27
                scl enable python27 "bash -c \"pip install setuptools --upgrade\""
                scl enable python27 "bash -c \"pip install tox\""
                scl enable python27 "bash -c \"{{ env.PIPELINE_BASH_FILE }} RUN\""

The Python 3.5 part is also contained (see pipeline.yaml).
The main point here to understand is that **scl enable** does use
a mechanism where you have to specify script that is executed **in context**
of the specified environent (here: python27). The variable **PIPELINE_BASH_FILE**
is generated/injected by the **spline** tool. You either can refer to by $ syntax (Bash)
or using Jinja2 syntax (as done here).

The init part of the script
---------------------------
The Bash script that is calling your code running inside a Docker container is
called first time with the parameter **INIT**. The Bash case structure
handles that rendering the Python template we need for the currently running
matrix; so we have to fetch exactly that template from the model which
relates to current **PYTHON_VERSION**. Because the template also contains
Jinja2 code we have to apply the **render** filter passing the environment
variables. The template (last line of it) does call the build script again
but now with parameter **RUN** which gives you the possibility to implement
your build process inside the Docker container **and** inside the correct
Python environment.

::

      - docker(container):
          mount: yes
          script: |
            case $1 in
              INIT)
                {{ model.templates['init_'+env.PYTHON_VERSION]|render(env=env) }}
                ;;
              RUN)
                echo "Running build with $(python -V)"
                ;;

The run part of the script
--------------------------
Of course we don't print just the Python version (as shown before); the final
**RUN** case looks like following:

::

    RUN)
        echo "Running build with $(python -V)"
        mkdir /build

        # copying all files under version into the container
        pushd /mnt/host/examples/python/primes
        tar cvzf /build/demo.tar.gz $(git ls-files)
        popd

        pushd /build
        # unpacking the copied sources files
        tar xvzf demo.tar.gz
        rm -f demo.tar.gz
        # running the build
        tox -e {{ env.PYTHON_VERSION }}
        popd
        ;;

We are inside the Docker container and also running in context
of a concrete Python version. Now a build folder will be generated
where we place the Python code. It's not optimal to run directly on the
shared workspace (repository) because:

 - The Docker standard user is root and generate files and folders
   on the Docker host probably raise permission issues when it comes
   to cleanup. Yes you can organize to be same user as in the host
   but with some effort (my personal opinion: avoid it).
 - If you run in parallel you share folders even when they are
   temporary build output (my personal opinion: avoid it).
 - On some systems the exchange of files and folders on those Docker
   mounts is expensive.

That's why I have choosen the variant to use Git since Git exactly knows
all files (and folders) under versions copying it into the build folder
of the Docker container. After unpacking you simply call **tox -e {{ env.PYTHON_VERSION }}**
and your build runs fully "locally".

The last lines (I don't print all - too many lines) look like following:

::

    2017-12-10 11:50:06,230 - spline.components.tasks -  | creating build/bdist.linux-x86_64/wheel/pipeline_demo_python_primes-1.0.dist-info/WHEEL
    2017-12-10 11:50:06,230 - spline.components.tasks -  | ___________________________________ summary ____________________________________
    2017-12-10 11:50:06,230 - spline.components.tasks -  |   py27: commands succeeded
    2017-12-10 11:50:06,230 - spline.components.tasks -  |   congratulations :)
    ...
    2017-12-10 11:51:24,231 - spline.components.tasks -  | creating build/bdist.linux-x86_64/wheel/pipeline_demo_python_primes-1.0.dist-info/WHEEL
    2017-12-10 11:51:24,231 - spline.components.tasks -  | ___________________________________ summary ____________________________________
    2017-12-10 11:51:24,232 - spline.components.tasks -  |   py35: commands succeeded
    2017-12-10 11:51:24,232 - spline.components.tasks -  |   congratulations :)

Run the build
-------------
Remains to show how the matrix build is executed.
For the demo inside the spline repository you have
to be in the root of it (because git requires .git from mount):

::

     spline --definition=examples/python/primes/pipeline.yaml

That's all.

Some final notes
----------------
 - For the moment it seems that the output of one Bash execution is passed back to
   the called after finish of it which results in a delay until you see something.
   I have filed an issue: #28: Asynchronous Bash execution. When I find a solution
   then I will remove this point.
 - If you copy back things into workspace (mount) keep in mind to use
   **chown -R ${UID}:${GID} <path or file>**.
