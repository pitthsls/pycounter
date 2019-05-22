"""Test COUNTER JR1 journal report (Excel)"""

from __future__ import absolute_import

import pytest


def test_report_type(jr1_report_xlsx):
    assert jr1_report_xlsx.report_type == u"JR1"


def test_report_version(jr1_report_xlsx):
    assert jr1_report_xlsx.report_version == 4


def test_year(jr1_report_xlsx):
    assert jr1_report_xlsx.year == 2013


def test_publisher(jr1_report_xlsx):
    assert all(  # pragma: no branch
        publication.publisher == u"American Medical Association"
        for publication in jr1_report_xlsx
    )


def test_platform(jr1_report_xlsx):
    for publication in jr1_report_xlsx:
        assert publication.platform == u"Silverchair"


@pytest.mark.parametrize(
    "pub_number,expected",
    [
        (0, [4, 14, 13, 30, 19, 7, 31, 6, 16, 12, 8, 12]),
        (1, [5414, 5459, 4936, 5172, 4064, 3904, 4054, 4090, 5010, 6680, 5961, 3742]),
        (8, [592, 574, 502, 616, 349, 476, 460, 383, 434, 496, 522, 304]),
    ],
)
def test_stats(jr1_report_xlsx, pub_number, expected):
    publication = jr1_report_xlsx.pubs[pub_number]
    assert [x[2] for x in publication] == expected
