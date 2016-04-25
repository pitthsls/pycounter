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


@urlmatch(netloc=r'(.*\.)?example\.com$')
def sushi_mock(url_unused, request_unused):
    path = os.path.join(os.path.dirname(__file__),
                        'data', 'sushi_simple.xml')
    with open(path, 'rb') as datafile:
        return datafile.read().decode('utf-8')


@urlmatch(netloc=r'(.*\.)?example\.com$')
def error_mock(url_unused, request_unused):
    path = os.path.join(os.path.dirname(__file__),
                        'data', 'sushi_error.xml')
    with open(path, 'rb') as datafile:
        return datafile.read().decode('utf-8')


@urlmatch(netloc=r'(.*\.)?example\.com$')
def bogus_mock(url_unused, request_unused):
    return "Bogus response with no XML"


class TestHelpers(unittest.TestCase):
    """Test _ns helper"""

    def test_ns(self):
        self.assertEqual(
            sushi._ns("sushi", "name"),
            "{http://www.niso.org/schemas/sushi}name")


class TestConvertRawSimple(unittest.TestCase):
    """Test converting simple SUSHI response"""

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'sushi_simple.xml')
        with open(path, 'rb') as datafile:
            self.report = sushi._raw_to_full(datafile.read())

    def test_report(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 4)

    def test_customer(self):
        self.assertEqual(self.report.institutional_identifier,
                         u"exampleLibrary")

    def test_title(self):
        publication = next(iter(self.report))
        self.assertEqual(publication.title, u'Journal of fake data')

    def test_data(self):
        publication = next(iter(self.report))
        self.assertEqual(publication.html_total, 6)
        self.assertEqual(publication.pdf_total, 8)
        data = [month[2] for month in publication]
        self.assertEqual(data[0], 14)


class TestConvertRawBook(unittest.TestCase):
    """Test converting simple BR1 SUSHI response"""

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'sushi_simple_br1.xml')
        with open(path, 'rb') as datafile:
            self.report = sushi._raw_to_full(datafile.read())

    def test_report(self):
        self.assertEqual(self.report.report_type, u'BR1')
        self.assertEqual(self.report.report_version, 4)

    def test_customer(self):
        self.assertEqual(self.report.institutional_identifier,
                         u"exampleLibrary")

    def test_isbn(self):
        publication = next(iter(self.report))
        self.assertEqual(publication.isbn, u"9780011234549")

    def test_title(self):
        publication = next(iter(self.report))
        self.assertEqual(publication.title, u'Fake data')

    def test_data(self):
        publication = next(iter(self.report))
        data = [month[2] for month in publication]
        self.assertEqual(data[0], 14)


class TestConvertRawDatabase(unittest.TestCase):
    """Test converting simple DB1 SUSHI response"""

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'sushi_simple_db1.xml')
        with open(path, 'rb') as datafile:
            self.report = sushi._raw_to_full(datafile.read())
        self.databases = list(self.report)

    def test_report(self):
        self.assertEqual(self.report.report_type, u'DB1')
        self.assertEqual(self.report.report_version, 4)

    def test_customer(self):
        self.assertEqual(self.report.institutional_identifier,
                         u"exampleLibrary")

    def test_platform(self):
        database = self.databases[0]
        self.assertEqual(database.platform, u'ExamplePlatform')

    def test_publisher(self):
        database = self.databases[0]
        self.assertEqual(database.publisher, u'ExamplePublisher')

    def test_title(self):
        database = self.databases[0]
        self.assertEqual(database.title, u'ExampleDatabase')

    def test_search_reg(self):
        database = self.databases[0]
        data = [month[2] for month in database]
        self.assertEqual(database.metric, u'Regular Searches')
        self.assertEqual(data[0], 5)

    def test_search_fed(self):
        database = self.databases[1]
        data = [month[2] for month in database]
        self.assertEqual(database.metric, u'Searches-federated and automated')
        self.assertEqual(data[0], 13)

    def test_result_click(self):
        database = self.databases[2]
        data = [month[2] for month in database]
        self.assertEqual(database.metric, u'Result Clicks')
        self.assertEqual(data[0], 16)

    def test_record_view(self):
        database = self.databases[3]
        data = [month[2] for month in database]
        self.assertEqual(database.metric, u'Record Views')
        self.assertEqual(data[0], 7)


