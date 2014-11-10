from __future__ import absolute_import
from pycounter import pycounter
import unittest
import os

class ParseExample(unittest.TestCase):
    def setUp(self):
        self.report = pycounter.parse(os.path.join(os.path.dirname(__file__),
                                                             'data/simpleJR1.tsv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 4)

    def test_year(self):
        self.assertEqual(self.report.year, 2013)

    def test_platform(self):
        for publication in self.report:
            self.assertEqual(publication.publisher, u"aap")
            self.assertEqual(publication.platform, u"Journal of Periodontology Online")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual(publication.monthdata, [1, 4, 9, 4, 2, 0, 1, 4, 5, 2, None, None])
        publication = self.report.pubs[1]
        self.assertEqual(publication.monthdata, [3, 0, 0, 0, 1, 0, 14, 1, 3, 5, None, None])
