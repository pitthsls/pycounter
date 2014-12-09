from __future__ import absolute_import
from pycounter import report as pycounter
import unittest
import os
import datetime


class ParseExample(unittest.TestCase):
    def setUp(self):
        self.report = pycounter.parse(os.path.join(os.path.dirname(__file__),
                                                   'data/simpleJR1.csv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 3)

    def test_year(self):
        self.assertEqual(self.report.year, 2011)

    def test_platform(self):
        for publication in self.report:
            self.assertEqual(publication.publisher,
                             u"Cambridge University Press")
            self.assertEqual(publication.platform, u"CJO")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual(publication.monthdata,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        publication = self.report.pubs[1]
        self.assertEqual(publication.monthdata,
                         [2, 1, 0, 0, 0, 5, 1, 1, 0, 5, 1, 0])

    def test_customer(self):
        self.assertEqual(self.report.customer, u"Univ of Pittsburgh")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2012, 2, 21))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2011, 1, 1),
                          datetime.date(2011, 12, 31)))


class ParseCounter4(unittest.TestCase):
    def setUp(self):
        self.report = pycounter.parse(os.path.join(os.path.dirname(__file__),
                                                   'data/C4JR1.csv'))

    def test_counter4_csv_data(self):

        publication = self.report.pubs[0]
        self.assertEqual(publication.monthdata,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        publication = self.report.pubs[1]
        self.assertEqual(publication.monthdata,
                         [2, 1, 0, 0, 0, 5, 1, 1, 0, 5, 1, 0])

    def test_metric(self):
        self.assertEqual(self.report.metric, u"FT Article Requests")

    def test_customer(self):
        self.assertEqual(self.report.customer, u"Univ of Pittsburgh")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2012, 2, 21))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2011, 1, 1),
                          datetime.date(2011, 12, 31)))
