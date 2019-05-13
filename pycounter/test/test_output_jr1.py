"""Test output of JR1 report"""

from __future__ import absolute_import

import datetime
import logging
import os
import tempfile
import unittest

from pycounter import csvhelper
from pycounter import report


class TestWritingJR1(unittest.TestCase):
    """Test write of JR1 to filesystem"""

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), "data/simpleJR1.tsv")
        self.rep = report.parse(self.filename)

    def test_output_tsv(self):
        output_file = tempfile.NamedTemporaryFile(delete=False)
        output_file.close()
        tmp_loc = output_file.name
        self.rep.write_tsv(tmp_loc)
        logging.debug("Temp file at %s", tmp_loc)

        with open(self.filename, "rb") as orig_file:
            orig_content = orig_file.read()

        with open(tmp_loc, "rb") as new_file:
            new_content = new_file.read()

        self.assertEqual(orig_content, new_content)


class TestOrderingOutput(unittest.TestCase):
    """Test that titles are in alphabetical order when output"""

    def setUp(self):
        self.report = report.CounterReport(
            report_type="JR1",
            report_version=4,
            customer=u"Foo",
            institutional_identifier=u"Bar",
            period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
        )
        self.report.pubs.append(
            report.CounterJournal(
                period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
                month_data=[(datetime.date(2016, 1, 1), 260)],
                title=u"Fake Journal",
                publisher=u"No one",
                platform=u"Your imagination",
            )
        )
        self.report.pubs.append(
            report.CounterJournal(
                period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
                month_data=[(datetime.date(2016, 1, 1), 62)],
                title=u"Another Fake Journal",
                publisher=u"No one",
                platform=u"Your imagination",
            )
        )
        self.output_content = self.report.as_generic()

    def test_ordering(self):
        self.assertEqual(self.output_content[9][0], u"Another Fake Journal")
        self.assertEqual(self.output_content[10][0], u"Fake Journal")
