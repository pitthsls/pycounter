"""Test output of database reports"""

from __future__ import absolute_import

import os
import unittest

from pycounter import csvhelper
from pycounter import report


class TestOutputDB1(unittest.TestCase):
    """Test output of DB1"""
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data/C4DB1.tsv')
        rep = report.parse(filename)
        with csvhelper.UnicodeReader(filename,
                                     delimiter='\t') as report_reader:
            self.file_content = list(report_reader)

        self.output_content = rep.as_generic()

    def test_header_content(self):
        self.assertEqual(self.file_content[0:7], self.output_content[0:7])

    def test_table_header(self):
        self.assertEqual(self.file_content[7], self.output_content[7])

    def test_totals(self):
        self.assertEqual(self.file_content, self.output_content)

    def test_data(self):
        for index, line in enumerate(self.file_content[9:], 9):
            self.assertEqual(line, self.output_content[index])


class TestOutputDB2(unittest.TestCase):
    """Test output of DB2"""
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data/C4DB2.tsv')
        rep = report.parse(filename)
        with csvhelper.UnicodeReader(filename,
                                     delimiter='\t') as report_reader:
            self.file_content = list(report_reader)

        self.output_content = rep.as_generic()

    def test_header_content(self):
        self.assertEqual(self.file_content[0:7], self.output_content[0:7])

    def test_table_header(self):
        self.assertEqual(self.file_content[7], self.output_content[7])

    def test_totals(self):
        self.assertEqual(self.file_content, self.output_content)

    def test_data(self):
        for index, line in enumerate(self.file_content[9:], 9):
            self.assertEqual(line, self.output_content[index])
