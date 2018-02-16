"""Testing of InMemoryFiles class."""
# pylint: disable=no-self-use, invalid-name
import os
import unittest
from mock import patch, call
from hamcrest import assert_that, equal_to, greater_than, has_item

from spline.tools.memfiles import InMemoryFiles


class TestInMemoryFiles(unittest.TestCase):
    """Testing of class InMemoryFiles."""

    def test_add_path(self):
        """Testing add_path method."""
        memfiles = InMemoryFiles()
        memfiles.add_path(os.path.dirname(__file__))
        assert_that(len(memfiles.files), greater_than(0))
        assert_that(memfiles.files, has_item("test_memfiles.py"))

    def test_json(self):
        """Testing methods to_json and from_json."""
        memfiles1 = InMemoryFiles()
        memfiles1.add_path(os.path.dirname(__file__))

        memfiles2 = InMemoryFiles.from_json(memfiles1.to_json())
        assert_that(memfiles1.files, equal_to(memfiles2.files))

    def test_compression(self):
        """Testing methods to_compressed and from_compressed."""
        memfiles1 = InMemoryFiles()
        memfiles1.add_path(os.path.dirname(__file__))

        memfiles2 = InMemoryFiles.from_compressed(memfiles1.to_compressed())
        assert_that(memfiles1.files, equal_to(memfiles2.files))

    @patch('os.makedirs')
    def test_save(self, mocked_makedirs):
        """Testing methods save."""
        memfiles = InMemoryFiles()
        memfiles.add_path(os.path.dirname(__file__), lambda fp: fp.endswith("memfiles.py"))

        with patch('spline.tools.memfiles.open') as mocked_open:
            memfiles.save('/tmp/does-not-exist')
            assert_that(mocked_makedirs.mock_calls, equal_to([call('/tmp/does-not-exist')]))

            special = [str(entry) for entry in mocked_open.mock_calls]
            special = [entry for entry in special if entry.find("write") > 0]
            assert_that(len(special), equal_to(1))
            content = special[0]
            assert_that(content.find("THIS HERE") >= 0, equal_to(True))
