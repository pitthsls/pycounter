"""Pytest fixtures for main test suite."""
import os

import pytest

from pycounter import csvhelper
from pycounter import report
import pycounter.sushi


def parsedata(filename):
    """Helper function returns a report from a filename relative to data directory."""
    return report.parse(os.path.join(os.path.dirname(__file__), "data", filename))


@pytest.fixture(
    params=["csvC4JR1", "C4JR1.csv", "simpleJR1.csv", "C4JR1_bad.csv", "C4JR1GOA.csv"]
)
def csv_jr1_report(request):
    """Various CSV format JR1 reports."""
    return parsedata(request.param)


@pytest.fixture(params=["csvC4JR1", "C4JR1.csv", "simpleJR1.csv", "C4JR1_bad.csv"])
def csv_jr1_report_std(request):
    """Standard (non-GOA) JR1 reports."""
    return parsedata(request.param)


@pytest.fixture(params=["csvC4JR1", "C4JR1.csv", "simpleJR1.csv"])
def csv_jr1_report_common_data(request):
    """JR1 reports with shared common data we can make assertions about."""
    return parsedata(request.param)


@pytest.fixture(params=["csvC4JR1", "C4JR1.csv", "C4JR1_bad.csv"])
def csv_jr1_r4_report(request):
    """Revision 4 JR1 reports."""
    return parsedata(request.param)


@pytest.fixture(params=["JR1.xlsx", "JR1_bad.xlsx", "xlsxJR1"])
def jr1_report_xlsx(request):
    """Excel formatted JR1 reports."""
    return parsedata(request.param)


def parse_sushi_file(filename):
    """Turn SUSHI data file into a report."""
    # pylint: disable= protected-access
    with open(os.path.join(os.path.dirname(__file__), "data", filename)) as datafile:
        return pycounter.sushi.raw_to_full(datafile.read())


@pytest.fixture(
    params=[
        "sushi_simple.xml",
        "sushi_simple_no_customer.xml",
        "sushi_simple_br1.xml",
        "sushi_simple_db1.xml",
        "sushi_db1_missing_record_view.xml",
    ]
)
def sushi_report_all(request):
    """Report from SUSHI, shared common data."""
    return parse_sushi_file(request.param)


@pytest.fixture(
    params=[
        "sushi_simple.xml",
        "sushi_simple_br1.xml",
        "sushi_simple_db1.xml",
        "sushi_db1_missing_record_view.xml",
    ]
)
def sushi_report_with_customer(request):
    """Report from SUSHI, shared common data with customer set."""
    return parse_sushi_file(request.param)


@pytest.fixture(params=["sushi_simple_no_customer.xml"])
def sushi_report_no_customer(request):
    """Report from SUSHI, shared common data with customer not set."""
    return parse_sushi_file(request.param)


@pytest.fixture(params=["sushi_simple.xml", "sushi_simple_no_customer.xml"])
def sushi_report_jr1(request):
    """Report from SUSHI, shared common data, JR1 only."""
    return parse_sushi_file(request.param)


@pytest.fixture(
    params=[
        "C4BR1.tsv",
        "C4DB1.tsv",
        "C4JR1.csv",
        "C4BR2.tsv",
        "C4DB2.tsv",
        "C4JR1mul.csv",
    ]
)
def common_output(request):
    """Common data for output."""
    delim = {"tsv": "\t", "csv": ","}[request.param.split(".")[1]]
    filename = os.path.join(os.path.dirname(__file__), "data", request.param)
    with csvhelper.UnicodeReader(filename, delimiter=delim) as report_reader:
        content = list(report_reader)
    return parsedata(request.param).as_generic(), content


@pytest.fixture(params=["simpleBR1.csv", "simpleBR2.csv"])
def br_c1(request):
    """Version 1 (COUNTER 3) book reports."""
    return parsedata(request.param)


@pytest.fixture(params=["C4BR2.tsv", "C4BR1.tsv", "simpleBR1.csv", "simpleBR2.csv"])
def all_book_reports(request):
    """All book reports."""
    return parsedata(request.param)


@pytest.fixture(params=["C4BR1.tsv", "simpleJR1.tsv"])
def report_file_output(request):
    """Reports with their expected output."""
    rpt = parsedata(request.param)
    with open(
        os.path.join(os.path.dirname(__file__), "data", request.param), "rb"
    ) as f:
        expected_data = f.read()
    return rpt, expected_data


@pytest.fixture(params=["C4DB1.tsv", "C4DB2.tsv"])
def db_report(request):
    """All C4 database reports."""
    return parsedata(request.param)
