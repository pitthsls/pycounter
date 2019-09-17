"""Test parsing of COUNTER 4 JR2 report (turnaways)"""

import datetime


def test_metric(jr2_report):
    assert jr2_report.metric is None  # Multiple metrics per report


def test_type(jr2_report):
    assert jr2_report.report_type == u"JR2"


def test_data(jr2_report):
    i = iter(jr2_report)
    row = next(i)
    item = next(iter(row))
    assert item == (
        datetime.date(2011, 1, 1),
        u"Access denied: concurrent/simultaneous user license limit exceeded",
        3,
    )
