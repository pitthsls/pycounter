from __future__ import absolute_import
from pycounter import report
from pycounter import csvhelper
import unittest
import os


class TestOutputJR1(unittest.TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data/C4JR1.csv')
        rep = report.parse(filename)
        with csvhelper.UnicodeReader(filename,
                                     delimiter=',') as report_reader:
            self.file_content = list(report_reader)

        self.output_content = rep.as_generic()

    def test_header_content(self):
        self.assertEqual(self.file_content[0:7], self.output_content[0:7])

    def test_table_header(self):
        self.assertEqual(self.file_content[7], self.output_content[7])

    def test_totals(self):
        # FIXME: eventually, should check HTML & PDF too, but not supported yet
        self.assertEqual(self.file_content[8][0:8],
                         self.output_content[8][0:8])
        self.assertEqual(self.file_content[8][10:],
                         self.output_content[8][10:])

    def test_data(self):
        # FIXME: eventually, should check HTML & PDF too, but not supported yet
        for index, line in enumerate(self.file_content[9:], 9):
            self.assertEqual(line[0:8],
                             self.output_content[index][0:8])
            self.assertEqual(line[10:],
                             self.output_content[index][10:])
