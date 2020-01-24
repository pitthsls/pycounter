"""Tests for the helpers module"""

from __future__ import absolute_import

import datetime

import pytest

from pycounter.helpers import (
    convert_covered,
    convert_date_run,
    is_first_last,
    next_month,
    prev_month,
)


@pytest.mark.parametrize(
    "pair",
    [
        ((2000, 1, 1), (2000, 2, 1)),
        ((2000, 12, 1), (2001, 1, 1)),
        ((2000, 2, 29), (2000, 3, 1)),
        ((1999, 12, 6), (2000, 1, 1)),
    ],
)
def test_nextmonth(pair):
    assert datetime.date(*pair[1]) == next_month(datetime.date(*pair[0]))


@pytest.mark.parametrize(
    "pair",
    [
        ((2000, 1, 1), (1999, 12, 1)),
        ((2000, 12, 1), (2000, 11, 1)),
        ((2000, 2, 29), (2000, 1, 1)),
        ((1999, 12, 6), (1999, 11, 1)),
    ],
)
def test_prevmonth(pair):
    assert datetime.date(*pair[1]) == prev_month(datetime.date(*pair[0]))


@pytest.mark.parametrize(
    "period,expected",
    [
        (((2000, 1, 1), (2000, 1, 31)), True),
        (((2000, 1, 2), (2000, 1, 31)), False),
        (((2000, 1, 1), (2000, 1, 30)), False),
    ],
)
def test_is_first_last(period, expected):
    dt_period = tuple(datetime.date(*part) for part in period)
    assert is_first_last(dt_period) == expected


@pytest.mark.parametrize(
    "covered_line, expected",
    [
        ("2017-01-01 to 2017-06-30", ((2017, 1, 1), (2017, 6, 30))),
        ("Begin_Date=2019-01-01; End_Date=2019-12-31", ((2019, 1, 1), (2019, 12, 31))),
    ],
)
def test_convert_covered(covered_line, expected):
    expected_dates = tuple(datetime.date(*val) for val in expected)
    assert convert_covered(covered_line) == expected_dates


@pytest.mark.parametrize(
    "date_run, expected",
    [("2017-01-01", (2017, 1, 1)), ("2020-01-24T14:04:36Z", (2020, 1, 24))],
)
def test_convert_date_run(date_run, expected):
    expected_date = datetime.date(*expected)
    assert convert_date_run(date_run) == expected_date
