"""Test parsing of COUNTER BR2 book report."""


def test_reportname(br2_report):
    assert br2_report.report_type == "BR2"


def test_report_version(br2_report):
    assert br2_report.report_version == 4


def test_metric(br2_report):
    assert br2_report.metric == "Book Section Requests"
