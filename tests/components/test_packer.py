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
        assert_that(os.path.isfile(filename), equal_to(True), "Missing %s" % filename)
        os.remove(filename)

        assert_that(output[-4], contains_string(
            "Build 'docker' finished."))
        assert_that(output[-2], contains_string(
            '==> Builds finished. The artifacts of successful builds are:'))
        assert_that(output[-1], contains_string(
            "--> docker: Exported Docker file: %s" % filename))

    def test_creator_dry_run(self):
        """Testing dry run for Packer Docker image."""
        filename = os.path.join(os.path.dirname(__file__), 'image.tar')
        script = '''{"builders": [{
                "type": "docker",
                "image": "{{ model.image }}:{{ env.tag }}",
                "export_path": "{{ variables.filename }}"}]}'''
        config = ShellConfig(script=script, title='test image creation',
                             model={'image': 'centos'}, env={'tag': '7'},
                             variables={'filename': filename}, dry_run=True)
        image = Packer.creator({}, config)
        output = [line for line in image.process() if line.find('export_path') >= 0]
        assert_that(len(output), equal_to(1))
