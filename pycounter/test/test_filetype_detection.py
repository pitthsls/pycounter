"""Test detecting file types correctly"""

from __future__ import absolute_import

import os

from pycounter import report
from pycounter.test import common_data


class ParseTSV(common_data.TSVJR1):
    """Test TSV"""

    def setUp(self):
        self.report = report.parse(
            os.path.join(os.path.dirname(__file__), "data/tsvC4JR1")
        )
