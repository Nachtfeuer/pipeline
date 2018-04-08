The Ansible(simple) Task
========================

The Ansible task provides you a subset of Ansible; mainly
the focus is to have an inventory file (hosts) and one playbook
maintainable by one spline document.

Example
-------
The next example you can see in the folder with same name in file `ansible-docker.yaml`.
One Docker container is organized to have **sshd** installed and the Ansible connects
to that container installing a few packages.

::

    - ansible(simple):
        inventory: |
            [all]
            localhost ansible_host={{ variables.container_host }} ansible_port=22 ansible_connection=ssh ansible_ssh_user=root ansible_ssh_pass={{ env.PASS }}
        limit: all
        script: |
        - hosts: all
            tasks:
            - name: Install packages
                yum:
                name: "{%raw%}{{ item }}{%endraw%}"
                state: present
                with_items:
                {% for package in model.packages %}
                  - {{ package }}
                {% endfor %}

Notes on Jinja Templating
-------------------------
Spline does use Jinja2 for templating and Ansible does it as well.
You have to control when the templating applies and when not.
In given example we would like to have a playbook that finally
looks like following:

::

    - hosts: all
        tasks:
        - name: Install packages
            yum:
            name: "{{ item }}"
            state: present
            with_items:
              - curl
              - git
              - cmake

That's why the evaluation of **item** has been suppressed.
Also you cannot insert the packages just by writing **{{ model.packages }}**
but the result is a Python list with 3 strings. Three lines with
items are wanted (as you can see above); of course a filter could apply
rendering as yaml syntax but then you also have to manage indentation which
turned out to be difficult (have not found a way to pass current indentation).

Hosts, ports, user and password
-------------------------------
For the  Docker example it was sufficient to define user and password in the inventory
file. Of course credentials in code are not fine but you can inject the credential from
outside (environment variable) or you use the mechanism only for setting up a
regression environment with no access to any production environment.

Reading the documentation about Ansible inventory you also shoud be able to
use **ansible_ssh_private_key_file**.

Please read: http://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html
