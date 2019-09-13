# coding: utf-8
"""Test parsing of COUNTER BR2 book report."""

from __future__ import absolute_import

import os
import unittest

import pycounter.report


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 BR2"""

    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__), "data/C4BR2.tsv")
        )

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u"BR2")
        self.assertEqual(self.report.report_version, 4)

    def test_metric(self):
        self.assertEqual(self.report.metric, u"Book Section Requests")
