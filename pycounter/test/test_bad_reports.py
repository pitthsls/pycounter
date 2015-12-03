from __future__ import absolute_import

import unittest

from pycounter import report
import pycounter.exceptions


class ParseBad(unittest.TestCase):
    def test_bogus_report_type(self):
        data = [[u"Bogus Report OR7 (R4)"]]
        self.assertRaises(pycounter.exceptions.UnknownReportTypeError,
                          report.parse_generic,
                          iter(data)
                          )
