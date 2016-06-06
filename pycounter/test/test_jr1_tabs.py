"""Test COUNTER JR1 journal report (TSV)"""

from __future__ import absolute_import

import os

from pycounter import report
from pycounter.test import common_data


class ParseExample(common_data.TSVJR1):
    """Test tab-separated JR1"""

    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/simpleJR1.tsv'))

    def test_html(self):
        expected = [0, 15, 33, 0]
        actual = [pub.html_total for pub in self.report.pubs]

        self.assertEqual(actual, expected)

    def test_pdf(self):
        expected = [32, 12, 855, 40]
        actual = [pub.pdf_total for pub in self.report.pubs]

        self.assertEqual(actual, expected)
