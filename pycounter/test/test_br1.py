"""Test parsing of COUNTER BR1 book report."""

from __future__ import absolute_import

import datetime
import os
import unittest

import pycounter.report


class ParseExample(unittest.TestCase):
    """Tests for parsing C3 BR1"""
    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__),
                         'data/simpleBR1.csv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'BR1')
        self.assertEqual(self.report.report_version, 1)

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
            [0, 25, 0, 0, 0, 0])

    def test_customer(self):
        self.assertEqual(self.report.customer,
                         u"University of Maximegalon")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2012, 7, 9))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2012, 1, 1),
                          datetime.date(2012, 6, 30)))


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 BR1"""
    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__),
                         'data/C4BR1.tsv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'BR1')
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
            [0, 25, 0, 0, 0, 0])

    def test_metric(self):
        self.assertEqual(self.report.metric, u"Book Title Requests")

    def test_customer(self):
        self.assertEqual(self.report.customer,
                         u"University of Maximegalon")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2012, 7, 9))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2012, 1, 1),
                          datetime.date(2012, 6, 30)))

    def test_isbn(self):
        publication = self.report.pubs[0]
        self.assertEqual(publication.isbn, u'9787490833809')
