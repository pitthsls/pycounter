"""Tests for pycounter.sushi"""
import datetime
import logging
import os

from click.testing import CliRunner
from httmock import HTTMock, urlmatch
import mock
import pytest

from pycounter import sushi
from pycounter import sushiclient
import pycounter.exceptions
import pycounter.helpers


@urlmatch(netloc=r"(.*\.)?example\.com$")
def report_queued_mock(url_unused, request_unused):
    if report_queued_mock.first_request:
        path = os.path.join(os.path.dirname(__file__), "data", "sushi_queued.xml")
        report_queued_mock.first_request = False
    else:
        path = os.path.join(os.path.dirname(__file__), "data", "sushi_simple.xml")
    with open(path, "rb") as datafile:
        return datafile.read().decode("utf-8")


report_queued_mock.first_request = True


@urlmatch(netloc=r"(.*\.)?example\.com$")
def sushi_mock(url_unused, request_unused):
    path = os.path.join(os.path.dirname(__file__), "data", "sushi_simple.xml")
    with open(path, "rb") as datafile:
        return datafile.read().decode("utf-8")


@urlmatch(netloc=r"(.*\.)?example\.com$")
def error_mock(url_unused, request_unused):
    path = os.path.join(os.path.dirname(__file__), "data", "sushi_error.xml")
    with open(path, "rb") as datafile:
        return datafile.read().decode("utf-8")


@urlmatch(netloc=r"(.*\.)?example\.com$")
def bogus_mock(url_unused, request_unused):
    return "Bogus response with no XML"


def test_helper_ns():
    """Test _ns helper"""
    assert (
        pycounter.helpers.ns("sushi", "name")
        == "{http://www.niso.org/schemas/sushi}name"
    )


def test_report_version(sushi_report_all):
    assert sushi_report_all.report_version == 4


def test_report_customer(sushi_report_with_customer):
    assert sushi_report_with_customer.institutional_identifier == "exampleLibrary"


def test_report_no_customer(sushi_report_no_customer):
    assert sushi_report_no_customer.institutional_identifier == ""


def test_report_type_jr1(sushi_report_jr1):
    assert sushi_report_jr1.report_type == "JR1"


def test_data_jr1(sushi_report_jr1):
    publication = next(iter(sushi_report_jr1))
    assert publication.html_total == 6
    assert publication.pdf_total == 8
    assert publication.doi == "10.5555/12345678"
    assert publication.proprietary_id == "JFD"

    data = [month[2] for month in publication]

    assert data[0] == 14


def test_title_jr1(sushi_report_jr1):
    publication = next(iter(sushi_report_jr1))
    assert publication.title == "Journal of fake data"


def test_data_jr2(sushi_report_jr2):
    assert [next(iter(line)) for line in sushi_report_jr2] == [
        (
            datetime.date(2013, 1, 1),
            "Access denied: concurrent/simultaneous user license exceeded",
            6,
        ),
        (datetime.date(2013, 1, 1), "Access denied: content item not licensed", 8),
    ]


def test_data_br3(sushi_report_br3):
    assert [next(iter(line)) for line in sushi_report_br3] == [
        (
            datetime.date(2013, 1, 1),
            "Access denied: concurrent/simultaneous user license exceeded",
            6,
        ),
        (datetime.date(2013, 1, 1), "Access denied: content item not licensed", 8),
    ]


def test_ssbr1_report(sushi_simple_br1):
    assert sushi_simple_br1.report_type == "BR1"


def test_ssbr1_isbn(sushi_simple_br1):
    i_report = iter(sushi_simple_br1)
    publication = next(i_report)
    assert publication.isbn == "9780011234549"

    next(i_report)
    pub3 = next(i_report)
    assert pub3.isbn == "9780011234540"


def test_ssbr1_title(sushi_simple_br1):
    publication = next(iter(sushi_simple_br1))
    assert publication.title == "Fake data"


def test_ssbr1_data(sushi_simple_br1):
    publication = next(iter(sushi_simple_br1))
    data = [month[2] for month in publication]
    assert data[0] == 14


def test_ssbr1_proprietary(sushi_simple_br1):
    publication = next(iter(sushi_simple_br1))
    assert publication.proprietary_id == "FD"


def test_db_report(sushi_simple_db1):
    assert sushi_simple_db1.report_type == "DB1"


def test_db_platform(sushi_simple_db1):
    database = list(sushi_simple_db1)[0]
    assert database.platform == "ExamplePlatform"


def test_db_publisher(sushi_simple_db1):
    database = list(sushi_simple_db1)[0]
    assert database.publisher == "ExamplePublisher"


def test_db_title(sushi_simple_db1):
    database = list(sushi_simple_db1)[0]
    assert database.title == "ExampleDatabase"


