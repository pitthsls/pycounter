"""Test parsing of deliberately bad data."""

from __future__ import absolute_import

import unittest

from pycounter import report
import pycounter.exceptions


class TestParseBad(unittest.TestCase):
    def test_bogus_report_type(self):
        data = [[u"Bogus Report 7 (R4)"]]
        self.assertRaises(pycounter.exceptions.UnknownReportTypeError,
                          report.parse_generic,
                          iter(data)
                          )

    def test_unsupported_report_type(self):
        """Test that we fail for report types that are real but unsupported"""
        # FIXME: eventually should be supported; remove this test when all are
        data = [[u"Platform Report 1 (R4)"]]
        self.assertRaises(pycounter.exceptions.UnknownReportTypeError,
                          report.parse_generic,
                          iter(data)
                          )


class TestBogusFiletype(unittest.TestCase):
    def test_bogus_file_type(self):
        self.assertRaises(pycounter.exceptions.PycounterException,
                          report.parse,
                          'no_such_file',
                          'qsx'
                          )
