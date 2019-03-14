import os

import pytest

from pycounter import report
import pycounter.sushi


@pytest.fixture(
    params=["csvC4JR1", "C4JR1.csv", "simpleJR1.csv", "C4JR1_bad.csv", "C4JR1GOA.csv"]
)
def csv_jr1_report(request):
    """Various CSV format JR1 reports."""
    return report.parse(os.path.join(os.path.dirname(__file__), "data", request.param))


@pytest.fixture(params=["csvC4JR1", "C4JR1.csv", "simpleJR1.csv", "C4JR1_bad.csv"])
def csv_jr1_report_std(request):
    """Standard (non-GOA) JR1 reports."""
    return report.parse(os.path.join(os.path.dirname(__file__), "data", request.param))


@pytest.fixture(params=["csvC4JR1", "C4JR1.csv", "simpleJR1.csv"])
def csv_jr1_report_common_data(request):
    """JR1 reports with shared common data we can make assertions about."""
    return report.parse(os.path.join(os.path.dirname(__file__), "data", request.param))


@pytest.fixture(params=["csvC4JR1", "C4JR1.csv", "C4JR1_bad.csv"])
def csv_jr1_r4_report(request):
    """Revision 4 JR1 reports."""
    return report.parse(os.path.join(os.path.dirname(__file__), "data", request.param))


@pytest.fixture(params=["JR1.xlsx", "JR1_bad.xlsx"])
def jr1_report_xlsx(request):
    """Excel formatted JR1 reports."""
    return report.parse(os.path.join(os.path.dirname(__file__), "data", request.param))


def parse_sushi_file(filename):
    # pylint: disable= protected-access
    with open(os.path.join(os.path.dirname(__file__), "data", filename)) as datafile:
        return pycounter.sushi._raw_to_full(datafile.read())


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
