"""Test COUNTER JR1 journal report (TSV)"""

from __future__ import absolute_import

import datetime
import os
import unittest

from pycounter import report


class ParseExample(unittest.TestCase):
    """Test tab-separated JR1"""

    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/simpleJR1.tsv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 4)

    def test_year(self):
        self.assertEqual(self.report.year, 2013)

    def test_platform(self):
        for publication in self.report:
            self.assertEqual(publication.publisher, u"aap")
            self.assertEqual(publication.platform,
                             u"Journal of Periodontology Online")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual([x[2] for x in publication],
                         [1, 4, 9, 4, 2, 0, 1, 4, 5, 2])
        publication = self.report.pubs[1]
        self.assertEqual([x[2] for x in publication],
                         [3, 0, 0, 0, 1, 0, 14, 1, 3, 5])

    def test_customer(self):
        self.assertEqual(self.report.customer, u"University of Maximegalon")

    def test_date_run(self):
        self.assertEqual(self.report.date_run, datetime.date(2013, 11, 22))

    def test_period(self):
        self.assertEqual(self.report.period,
                         (datetime.date(2013, 1, 1),
                          datetime.date(2013, 10, 31)))

    def test_dates(self):
        publication = self.report.pubs[0]
        self.assertEqual([x[0] for x in publication],
                         [datetime.date(2013, 1, 1),
                          datetime.date(2013, 2, 1),
                          datetime.date(2013, 3, 1),
                          datetime.date(2013, 4, 1),
                          datetime.date(2013, 5, 1),
                          datetime.date(2013, 6, 1),
                          datetime.date(2013, 7, 1),
                          datetime.date(2013, 8, 1),
                          datetime.date(2013, 9, 1),
                          datetime.date(2013, 10, 1),
                          ]
                         )

    def test_html(self):
        expected = [0, 15, 33, 0]
        actual = [pub.html_total for pub in self.report.pubs]

        self.assertEqual(actual, expected)

    def test_pdf(self):
        expected = [32, 12, 855, 40]
        actual = [pub.pdf_total for pub in self.report.pubs]

        self.assertEqual(actual, expected)
