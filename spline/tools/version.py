"""Module version."""
import sys
import re
import json
from spline.version import VERSION
from spline.components.config import ShellConfig
from spline.components.bash import Bash
from spline.tools.logger import Logger


class Version(object):
    """
    Version class to allow comparing versions.

    >>> a, b, c = Version("1.2"), Version("1.3"), Version("1.4")
    >>> a < b, b < a, a < c, b < c, c > b, b > c, a == a
    (True, False, True, True, True, False, True)
    """

    def __init__(self, version):
        """Initialize with version string like 1.2.3."""
        self.version = version.split('.')

    def __repr__(self):
        """String representation of this class."""
        return "Version(%s)" % (".".join(self.version))

    def __eq__(self, other):
        """Comparing two versions to be equal."""
        result = True
        if not id(self) == id(other):
            if isinstance(other, Version):
                result = self.version == other.version
            else:
                result = False
        return result

    def __lt__(self, other):
        """Comparing given version to be less than the other one."""
        result = False
        if isinstance(other, Version):
            result = self.version < other.version
        else:
            raise TypeError("Comparing type Version with incomaptible type %s" % type(other))
        return result


class VersionsCheck(object):
    """Evaluating versions of required tools."""

    LOGGER = Logger.get_logger(__name__)
    """Logger instance for this class."""

    BASH_VERSION = r'''bash --version|head -1'''
    """Find Bash version."""

    DOCKER_VERSION = r'''docker version|grep "Version:"|head -1'''
    """Find Docker version."""

    PACKER_VERSION = r'''packer -version'''
    """Find Packer version."""

    ANSIBLE_VERSION = r'''ansible --version'''
    """Find Ansible version."""

    def __init__(self):
        """Do nothing the moment."""
        pass

    def process(self, document):
        """Logging versions of required tools."""
        content = json.dumps(document)

        versions = {}
        versions.update({'Spline': Version(VERSION)})
        versions.update(self.get_version("Bash", self.BASH_VERSION))

        if content.find('"docker(container)":') >= 0 or content.find('"docker(image)":') >= 0:
            versions.update(VersionsCheck.get_version("Docker", self.DOCKER_VERSION))
        if content.find('"packer":') >= 0:
            versions.update(VersionsCheck.get_version("Packer", self.PACKER_VERSION))
        if content.find('"ansible(simple)":') >= 0:
            versions.update(VersionsCheck.get_version('Ansible', self.ANSIBLE_VERSION))

        return versions

    @staticmethod
    def get_version(tool_name, tool_command):
        """
        Get name and version of a tool defined by given command.

        Args:
            tool_name (str): name of the tool.
            tool_command (str): Bash one line command to get the version of the tool.

        Returns:
            dict: tool name and version or empty when no line has been found
        """
        result = {}
        for line in Bash(ShellConfig(script=tool_command, internal=True)).process():
            if line.find("command not found") >= 0:
                VersionsCheck.LOGGER.error("Required tool '%s' not found (stopping pipeline)!", tool_name)
                sys.exit(1)
            else:
                version = list(re.findall(r'(\d+(\.\d+)+)+', line))[0][0]
                result = {tool_name: Version(str(version))}
            break
        return result


class VersionsReport(object):
    """Logging versions."""

    LOGGER = Logger.get_logger(__name__)
    """Logger instance for this class."""

    def process(self, versions):
        """Logging version sorted ascending by tool name."""
        for tool_name in sorted(versions.keys()):
            version = versions[tool_name]
            self._log("Using tool '%s', %s" % (tool_name, version))

    def _log(self, message):
        """Logging a message."""
        self.LOGGER.info(message)
