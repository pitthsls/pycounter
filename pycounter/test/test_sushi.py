"""Tests for pycounter.sushi"""
from __future__ import absolute_import

import datetime
import logging
import os
import unittest

from click.testing import CliRunner
from httmock import HTTMock, urlmatch
import mock

from pycounter import sushi
from pycounter import sushiclient
import pycounter.exceptions


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
    assert sushi.ns("sushi", "name") == "{http://www.niso.org/schemas/sushi}name"


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


class TestRawDatabaseWithMissingData(unittest.TestCase):
    """
    Test database request with January missing for 'search_fed'
    and no 'record_view' records
    """

    def setUp(self):
        path = os.path.join(
            os.path.dirname(__file__), "data", "sushi_db1_missing_record_view.xml"
        )
        with open(path, "rb") as datafile:
            self.report = sushi.raw_to_full(datafile.read())
        # missing data only injected when making generic to write
        self.report.as_generic()
        self.databases = list(self.report)

    def test_january(self):
        database = self.databases[1]
        data = [month[2] for month in database]
        self.assertEqual(database.metric, "Searches-federated and automated")
        self.assertEqual(data[0], 0)

    def test_record_view(self):
        database = self.databases[3]
        data = [month[2] for month in database]
        self.assertEqual(database.metric, "Record Views")
        self.assertEqual(data[0], 0)


class TestMissingMonth(unittest.TestCase):
    """Test SUSHI with months missing"""

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "data", "sushi_missing_jan.xml")
        with open(path, "rb") as datafile:
            self.report = sushi.raw_to_full(datafile.read())
        self.publication = next(iter(self.report))

    def test_february(self):
        first_month_data = next(iter(self.publication))
        self.assertEqual(first_month_data[0], datetime.date(2013, 2, 1))

    def test_title(self):
        self.assertEqual(self.publication.title, "Journal of fake data")


class TestSushiRequest(unittest.TestCase):
    """Test making a SUSHI request"""

    def setUp(self):
        with HTTMock(sushi_mock):
            self.report = sushi.get_report(
                "http://www.example.com/Sushi",
                datetime.date(2015, 1, 1),
                datetime.date(2015, 1, 31),
            )

    def test_report(self):
        self.assertEqual(self.report.report_type, "JR1")
        self.assertEqual(self.report.report_version, 4)


class TestSushiDump(unittest.TestCase):
    """Test dumping SUSHI response"""

    @mock.patch("pycounter.sushi.logger")
    def test_dump(self, mock_logger):
        with HTTMock(sushi_mock):
            sushi.get_report(
                "http://www.example.com/Sushi",
                datetime.date(2015, 1, 1),
                datetime.date(2015, 1, 31),
                sushi_dump=True,
            )
        self.assertTrue(mock_logger.debug.called)


class TestBogusXML(unittest.TestCase):
    """Test dealing with broken XML"""

    def test_request(self):
        logging.disable(logging.CRITICAL)
        with HTTMock(bogus_mock):
            self.assertRaises(
                pycounter.exceptions.SushiException,
                sushi.get_report,
                "http://www.example.com/bogus",
                datetime.date(2015, 1, 1),
                datetime.date(2015, 1, 31),
            )


class TestSushiError(unittest.TestCase):
    """Test error from SUSHI"""

    def test_error(self):
        with HTTMock(error_mock):
            self.assertRaises(
                pycounter.exceptions.SushiException,
                sushi.get_report,
                "http://www.example.com/out_of_range",
                datetime.date(2015, 1, 1),
                datetime.date(2015, 1, 31),
            )


class TestSushiClient(unittest.TestCase):
    """Test the client"""

    def test_get(self):
        arglist = ["http://www.example.com/Sushi"]

        with HTTMock(sushi_mock):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(sushiclient.main, arglist)
                with open("report.tsv") as tsv_file:
                    self.assertTrue("Journal Report 1" in tsv_file.read())
                self.assertEqual(result.exit_code, 0)

    def test_output_file(self):
        arglist = ["-o", "other_report.tsv", "http://www.example.com/Sushi"]

        with HTTMock(sushi_mock):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(sushiclient.main, arglist)
                with open("other_report.tsv") as tsv_file:
                    self.assertTrue("Journal Report 1" in tsv_file.read())
                self.assertEqual(result.exit_code, 0)

    def test_end_date_error(self):
        """Test trying to use implied start date and explicit end date"""
        arglist = ["http://www.example.com/Sushi", "-e", "2015-12-31"]
        runner = CliRunner()
        result = runner.invoke(sushiclient.main, arglist)
        self.assertEqual(result.exit_code, 1)

    def test_explicit_dates(self):
        """Test providing both start and end dates"""
        arglist = [
            "http://www.example.com/Sushi",
            "-s",
            "2015-10-31",
            "-e",
            "2015-12-31",
        ]
        with HTTMock(sushi_mock):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(sushiclient.main, arglist)
                self.assertEqual(result.exit_code, 0)

    def test_queued_report(self):
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
                self.assertEqual(result.exit_code, 0)


def test_missing_issn(sushi_missing_ii):
    publication = next(iter(sushi_missing_ii))
    assert publication.issn == ""
