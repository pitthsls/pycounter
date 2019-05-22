"""Tests for COUNTER 5 SUSHI support."""


def test_report_type(sushi5_report):
    assert sushi5_report.report_type == u"TR_J1"


def test_report_version(sushi5_report):
    assert sushi5_report.report_version == 5


def test_report_customer(sushi5_report):
    assert sushi5_report.institutional_identifier == u"exampleLibrary"


def test_data(sushi5_report):
    publication = next(iter(sushi5_report))
    data = [month[2] for month in publication]
    assert data[0] == 14


def test_metric(sushi5_report):
    publication = next(iter(sushi5_report))
    metrics = [month[1] for month in publication]
    assert metrics[0] == u"FT Item Requests"  # FIXME: COUNTER4 compat kludge


def test_doi(sushi5_report):
    publication = next(iter(sushi5_report))
    assert publication.doi == "some.fake.doi"
