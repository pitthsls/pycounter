"""Test COUNTER DB1 database report"""

from __future__ import absolute_import

import os
import unittest

import pycounter.report


class ParseCounter4Example(unittest.TestCase):
    """Tests for parsing C4 PR1"""

    def setUp(self):
        self.report = pycounter.report.parse(
            os.path.join(os.path.dirname(__file__), "data/PR1.tsv")
        )

    def test_reportname(self):
        self.assertEqual(self.report.report_type, u"PR1")

    def test_stats(self):
        publication = self.report.pubs[0]
        self.assertEqual(
            [x[2] for x in publication], [91, 41, 13, 21, 44, 8, 0, 0, 36, 36, 7, 2]
        )

    def test_row_metric(self):
        # test metric of the first row
        jan_data = next(iter(self.report.pubs[0]))
        self.assertEqual(jan_data[1], "Regular Searches")
        # test metric of the second row
        jan_data = next(iter(self.report.pubs[1]))
        self.assertEqual(jan_data[1], "Searches-federated and automated")


def test_output(tmp_path):
    report = pycounter.report.parse(
        os.path.join(os.path.dirname(__file__), "data/PR1.tsv")
    )
    report.write_tsv(str(tmp_path / "outputfile.tsv"))
    with open(str(tmp_path / "outputfile.tsv"), "rb") as new_file:
        new_content = new_file.read()
    assert b"Searches-federated" in new_content
