"""Testing of module tools.version."""
# pylint: disable=no-self-use, invalid-name
import unittest
from mock import patch, call
from hamcrest import assert_that, equal_to
from spline.tools.version import VersionsReport


class TestToolVersion(unittest.TestCase):
    """Testing of module tools.version."""

    def test_bash_only(self):
        """Testing with Bash only."""
        report = VersionsReport()
        with patch.object(report, '_log_version') as mocked_log_version:
            report.process({})
            assert_that(mocked_log_version.mock_calls, equal_to([
                call('Bash', r'bash --version|head -1|grep -Po "\d+\.\d+\.\d+"')
            ]))

    def test_bash_and_docker_container(self):
        """Testing with Bash and Docker container only."""
        report = VersionsReport()
        with patch.object(report, '_log_version') as mocked_log_version:
            report.process({'docker(container)': ''})
            assert_that(mocked_log_version.mock_calls, equal_to([
                call('Bash', r'bash --version|head -1|grep -Po "\d+\.\d+\.\d+"'),
                call('Docker', r'docker version|grep "Version:"|head -1|grep -Po "\d+\.\d+\.\d+"')
            ]))

    def test_bash_and_docker_image(self):
        """Testing with Bash and Docker image only."""
        report = VersionsReport()
        with patch.object(report, '_log_version') as mocked_log_version:
            report.process({'docker(image)': ''})
            assert_that(mocked_log_version.mock_calls, equal_to([
                call('Bash', r'bash --version|head -1|grep -Po "\d+\.\d+\.\d+"'),
                call('Docker', r'docker version|grep "Version:"|head -1|grep -Po "\d+\.\d+\.\d+"')
            ]))

    def test_bash_and_packer(self):
        """Testing with Bash and Packer image only."""
        report = VersionsReport()
        with patch.object(report, '_log_version') as mocked_log_version:
            report.process({'packer': ''})
            assert_that(mocked_log_version.mock_calls, equal_to([
                call('Bash', r'bash --version|head -1|grep -Po "\d+\.\d+\.\d+"'),
                call('Packer', 'packer -version')
            ]))

    def test_bash_and_ansible(self):
        """Testing with Bash and Ansible only."""
        report = VersionsReport()
        with patch.object(report, '_log_version') as mocked_log_version:
            report.process({'ansible(simple)': ''})
            assert_that(mocked_log_version.mock_calls, equal_to([
                call('Bash', r'bash --version|head -1|grep -Po "\d+\.\d+\.\d+"'),
                call('Ansible', r'ansible --version|grep -Po "\d+\.\d+\.\d+\.\d+"')
            ]))
