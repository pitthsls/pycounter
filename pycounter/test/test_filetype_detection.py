"""Test detecting file types correctly"""

from __future__ import absolute_import

import datetime
import os
import unittest

from pycounter import report
from pycounter.test import common_data


class ParseCSV(unittest.TestCase):
    """Test CSV"""
    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/csvC4JR1'))

    def test_counter4_csv_data(self):

        publication = self.report.pubs[0]
        self.assertEqual([x[2] for x in publication],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        publication = self.report.pubs[1]
        self.assertEqual([x[2] for x in publication],
                         [2, 1, 0, 0, 0, 5, 1, 1, 0, 5, 1, 0])

    def test_metric(self):
        self.assertEqual(self.report.metric, u"FT Article Requests")

    def test_customer(self):
        self.assertEqual(self.report.customer, u"University of Maximegalon")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2012, 2, 21))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2011, 1, 1),
                          datetime.date(2011, 12, 31)))


class ParseTSV(common_data.TSVJR1):
    """Test TSV"""
    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/tsvC4JR1'))


class ParseXLSX(unittest.TestCase):
    """Test XLSX"""
    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                   'data/xlsxJR1'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 4)

    def test_year(self):
        self.assertEqual(self.report.year, 2013)

    def test_platform(self):
        for publication in self.report:
            self.assertEqual(publication.publisher,
                             u"American Medical Association")
            self.assertEqual(publication.platform, u"Silverchair")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual([x[2] for x in publication],
                         [4, 14, 13, 30, 19, 7, 31, 6, 16, 12, 8, 12])
        publication = self.report.pubs[1]
        self.assertEqual(
            [x[2] for x in publication],
            [5414, 5459, 4936, 5172, 4064, 3904, 4054,
             4090, 5010, 6680, 5961, 3742])
