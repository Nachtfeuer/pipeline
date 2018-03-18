"""Testing of class Image."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from hamcrest import assert_that, equal_to, contains_string
from spline.components.packer import Packer
from spline.components.config import ShellConfig


@unittest.skipIf('INSIDE_DOCKER' in os.environ and os.environ['INSIDE_DOCKER'] == 'yes',
                 "Docker based tests cannot run inside Docker")
class TestPacker(unittest.TestCase):
    """Testing of class Packer."""

    def test_creator_simple(self):
        """Testing Packer using a Docker builder."""
        filename = os.path.join(os.path.dirname(__file__), 'image.tar')
        script = '''{"builders": [{"type": "docker", "image": "centos:7", "export_path": "%s"}]}''' % filename
        config = ShellConfig(script=script, model={}, env={})
        image = Packer.creator({}, config)
        output = list(image.process())
        assert_that(os.path.isfile(filename), equal_to(True))
        os.remove(filename)

        assert_that(output[-4], contains_string(
            "Build 'docker' finished."))
        assert_that(output[-2], contains_string(
            '==> Builds finished. The artifacts of successful builds are:'))
        assert_that(output[-1], contains_string(
            "--> docker: Exported Docker file: %s" % filename))
