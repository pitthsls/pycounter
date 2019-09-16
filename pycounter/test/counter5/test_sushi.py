"""Tests for COUNTER 5 SUSHI support."""

import io
import os

from httmock import all_requests, HTTMock
import pytest

import pycounter.exceptions
import pycounter.sushi5


def test_report_type(sushi5_report_trj1):
    assert sushi5_report_trj1.report_type == u"TR_J1"


def test_report_version(sushi5_report_trj1):
    assert sushi5_report_trj1.report_version == 5


def test_report_customer(sushi5_report_trj1):
    assert sushi5_report_trj1.institutional_identifier == u"exampleLibrary"


def test_data(sushi5_report_trj1):
    publication = next(iter(sushi5_report_trj1))
    data = [month[2] for month in publication]
    assert data[0] == 14


def test_metric(sushi5_report_trj1):
    publication = next(iter(sushi5_report_trj1))
    metrics = [month[1] for month in publication]
    assert metrics[0] == u"Total_Item_Requests"


def test_doi(sushi5_report_trj1):
    publication = next(iter(sushi5_report_trj1))
    assert publication.doi == "some.fake.doi"


@all_requests
def not_authorized(url_unused, request_unused):
    """Mocked SUSHI service."""
    path = os.path.join(os.path.dirname(__file__), "data", "not_authorized.json")
    with io.open(path, "r", encoding="utf-8") as datafile:
        return datafile.read()


def test_error_not_authorized():
    with pytest.raises(pycounter.exceptions.Sushi5Error) as exception:
        with HTTMock(not_authorized):
            pycounter.sushi5.get_sushi_stats_raw(
                url="https://example.com/sushi", release=5
            )
    exc = exception.value
    assert exc.message == u"Requestor Not Authorized to Access Service"
    assert exc.severity == "Error"
    assert exc.code == 2000


def test_bk_data(sushi5_report_trb1):
    publication = next(iter(sushi5_report_trb1))
    data = [month[2] for month in publication]
    assert data[0] == 22
