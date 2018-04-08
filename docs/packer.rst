The Packer Task
===============

Setup
-----
You have to ensure that the packer tool is installed and in the search path.
The installation is simple (mainly download, unpack and copy of one binary).

Simpe Example
-------------

The next example demonstrates how you can use the packer
task to generate a Docker image:

::

    - packer:
        script: |
            {"builders": [{
                "type": "docker",
                "image": "{{ model.image }}",
                "commit": true,
                "changes": [
                    "LABEL pipeline={{ env.PIPELINE_PID }}",
                    "LABEL pipeline-stage={{ env.PIPELINE_STAGE }}"
                ]
            }],

            "provisioners": [{
                "type": "shell",
                "inline": [
                    "yum -y install python-setuptools",
                    "easy_install pip",
                    "pip install tox"
                ]
            }],

            "post-processors": [{
                "type": "docker-tag",
                "repository": "spline/packer/demo",
                "tag": "0.1"
            }]}

The output looks like following starting with:

::

    2018-03-16 05:20:50,948 - spline.components.bash - Running script /tmp/pipeline-script-5N9ZeH.sh
    2018-03-16 05:20:50,955 - spline.components.tasks -  | packer build  /tmp/packer-e7je86.json
    2018-03-16 05:20:51,125 - spline.components.tasks -  | docker output will be in this color.
    2018-03-16 05:20:51,128 - spline.components.tasks -  |
    2018-03-16 05:20:51,163 - spline.components.tasks -  | ==> docker: Creating a temporary directory for sharing data...
    2018-03-16 05:20:51,164 - spline.components.tasks -  | ==> docker: Pulling Docker image: centos:7
    2018-03-16 05:21:03,703 - spline.components.tasks -  |     docker: 7: Pulling from library/centos
    2018-03-16 05:21:14,557 - spline.components.tasks -  |     docker: Digest: sha256:dcbc4e5e7052ea2306eed59563da1fec09196f2ecacbe042acbdcd2b44b05270
    2018-03-16 05:21:14,559 - spline.components.tasks -  |     docker: Status: Image is up to date for centos:7
    2018-03-16 05:21:14,561 - spline.components.tasks -  | ==> docker: Starting docker container...
    2018-03-16 05:21:14,564 - spline.components.tasks -  |     docker: Run command: docker run -v /home/thomas/.packer.d/tmp/packer-docker809184673:/packer-files -d -i -t centos:7 /bin/bash
    2018-03-16 05:21:15,115 - spline.components.tasks -  |     docker: Container ID: 2543f16b4acc3e107ef7ce5b1e8164d66bfbc0a0a34ad682c3b75db390677e80
    2018-03-16 05:21:15,198 - spline.components.tasks -  | ==> docker: Provisioning with shell script: /tmp/packer-shell164186494
    2018-03-16 05:21:16,627 - spline.components.tasks -  |     docker: Loaded plugins: fastestmirror, ovl
    2018-03-16 05:21:25,764 - spline.components.tasks -  |     docker: Determining fastest mirrors
    2018-03-16 05:21:27,312 - spline.components.tasks -  |     docker:  * base: centos.intergenia.de
    2018-03-16 05:21:27,316 - spline.components.tasks -  |     docker:  * extras: centos.intergenia.de
    2018-03-16 05:21:27,319 - spline.components.tasks -  |     docker:  * updates: mirror.fra10.de.leaseweb.net
    2018-03-16 05:21:30,280 - spline.components.tasks -  |     docker: Resolving Dependencies
    2018-03-16 05:21:30,281 - spline.components.tasks -  |     docker: --> Running transaction check
    2018-03-16 05:21:30,282 - spline.components.tasks -  |     docker: ---> Package python-setuptools.noarch 0:0.9.8-7.el7 will be installed

and finishing with:

::

    2018-03-16 05:21:39,991 - spline.components.tasks -  | ==> docker: Committing the container
    2018-03-16 05:21:41,831 - spline.components.tasks -  |     docker: Image ID: sha256:270dbc58a828269a069142c8cef9c7d93c735b9217d617ee123cd5c4e2d552a2
    2018-03-16 05:21:41,832 - spline.components.tasks -  | ==> docker: Killing the container: 2543f16b4acc3e107ef7ce5b1e8164d66bfbc0a0a34ad682c3b75db390677e80
    2018-03-16 05:21:42,380 - spline.components.tasks -  | ==> docker: Running post-processor: docker-tag
    2018-03-16 05:21:42,385 - spline.components.tasks -  |     docker (docker-tag): Tagging image: sha256:270dbc58a828269a069142c8cef9c7d93c735b9217d617ee123cd5c4e2d552a2
    2018-03-16 05:21:42,385 - spline.components.tasks -  |     docker (docker-tag): Repository: spline/packer/demo:0.1
    2018-03-16 05:21:42,451 - spline.components.tasks -  | Build 'docker' finished.
    2018-03-16 05:21:42,452 - spline.components.tasks -  |
    2018-03-16 05:21:42,452 - spline.components.tasks -  | ==> Builds finished. The artifacts of successful builds are:
    2018-03-16 05:21:42,455 - spline.components.tasks -  | --> docker: Imported Docker image: sha256:270dbc58a828269a069142c8cef9c7d93c735b9217d617ee123cd5c4e2d552a2
    2018-03-16 05:21:42,457 - spline.components.tasks -  | --> docker: Imported Docker image: spline/packer/demo:0.1
    2018-03-16 05:21:43,344 - spline.components.bash - Exit code has been 0
    2018-03-16 05:21:43,345 - spline.components.tasks - Processing Bash code: finished

Important notes
---------------

 - **you don't require packer variables**:  Because you directly can use Jinja2 templating you don't require
   variables in the Packer script.
 - **You are responsible**: It depends on you what you are generating and how you do it. The example is just
   for Docker but Packer does support more image types. Spline does not know how to cleanup things here.
   Also you have to ensure unique names (if wanted) considering builds running in parallel avoiding
   any conflicts. The `docker(image)` task (as comparison) injects the spline pid into the image name;
   you can do it easily using Jinja2 templating but you have to do it yourself.
 - **No filter**: You can have multiple builders in packer and when use them the packer task generates all
   images (`-only` and  `-except` options are not used).
 - Packer is enabled for parallelization
 - When the build does fail Packer does the cleanup.
 - The spline option `--debug` will be passed as `-debug` to the **packer build** command.
   **Please pay attention here**: you have to press enter for individual steps.