class TestRawDatabaseWithMissingData(unittest.TestCase):
    """
    Test database request with January missing for 'search_fed'
    and no 'record_view' records
    """

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'sushi_db1_missing_record_view.xml')
        with open(path, 'rb') as datafile:
            self.report = sushi._raw_to_full(datafile.read())
        # missing data only injected when making generic to write
        self.report.as_generic()
        self.databases = list(self.report)

    def test_january(self):
        database = self.databases[1]
        data = [month[2] for month in database]
        self.assertEqual(database.metric, u'Searches-federated and automated')
        self.assertEqual(data[0], 0)

    def test_record_view(self):
        database = self.databases[3]
        data = [month[2] for month in database]
        self.assertEqual(database.metric, u'Record Views')
        self.assertEqual(data[0], 0)


class TestMissingMonth(unittest.TestCase):
    """Test SUSHI with months missing"""

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'sushi_missing_jan.xml')
        with open(path, 'rb') as datafile:
            self.report = sushi._raw_to_full(datafile.read())
        self.publication = next(iter(self.report))

    def test_february(self):
        first_month_data = next(iter(self.publication))
        self.assertEqual(first_month_data[0],
                         datetime.date(2013, 2, 1))

    def test_title(self):
        self.assertEqual(self.publication.title, u'Journal of fake data')


class TestSushiRequest(unittest.TestCase):
    """Test making a SUSHI request"""

    def setUp(self):
        with HTTMock(sushi_mock):
            self.report = sushi.get_report('http://www.example.com/Sushi',
                                           datetime.date(2015, 1, 1),
                                           datetime.date(2015, 1, 31)
                                           )

    def test_report(self):
        self.assertEqual(self.report.report_type, u'JR1')
        self.assertEqual(self.report.report_version, 4)


class TestSushiDump(unittest.TestCase):
    """Test dumping SUSHI response"""

    @mock.patch('pycounter.sushi.logger')
    def test_dump(self, mock_logger):
        with HTTMock(sushi_mock):
            self.report = sushi.get_report('http://www.example.com/Sushi',
                                           datetime.date(2015, 1, 1),
                                           datetime.date(2015, 1, 31),
                                           sushi_dump=True
                                           )
        self.assertTrue(mock_logger.debug.called)


class TestBogusXML(unittest.TestCase):
    """Test dealing with broken XML"""

    def test_request(self):
        logging.disable(logging.CRITICAL)
        with HTTMock(bogus_mock):
            self.assertRaises(pycounter.exceptions.SushiException,
                              sushi.get_report,
                              'http://www.example.com/bogus',
                              datetime.date(2015, 1, 1),
                              datetime.date(2015, 1, 31)
                              )


class TestSushiError(unittest.TestCase):
    """Test error from SUSHI"""

    def test_error(self):
        with HTTMock(error_mock):
            self.assertRaises(pycounter.exceptions.SushiException,
                              sushi.get_report,
                              'http://www.example.com/out_of_range',
                              datetime.date(2015, 1, 1),
                              datetime.date(2015, 1, 31)
                              )


class TestSushiClient(unittest.TestCase):
    """Test the client"""

    def test_get(self):
        arglist = [
            'http://www.example.com/Sushi',
        ]

        with HTTMock(sushi_mock):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(sushiclient.main, arglist)
                with open('report.tsv') as tsv_file:
                    self.assertTrue('Journal Report 1' in tsv_file.read())
                self.assertEqual(result.exit_code, 0)

    def test_end_date_error(self):
        """Test trying to use implied start date and explicit end date"""
        arglist = [
            'http://www.example.com/Sushi',
            '-e', '2015-12-31',
        ]
        runner = CliRunner()
        result = runner.invoke(sushiclient.main, arglist)
        self.assertEqual(result.exit_code, 1)

    def test_explicit_dates(self):
        """Test providing both start and end dates"""
        arglist = [
            'http://www.example.com/Sushi',
            '-s', '2015-10-31',
            '-e', '2015-12-31',
        ]
        with HTTMock(sushi_mock):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(sushiclient.main, arglist)
                self.assertEqual(result.exit_code, 0)


class TestMissingItemIdentifier(unittest.TestCase):
    """Test converting simple SUSHI response"""

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'sushi_missing_ii.xml')
        with open(path, 'rb') as datafile:
            self.report = sushi._raw_to_full(datafile.read())

    def test_issn(self):
        publication = next(iter(self.report))
        self.assertEqual(publication.issn, "")
