"""Test parsing of COUNTER BR1 book report."""

from __future__ import absolute_import

import os
import unittest

import pycounter.report


class ParseExample(unittest.TestCase):
    """Tests for parsing C3 BR1"""

    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__), "data/simpleBR1.csv")
        )

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u"BR1")


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 BR1"""

    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__), "data/C4BR1.tsv")
        )

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u"BR1")
        self.assertEqual(self.report.report_version, 4)

    def test_metric(self):
        self.assertEqual(self.report.metric, u"Book Title Requests")

    def test_isbn(self):
        publication = self.report.pubs[0]
        self.assertEqual(publication.isbn, u"9787490833809")
