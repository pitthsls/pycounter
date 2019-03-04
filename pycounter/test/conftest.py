import os

import pytest

from pycounter import report


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
