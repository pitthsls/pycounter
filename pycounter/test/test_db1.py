"""Test COUNTER DB1 database report"""

from __future__ import absolute_import

import os
import unittest

import pycounter.report


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 DB1"""

    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__), "data/C4DB1.tsv")
        )

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u"DB1")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual([x[2] for x in publication], [0, 20, 0, 0, 5, 0])

    def test_row_metric(self):
        publication = self.report.pubs[0]
        jan_data = next(iter(publication))
        self.assertEqual(jan_data[1], "Regular Searches")


class ParseCounter4SplitExample(unittest.TestCase):
    """Tests for parsing C4 DB1"""

    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__), "data/C4DB1_split_year.tsv")
        )

    def test_year(self):
        self.assertEqual(self.report.year, 2012)
