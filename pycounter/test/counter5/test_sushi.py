"""Tests for COUNTER 5 SUSHI support."""


def test_report_type(sushi5_report):
    assert u"TR_J1" == sushi5_report.report_type


def test_report_version(sushi5_report):
    assert 5 == sushi5_report.report_version


def test_report_customer(sushi5_report):
    assert u"exampleLibrary" == sushi5_report.institutional_identifier


def test_data(sushi5_report):
    publication = next(iter(sushi5_report))
    data = [month[2] for month in publication]
    assert 14 == data[0]


def test_metric(sushi5_report):
    publication = next(iter(sushi5_report))
    metrics = [month[1] for month in publication]
    assert metrics[0] == u"FT Item Requests"  # FIXME: COUNTER4 compat kludge
