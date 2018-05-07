"""Wrapper for Ansible tool."""
# Copyright (c) 2018 Thomas Lehmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# pylint: disable=useless-super-delegation
import os
from spline.components.bash import Bash
from spline.tools.filters import render
from spline.tools.stream import write_temporary_file


class Ansible(Bash):
    """
    Wrapper for Ansible tool.

    .. inheritance-diagram:: Image
    """

    def __init__(self, config):
        """Initialize with Bash code (do not call it directly)."""
        super(Ansible, self).__init__(config)

    @staticmethod
    def creator(entry, config):
        """Creator function for creating an instance of an Ansible script."""
        ansible_playbook = "ansible.playbook.dry.run.see.comment"
        ansible_inventory = "ansible.inventory.dry.run.see.comment"

        ansible_playbook_content = render(config.script, model=config.model, env=config.env,
                                          variables=config.variables, item=config.item)
        ansible_inventory_content = render(entry['inventory'], model=config.model, env=config.env,
                                           variables=config.variables, item=config.item)

        if not config.dry_run:
            ansible_playbook = write_temporary_file(ansible_playbook_content, 'ansible-play-', '.yaml')
            ansible_playbook_content = ''
            ansible_inventory = write_temporary_file(ansible_inventory_content, prefix='ansible-inventory-')
            ansible_inventory_content = ''

        # rendering the Bash script for running the Ansible playbook
        template_file = os.path.join(os.path.dirname(__file__), 'templates/ansible.sh.j2')
        with open(template_file) as handle:
            template = handle.read()
            config.script = render(template, debug=config.debug,
                                   ansible_playbook_content=ansible_playbook_content,
                                   ansible_playbook=ansible_playbook,
                                   ansible_inventory_content=ansible_inventory_content,
                                   ansible_inventory=ansible_inventory,
                                   limit=entry['limit'])

        return Ansible(config)
