"""Testing of module tools.version."""
# pylint: disable=no-self-use, invalid-name
import unittest
from mock import patch, call
from hamcrest import assert_that, equal_to, less_than, is_not, calling, raises, has_key
from spline.tools.version import VersionsCheck, VersionsReport, Version


class TestToolsVersion(unittest.TestCase):
    """Testing of module tools.version."""

    def test_bash_version__only(self):
        """Testing with Bash only."""
        versions = VersionsCheck().process({})
        report = VersionsReport()
        with patch.object(report, '_log') as mocked_log:
            report.process(versions)
            assert_that(mocked_log.mock_calls, equal_to([
                call("Using tool 'Bash', %s" % versions['Bash']),
                call("Using tool 'Spline', %s" % versions['Spline'])
            ]))

    def test_bash_and_docker_container(self):
        """Testing with Bash and Docker container only."""
        versions = VersionsCheck().process({'docker(container)': ''})
        report = VersionsReport()
        with patch.object(report, '_log') as mocked_log:
            report.process(versions)
            assert_that(mocked_log.mock_calls, equal_to([
                call("Using tool 'Bash', %s" % versions['Bash']),
                call("Using tool 'Docker', %s" % versions['Docker']),
                call("Using tool 'Spline', %s" % versions['Spline'])
            ]))

    def test_bash_and_docker_image(self):
        """Testing with Bash and Docker image only."""
        versions = VersionsCheck().process({'docker(image)': ''})
        report = VersionsReport()
        with patch.object(report, '_log') as mocked_log:
            report.process(versions)
            assert_that(mocked_log.mock_calls, equal_to([
                call("Using tool 'Bash', %s" % versions['Bash']),
                call("Using tool 'Docker', %s" % versions['Docker']),
                call("Using tool 'Spline', %s" % versions['Spline'])

            ]))

    def test_bash_and_packer(self):
        """Testing with Bash and Packer image only."""
        versions = VersionsCheck().process({'packer': ''})
        report = VersionsReport()
        with patch.object(report, '_log') as mocked_log:
            report.process(versions)
            assert_that(mocked_log.mock_calls, equal_to([
                call("Using tool 'Bash', %s" % versions['Bash']),
                call("Using tool 'Packer', %s" % versions['Packer']),
                call("Using tool 'Spline', %s" % versions['Spline'])
            ]))

    def test_bash_and_ansible(self):
        """Testing with Bash and Ansible only."""
        with patch("spline.tools.version.VersionsCheck.get_version") as mocked_get_version:
            mocked_versions = {'Bash': Version("2.0"), 'Ansible': Version("1.0")}
            mocked_get_version.side_effect = lambda key, _: {key: mocked_versions[key]}

            versions = VersionsCheck().process({'ansible(simple)': ''})
            report = VersionsReport()

            with patch.object(report, '_log') as mocked_log:
                report.process(versions)
                assert_that(mocked_log.mock_calls, equal_to([
                    call("Using tool 'Ansible', %s" % versions['Ansible']),
                    call("Using tool 'Bash', %s" % versions['Bash']),
                    call("Using tool 'Spline', %s" % versions['Spline'])
                ]))

    def test_get_version(self):
        """Testing get_version function."""
        result = VersionsCheck.get_version('Bash', VersionsCheck.BASH_VERSION)
        assert_that(result, has_key('Bash'))
        with patch('sys.exit') as mocked_exit:
            VersionsCheck.get_version('Bash', VersionsCheck.BASH_VERSION.replace("bash", "xbashx"))
            assert_that(mocked_exit.mock_calls, equal_to([call(1)]))

    def test_version_init(self):
        """Testing version initialization."""
        version = Version('1.2.3')
        assert_that(str(version), equal_to('Version(1.2.3)'))

    def test_version_comparison(self):
        """Testing comparison of versions."""
        version = Version("1.2")
        assert_that(version, equal_to(version))
        assert_that(Version("1.2"), equal_to(Version("1.2")))
        assert_that(Version("1.2"), less_than(Version("1.3")))
        assert_that(Version("1.2"), less_than(Version("1.2.1")))
        assert_that(Version("1.3"), is_not(less_than(Version("1.2"))))
        assert_that(Version("1.3") == 1.3, equal_to(False))
        assert_that(calling(Version("1.3").__lt__).with_args(1.3),
                    raises(TypeError, "Comparing type Version with incomaptible type"))
