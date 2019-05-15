"""Tests for BR1 and BR2 (COUNTER3/4) reports."""
import datetime


def test_version(br_c1):
    assert br_c1.report_version == 1


def test_year(br_c1):
    assert br_c1.year == 2012


def test_publisher(br_c1):
    for publication in br_c1:
        assert publication.publisher == u"Megadodo Publications"


def test_platform(br_c1):
    for publication in br_c1:
        assert publication.platform == u"HHGTTG Online"


def test_stats(br_c1):
    publication = br_c1.pubs[0]
    assert [x[2] for x in publication] == [0, 25, 0, 0, 0, 0]


def test_customer(br_c1):
    assert br_c1.customer == u"University of Maximegalon"


def test_date_run(br_c1):
    assert br_c1.date_run == datetime.date(2012, 7, 9)


def test_period(br_c1):
    assert br_c1.period == (datetime.date(2012, 1, 1), datetime.date(2012, 6, 30))
