"""Test parsing of COUNTER BR1 book report."""


def test_reportname(br1_report):
    assert br1_report.report_type == "BR1"
    assert br1_report.report_version == 4


def test_metric(br1_report):
    assert br1_report.metric == "Book Title Requests"


def test_isbn(br1_report):
    publication = br1_report.pubs[0]
    assert publication.isbn == "9787490833809"
