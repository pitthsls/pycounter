"""Test parsing of COUNTER BR1 book report."""

import os
import unittest

import pycounter.report


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 BR1"""

    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__), "data/C4BR1.tsv")
        )

    def test_reportname(self):
        self.assertEqual(self.report.report_type, "BR1")
        self.assertEqual(self.report.report_version, 4)

    def test_metric(self):
        self.assertEqual(self.report.metric, "Book Title Requests")

    def test_isbn(self):
        publication = self.report.pubs[0]
        self.assertEqual(publication.isbn, "9787490833809")
