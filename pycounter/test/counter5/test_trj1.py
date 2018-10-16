"""Tests of title report for journals."""


def test_version(trj1_report):
    assert trj1_report.report_version == 5
