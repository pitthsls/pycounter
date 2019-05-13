"""Test output of BR1 report"""

from __future__ import absolute_import

import logging
import os
import tempfile
import unittest

from pycounter import report


class TestWritingBR1(unittest.TestCase):
    """Test write of BR1 to filesystem"""

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), "data/C4BR1.tsv")
        self.rep = report.parse(self.filename)

        self.output_content = self.rep.as_generic()

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
