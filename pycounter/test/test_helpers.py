"""Tests for the helpers module"""

from __future__ import absolute_import

import datetime

import pytest

from pycounter.helpers import next_month, prev_month


@pytest.mark.parametrize('pair', [((2000, 1, 1), (2000, 2, 1)),
                                  ((2000, 12, 1), (2001, 1, 1)),
                                  ((2000, 2, 29), (2000, 3, 1)),
                                  ((1999, 12, 6), (2000, 1, 1)),
                                  ])
def test_nextmonth(pair):
    assert datetime.date(*pair[1]) == next_month(datetime.date(*pair[0]))


@pytest.mark.parametrize('pair', [((2000, 1, 1), (1999, 12, 1)),
                                  ((2000, 12, 1), (2000, 11, 1)),
                                  ((2000, 2, 29), (2000, 1, 1)),
                                  ((1999, 12, 6), (1999, 11, 1)),
                                  ])
def test_prevmonth(pair):
    assert datetime.date(*pair[1]) == prev_month(datetime.date(*pair[0]))
