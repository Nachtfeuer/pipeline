"""Generating report in different formats."""
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
import os
from datetime import datetime

from spline.version import VERSION
from spline.tools.filters import render
from spline.tools.logger import Logger


def generate_html(store):
    """
    Generating HTML report.

    Args:
        store (Store): report data.

    Returns:
        str: rendered HTML template.
    """
    spline = {
        'version': VERSION,
        'url': 'https://github.com/Nachtfeuer/pipeline',
        'generated': datetime.now().strftime("%A, %d. %B %Y - %I:%M:%S %p")
    }

    html_template_file = os.path.join(os.path.dirname(__file__), 'templates/report.html.j2')
    with open(html_template_file) as handle:
        html_template = handle.read()
        return render(html_template, spline=spline, store=store)


def generate(store, report_format, path):
    """
    Generate file in defined format representing the report of pipeline(s).

    Args:
        store (Store): report data.
        report_format (str): currently "html" is supported only.
        path (str): path where to write the report to. Missing sub folders will be created.
    """
    success = False
    if report_format in ['html']:
        rendered_content = {
            'html': generate_html
        }[report_format](store)

        if not os.path.isdir(path):
            os.makedirs(path)

        if rendered_content is not None:
            # writing report file
            with open(os.path.join(path, 'pipeline.' + report_format), 'w') as handle:
                handle.write(rendered_content)
            success = True
    else:
        Logger.get_logger(__name__).error("Unknown report format %s", report_format)
    return success
