"""Testing of module filter."""
# pylint: disable=no-self-use, invalid-name
import unittest
from mock import patch, MagicMock, call
from hamcrest import assert_that, equal_to, greater_than

from spline.tools.report.generator import generate, generate_html
from spline.tools.report.collector import Store


class TestReportGenerator(unittest.TestCase):
    """Testing of report generator."""

    def test_unknown_format(self):
        """Testing unknown format."""
        assert_that(generate(None, 'foobar', '/tmp'), equal_to(False))

    def test_write(self):
        """Testing normal write without really writing to a file."""
        with patch("os.makedirs") as mocked_make_dirs:
            with patch("spline.tools.report.generator.generate_html") as mocked_generate_html:
                mocked_generate_html.return_value = '<html></html>'
                stream = MagicMock()
                with patch("spline.tools.report.generator.open") as mocked_open:
                    mocked_open.return_value = stream
                    assert_that(generate(Store(), 'html', '/tmp/html'), equal_to(True))
                    mocked_make_dirs.assert_called_once_with('/tmp/html')
                assert_that(stream.mock_calls[1],
                            equal_to(call.__enter__().write('<html></html>')))

    def test_generate_html(self):
        """Testing html generation."""
        html = generate_html(Store())
        assert_that(html.find('Spline - Pipeline Visualization'), greater_than(0))

    def test_failed_rendering(self):
        """Testing failed rendering."""
        with patch("spline.tools.report.generator.render") as mocked_render:
            mocked_render.return_value = None
            assert_that(generate(Store(), 'html', '/tmp'), equal_to(False))
