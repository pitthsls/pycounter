"""Test output of BR1 report"""

from __future__ import absolute_import

import logging
import os
import tempfile
import unittest

from pycounter import csvhelper
from pycounter import report


class TestOutputBR1(unittest.TestCase):
    """Test output of BR1"""
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data/C4BR1.tsv')
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


class TestWritingBR1(unittest.TestCase):
    """Test write of BR1 to filesystem"""
    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__),
                                     'data/C4BR1.tsv')
        self.rep = report.parse(self.filename)

        self.output_content = self.rep.as_generic()

    def test_output_tsv(self):
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.close()
        tmp_loc = tf.name
        self.rep.write_tsv(tmp_loc)
        logging.debug("Temp file at %s", tmp_loc)

        with open(self.filename, 'rb') as orig_file:
            orig_content = orig_file.read()

        with open(tmp_loc, 'rb') as new_file:
            new_content = new_file.read()

        self.assertEqual(orig_content, new_content)


class TestOutputBR2(unittest.TestCase):
    """Test output of BR2"""
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data/C4BR2.tsv')
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
