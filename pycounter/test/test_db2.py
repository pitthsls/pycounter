"""Test COUNTER DB2 database report"""

from __future__ import absolute_import

import os
import unittest

import pycounter.report


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 DB2"""

    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__), "data/C4DB2.tsv")
        )

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u"DB2")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual([x[2] for x in publication], [0, 5, 0, 0, 0, 0])

    def test_row_metric(self):
        publication = self.report.pubs[0]
        jan_data = next(iter(publication))
        self.assertEqual(
            jan_data[1],
            "Access denied: concurrent/" "simultaneous user license " "limit exceeded",
        )