def test_db_search_reg(sushi_simple_db1):
    database = list(sushi_simple_db1)[0]
    data = [month[2] for month in database]
    assert database.metric == "Regular Searches"
    assert data[0] == 5


def test_db_search_fed(sushi_simple_db1):
    database = list(sushi_simple_db1)[1]
    data = [month[2] for month in database]
    assert database.metric == "Searches-federated and automated"
    assert data[0] == 13


def test_db_result_click(sushi_simple_db1):
    database = list(sushi_simple_db1)[2]
    data = [month[2] for month in database]
    assert database.metric == "Result Clicks"
    assert data[0] == 16


def test_db_record_view(sushi_simple_db1):
    database = list(sushi_simple_db1)[3]
    data = [month[2] for month in database]
    assert database.metric == "Record Views"
    assert data[0] == 7


def test_missing_january(sushi_missing_rec):
    database = list(sushi_missing_rec)[1]
    data = [month[2] for month in database]
    assert database.metric == "Searches-federated and automated"
    assert data[0] == 0


def test_missing_record_view(sushi_missing_rec):
    database = list(sushi_missing_rec)[3]
    data = [month[2] for month in database]
    assert database.metric == "Record Views"
    assert data[0] == 0


def test_mj_february(sushi_missing_jan):
    publication = next(iter(sushi_missing_jan))
    first_month_data = next(iter(publication))
    assert first_month_data[0] == datetime.date(2013, 2, 1)


def test_mj_title(sushi_missing_jan):
    publication = next(iter(sushi_missing_jan))
    assert publication.title == "Journal of fake data"


def test_sushi_request():
    """Test making a SUSHI request"""
    with HTTMock(sushi_mock):
        rpt = sushi.get_report(
            "http://www.example.com/Sushi",
            datetime.date(2015, 1, 1),
            datetime.date(2015, 1, 31),
        )
    assert rpt.report_type == "JR1"
    assert rpt.report_version == 4


@mock.patch("pycounter.sushi.logger")
def test_sushi_dump(mock_logger):
    """Test dumping SUSHI response"""
    with HTTMock(sushi_mock):
        sushi.get_report(
            "http://www.example.com/Sushi",
            datetime.date(2015, 1, 1),
            datetime.date(2015, 1, 31),
            sushi_dump=True,
        )
    assert mock_logger.debug.called


def test_bogus_xml():
    """Test dealing with broken XML"""
    logging.disable(logging.CRITICAL)
    with HTTMock(bogus_mock):
        with pytest.raises(pycounter.exceptions.SushiException):
            sushi.get_report(
                "http://www.example.com/bogus",
                datetime.date(2015, 1, 1),
                datetime.date(2015, 1, 31),
            )


def test_sushi_error():
    """Test error from SUSHI"""
    with HTTMock(error_mock):
        with pytest.raises(pycounter.exceptions.SushiException):
            sushi.get_report(
                "http://www.example.com/out_of_range",
                datetime.date(2015, 1, 1),
                datetime.date(2015, 1, 31),
            )


def test_sushi_client_get():
    arglist = ["http://www.example.com/Sushi"]

    with HTTMock(sushi_mock):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(sushiclient.main, arglist)
            with open("report.tsv") as tsv_file:
                assert "Journal Report 1" in tsv_file.read()
            assert result.exit_code == 0


def test_sushi_client_output_file():
    arglist = ["-o", "other_report.tsv", "http://www.example.com/Sushi"]

    with HTTMock(sushi_mock):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(sushiclient.main, arglist)
            with open("other_report.tsv") as tsv_file:
                assert "Journal Report 1" in tsv_file.read()
            assert result.exit_code == 0


def test_sushi_client_end_date_error():
    """Test trying to use implied start date and explicit end date"""
    arglist = ["http://www.example.com/Sushi", "-e", "2015-12-31"]
    runner = CliRunner()
    result = runner.invoke(sushiclient.main, arglist)
    assert result.exit_code == 1


def test_sushi_client_explicit_dates():
    """Test providing both start and end dates"""
    arglist = ["http://www.example.com/Sushi", "-s", "2015-10-31", "-e", "2015-12-31"]
    with HTTMock(sushi_mock):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(sushiclient.main, arglist)
            assert result.exit_code == 0


def test_sushi_client_queued_report():
    """Test that queued report is retried"""
    arglist = [
        "http://www.example.com/Sushi",
        "-s",
        "2013-01-01",
        "-e",
        "2013-01-31",
        "--no-delay",
    ]
    with HTTMock(report_queued_mock):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(sushiclient.main, arglist)
            assert result.exit_code == 0


def test_missing_issn(sushi_missing_ii):
    publication = next(iter(sushi_missing_ii))
    assert publication.issn == ""
