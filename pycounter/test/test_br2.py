# coding: utf-8
"""Test parsing of COUNTER BR2 book report."""

from __future__ import absolute_import

import os
import unittest
import warnings

import pycounter.report


class ParseExample(unittest.TestCase):
    """Tests for parsing C3 BR2"""
    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__),
                         'data/simpleBR2.csv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'BR2')
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


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 BR2"""
    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__),
                         'data/C4BR2.tsv'))

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u'BR2')
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
        self.assertEqual(self.report.metric, u"Book Section Requests")


class ParseLatin1(unittest.TestCase):
    """Tests for parsing BR2 in latin-1 encoding"""
    def setUp(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.report = pycounter.report.parse(
                os.path.join(os.path.dirname(__file__),
                             'data/simpleBR2_latin_1.csv'))

    def test_title(self):
        publication = self.report.pubs[1]
        self.assertEqual(publication.title, u'Öfake Book')
