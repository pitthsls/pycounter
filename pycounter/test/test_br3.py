"""Test parsing of COUNTER 4 BR3 report (turnaways)"""

import datetime


def test_metric(br3_report):
    assert br3_report.metric is None  # Multiple metrics per report


def test_type(br3_report):
    assert br3_report.report_type == u"BR3"


def test_data(br3_report):
    i = iter(br3_report)
    row = next(i)
    item = next(iter(row))
    assert item == (
        datetime.date(2012, 1, 1),
        u"Access denied: concurrent/simultaneous user license limit exceeded",
        4,
    )
