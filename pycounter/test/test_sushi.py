"""Tests for pycounter.sushi"""

from __future__ import absolute_import

import unittest
import os
from httmock import urlmatch, HTTMock
import datetime

from pycounter import sushi
import pycounter.exceptions


@urlmatch(netloc=r'(.*\.)?example\.com$')
def sushi_mock(url, request):
    path = os.path.join(os.path.dirname(__file__),
                        'data', 'sushi_simple.xml')
    with open(path, 'rb') as datafile:
        return datafile.read().decode('utf-8')


@urlmatch(netloc=r'(.*\.)?example\.com$')
def bogus_mock(url, request):
    return "Bogus response with no XML"


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

    def test_title(self):
        publication = next(iter(self.report))
        self.assertEqual(publication.title, u'Journal of fake data')


class TestMissingMonth(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'sushi_missing_jan.xml')
        with open(path, 'rb') as datafile:
            self.report = sushi._raw_to_full(datafile.read())
        self.publication = next(iter(self.report))

    def test_february(self):
        first_month_data = next(iter(self.publication))
        self.assertEqual(first_month_data[0],
                         datetime.date(2013, 2, 1))

    def test_title(self):
        self.assertEqual(self.publication.title, u'Journal of fake data')


class TestSushiRequest(unittest.TestCase):
    def setUp(self):
        with HTTMock(sushi_mock):
            self.report = sushi.get_report('http://www.example.com/Sushi',
                                           datetime.date(2015, 1, 1),
                                           datetime.date(2015, 1, 31)
                                           )

    def test_report(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 4)


class TestBogusXML(unittest.TestCase):
    def test_request(self):
        with HTTMock(bogus_mock):
            self.assertRaises(pycounter.exceptions.SushiException,
                              sushi.get_report,
                              'http://www.example.com/bogus',
                              datetime.date(2015, 1, 1),
                              datetime.date(2015, 1, 31)
                              )
