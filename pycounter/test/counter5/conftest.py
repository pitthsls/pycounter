"""Pytest fixtures for COUNTER 5 test suite."""
import datetime
import io
import os

from httmock import HTTMock, urlmatch
import pytest

import pycounter


@urlmatch(netloc=r"(.*\.)?example\.com$")
def sushi_mock(url_unused, request_unused):
    """Mocked SUSHI service."""
    path = os.path.join(os.path.dirname(__file__), "data", "sushi_simple.json")
    with io.open(path, "r", encoding="utf-8") as datafile:
        return datafile.read()


@urlmatch(netloc=r"(.*\.)?example\.com$")
def sushi_book_mock(url_unused, request_unused):
    """Mocked SUSHI service."""
    path = os.path.join(os.path.dirname(__file__), "data", "sushi_book.json")
    with io.open(path, "r", encoding="utf-8") as datafile:
        return datafile.read()


@pytest.fixture
def trj1_report():
    """Tab-separated title report."""
    return pycounter.report.parse(
        os.path.join(os.path.dirname(__file__), "data", "tr_j1.tsv")
    )


@pytest.fixture
def trj2_report():
    """Tab-separated title turnaways report."""
    return pycounter.report.parse(
        os.path.join(os.path.dirname(__file__), "data", "tr_j2.tsv")
    )


@pytest.fixture
def sushi5_report_trb1():
    """JSON SUSHI report."""
    with HTTMock(sushi_book_mock):
        return pycounter.sushi.get_report(
            url="http://www.example.com/Sushi",
            start_date=datetime.date(2019, 1, 1),
            end_date=datetime.date(2019, 2, 28),
            release=5,
            report="TR_B1",
        )


@pytest.fixture
def sushi5_report_trj1():
    """JSON SUSHI report."""
    with HTTMock(sushi_mock):
        return pycounter.sushi.get_report(
            url="http://www.example.com/Sushi",
            start_date=datetime.date(2019, 1, 1),
            end_date=datetime.date(2019, 2, 28),
            release=5,
            report="TR_J1",
        )


@pytest.fixture(params=["tr_j1.tsv", "tr_j2.tsv"])
def all_c5_reports(request):
    """All COUNTER 4 reports."""
    return pycounter.report.parse(
        os.path.join(os.path.dirname(__file__), "data", request.param)
    )
