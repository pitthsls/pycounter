import os

import pycounter.report


def test_parse():
    report = pycounter.report.parse(
        os.path.join(os.path.dirname(__file__), "data", "tr_j1.tsv")
    )
    assert report.report_version == 5
