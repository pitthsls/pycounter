from __future__ import absolute_import
from pycounter import report
import unittest
import os
import datetime


class ParseExample(unittest.TestCase):
    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/simpleJR1.csv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 3)

    def test_year(self):
        self.assertEqual(self.report.year, 2011)

    def test_platform(self):
        for publication in self.report:
            self.assertEqual(publication.publisher,
                             u"Maximegalon University Press")
            self.assertEqual(publication.platform, u"MJO")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual([x[2] for x in publication],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        publication = self.report.pubs[1]
        self.assertEqual([x[2] for x in publication],
                         [2, 1, 0, 0, 0, 5, 1, 1, 0, 5, 1, 0])

    def test_customer(self):
        self.assertEqual(self.report.customer, u"University of Maximegalon")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2012, 2, 21))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2011, 1, 1),
                          datetime.date(2011, 12, 31)))


class ParseCounter4(unittest.TestCase):
    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/C4JR1.csv'))

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


class ParseMultiyear(unittest.TestCase):
    """Multi-year COUNTER report
    """

    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/C4JR1my.csv'))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2011, 10, 1),
                          datetime.date(2012, 2, 29)))

    def test_monthdata_exception(self):
        self.assertRaises(AttributeError, getattr,
                          self.report.pubs[0], 'monthdata')

    def test_data(self):
        self.assertEqual(len(list(self.report.pubs[0])), 5)
        usage = [x[2] for x in self.report.pubs[0]]
        self.assertEqual(usage, [0, 0, 0, 0, 0])

    def test_month_data(self):
        expected = [datetime.date(2011, 10, 1),
                    datetime.date(2011, 11, 1),
                    datetime.date(2011, 12, 1),
                    datetime.date(2012, 1, 1),
                    datetime.date(2012, 2, 1),
                    ]

        months = [x[0] for x in self.report.pubs[0]]

        self.assertEqual(months, expected)


class ParseBigMultiyear(unittest.TestCase):
    """Multi-year report with more than 12 months of data
    """

    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/C4JR1big.csv'))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2011, 1, 1),
                          datetime.date(2012, 12, 31)))

    def test_monthdata_exception(self):
        self.assertRaises(AttributeError, getattr,
                          self.report.pubs[0], 'monthdata')

    def test_data(self):
        usage = [x[2] for x in self.report.pubs[0]]
        self.assertEqual(usage,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                          ])


class ParseGOA(unittest.TestCase):
    """Gold Open Access Report
    """

    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/C4JR1GOA.csv'))

    def test_metric(self):
        self.assertEqual(self.report.metric,
                         u"Gold Open Access Article Requests")

    def test_customer(self):
        self.assertEqual(self.report.customer, u"University of Maximegalon")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2012, 2, 21))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2011, 1, 1),
                          datetime.date(2011, 12, 31)))