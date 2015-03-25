"""Tests for pycounter.sushi"""

from __future__ import absolute_import

import unittest
import os
from httmock import urlmatch, HTTMock
import datetime

from pycounter import sushi


@urlmatch(netloc=r'(.*\.)?example\.com$')
def sushi_mock(url, request):
    path = os.path.join(os.path.dirname(__file__),
                        'data', 'sushi_simple.xml')
    with open(path, 'rb') as datafile:
        return datafile.read().decode('utf-8')


class TestHelpers(unittest.TestCase):
    def test_ns(self):
        self.assertEqual(
            sushi._ns("sushi", "name"),
            "{http://www.niso.org/schemas/sushi}name")


class TestConvertRawSimple(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'sushi_simple.xml')
        with open(path, 'rb') as datafile:
            self.report = sushi._raw_to_full(datafile.read())

    def test_report(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 4)


class TestSushiRequest(unittest.TestCase):
    def setUp(self):
        with HTTMock(sushi_mock):
            self.report = sushi.get_report('http://www.example.com/SushiService',
                                           datetime.date(2015, 1, 1),
                                           datetime.date(2015, 1, 31)
                                           )

    def test_report(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 4)
