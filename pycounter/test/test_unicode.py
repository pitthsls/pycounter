from __future__ import absolute_import
from pycounter import pycounter
import unittest
import os

class UnicodeTests(unittest.TestCase):
    """All parsers should return text fields as unicode"""

    def test_xslx_unicode(self):
        report = pycounter.parse(os.path.join(os.path.dirname(__file__),
                                              'data/JR1.xlsx'))
        self.assertTrue(isinstance(report.pubs[0].title, unicode))
        self.assertTrue(isinstance(report.pubs[0].publisher, unicode))
        self.assertTrue(isinstance(report.pubs[0].platform, unicode))

    def test_tsv_unicode(self):
        report = pycounter.parse(os.path.join(os.path.dirname(__file__),
                                              'data/simpleJR1.tsv'))

        self.assertTrue(isinstance(report.pubs[0].title, unicode))
        self.assertTrue(isinstance(report.pubs[0].publisher, unicode))
        self.assertTrue(isinstance(report.pubs[0].platform, unicode))

    def test_csv_unicode(self):
        report = pycounter.parse(os.path.join(os.path.dirname(__file__),
                                              'data/simpleJR1.csv'))

        self.assertTrue(isinstance(report.pubs[0].title, unicode))
        self.assertTrue(isinstance(report.pubs[0].publisher, unicode))
        self.assertTrue(isinstance(report.pubs[0].platform, unicode))
