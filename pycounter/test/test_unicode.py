"""regression test to ensure all output is of text type"""

from __future__ import absolute_import

import os
import unittest

from six import text_type

from pycounter import report


class UnicodeTests(unittest.TestCase):
    """All parsers should return text fields as unicode"""

    def test_xslx_unicode(self):
        rep = report.parse(os.path.join(os.path.dirname(__file__),
                                        'data/JR1.xlsx'))
        self.assertTrue(isinstance(rep.pubs[0].title, text_type))
        self.assertTrue(isinstance(rep.pubs[0].publisher, text_type))
        self.assertTrue(isinstance(rep.pubs[0].platform, text_type))

    def test_tsv_unicode(self):
        rep = report.parse(os.path.join(os.path.dirname(__file__),
                                        'data/simpleJR1.tsv'))

        self.assertTrue(isinstance(rep.pubs[0].title, text_type))
        self.assertTrue(isinstance(rep.pubs[0].publisher, text_type))
        self.assertTrue(isinstance(rep.pubs[0].platform, text_type))

    def test_csv_unicode(self):
        rep = report.parse(os.path.join(os.path.dirname(__file__),
                                        'data/simpleJR1.csv'))

        self.assertTrue(isinstance(rep.pubs[0].title, text_type))
        self.assertTrue(isinstance(rep.pubs[0].publisher, text_type))
        self.assertTrue(isinstance(rep.pubs[0].platform, text_type))
