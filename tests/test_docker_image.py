"""Testing of class Image."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
import logging
from hamcrest import assert_that, equal_to
from spline.components.docker import Image
from spline.components.bash import Bash
from spline.components.config import ShellConfig


@unittest.skipIf('INSIDE_DOCKER' in os.environ and os.environ['INSIDE_DOCKER'] == 'yes',
                 "Docker based tests cannot run inside Docker")
class TestDockerImage(unittest.TestCase):
    """Testing of class Image (docker)."""

    @staticmethod
    def cleanup(name, tag):
        """Removing Docker image."""
        shell = Bash(ShellConfig(script="docker rmi %s:%s" % (name, tag)))
        for line in shell.process():
            logging.info(line)
        assert_that(shell.success, equal_to(True))

    def test_createor_simple(self):
        """Testing image."""
        config = ShellConfig(script='''FROM {{ model.image }}:{{ env.tag }}\nRUN yum -y install ctags''',
                             title='test image creation', model={'image': 'centos'}, env={'tag': '7'})
        image = Image.creator({'name': 'test', 'tag': 'latest', 'unique': True}, config)
        output = [line for line in image.process() if line.find('Successfully tagged') >= 0]
        assert_that(len(output), equal_to(1))
        TestDockerImage.cleanup(name="test-%s" % os.getpid(), tag='latest')
