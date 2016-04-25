"""Test COUNTER DB2 database report"""

from __future__ import absolute_import

import datetime
import os
import unittest

from pycounter.constants import METRICS
import pycounter.report


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 DB2"""
    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__),
                         'data/C4DB2.tsv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'DB2')
        self.assertEqual(self.report.report_version, 4)

    def test_year(self):
        self.assertEqual(self.report.year, 2012)

    def test_platform(self):
        for publication in self.report:
            self.assertEqual(publication.publisher, u"Megadodo Publications")
            self.assertEqual(publication.platform, u"HHGTTG Online")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual(
            [x[2] for x in publication],
            [0, 5, 0, 0, 0, 0])

    def test_report_metric(self):
        for metric in self.report.metric:
            self.assertTrue(metric in METRICS[self.report.report_type])

    def test_row_metric(self):
        publication = self.report.pubs[0]
        jan_data = next(iter(publication))
        self.assertEqual(jan_data[1], "Access denied: concurrent/"
                                      "simultaneous user license "
                                      "limit exceeded")

    def test_customer(self):
        self.assertEqual(self.report.customer,
                         u"University of Maximegalon")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2012, 7, 9))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2012, 1, 1),
                          datetime.date(2012, 6, 30)))
