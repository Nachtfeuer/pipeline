"""Module version."""
import json
from spline.version import VERSION
from spline.components.config import ShellConfig
from spline.components.bash import Bash
from spline.tools.logger import Logger


class VersionsReport(object):
    """Logging versions of required tools."""

    LOGGER = Logger.get_logger(__name__)
    """Logger instance for this class."""

    def __init__(self):
        """Do nothing the moment."""
        pass

    def process(self, document):
        """Logging versions of required tools."""
        content = json.dumps(document)

        self.LOGGER.info('Using: %-10s version: %s', 'Spline', VERSION)
        bash_version = r'''bash --version|head -1|grep -Po "\d+\.\d+\.\d+"'''
        self._log_version("Bash", bash_version)

        if content.find('"docker(container)":') >= 0 or content.find('"docker(image)":') >= 0:
            docker_version = r'''docker version|grep "Version:"|head -1|grep -Po "\d+\.\d+\.\d+"'''
            self._log_version("Docker", docker_version)
        if content.find('"packer":') >= 0:
            packer_version = r'''packer -version'''
            self._log_version("Packer", packer_version)
        if content.find('"ansible(simple)":') >= 0:
            ansible_version = r'''ansible --version|grep -Po "\d+\.\d+\.\d+\.\d+"'''
            self._log_version('Ansible', ansible_version)

    def _log_version(self, tool_name, tool_command):
        """
        Logging name and version of a tool defined by given command.

        Args:
            tool_name (str): name of the tool.
            tool_command (str): Bash one line command to get the version of the tool.
        """
        for line in Bash(ShellConfig(script=tool_command, internal=True)).process():
            self.LOGGER.info("Using: %-10s version: %s", tool_name, line)
