"""Test COUNTER JR1 journal report (Excel)"""

from __future__ import absolute_import

import os
import unittest

from pycounter import report


class ParseExample(unittest.TestCase):
    """Test XLSX JR 1"""

    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/JR1.xlsx'))

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


class ParseBadExample(unittest.TestCase):
    """Test XLSX JR 1 with Excel-isms instead of COUNTER strings"""

    def setUp(self):
        self.report = report.parse(os.path.join(os.path.dirname(__file__),
                                                'data/JR1_bad.xlsx'))

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
