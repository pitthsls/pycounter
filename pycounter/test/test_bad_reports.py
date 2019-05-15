"""Test parsing of deliberately bad data."""

from __future__ import absolute_import

import pytest

from pycounter import report
import pycounter.exceptions


@pytest.mark.parametrize(
    "report_type",
    [u"Bogus Report 7 (R4)", u"Platform Report 1 (R4)"],  # unsupported but valid
)
def test_report_type(report_type):
    """Report type doesn't exist."""
    data = [[report_type]]
    with pytest.raises(pycounter.exceptions.UnknownReportTypeError):
        report.parse_generic(iter(data))


def test_bogus_file_type():
    with pytest.raises(pycounter.exceptions.PycounterException):
        report.parse("no_such_file", "qsx")
