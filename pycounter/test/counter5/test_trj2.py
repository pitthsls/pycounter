"""Test parsing of COUNTER 5 TRJ2 report (turnaways)"""

import datetime


def test_metric(trj2_report):
    assert trj2_report.metric is None  # Multiple metrics per report


def test_type(trj2_report):
    assert trj2_report.report_type == u"TR_J2"


def test_data(trj2_report):
    i = iter(trj2_report)
    row = next(i)
    item = next(iter(row))
    assert item == (datetime.date(2017, 1, 1), u"Limit_Exceeded", 3)
