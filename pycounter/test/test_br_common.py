"""Tests for BR1 and BR2 (COUNTER3/4) reports."""
import datetime


def test_publisher(all_book_reports):
    for publication in all_book_reports:
        assert publication.publisher == "Megadodo Publications"


def test_platform(all_book_reports):
    for publication in all_book_reports:
        assert publication.platform == "HHGTTG Online"


def test_stats(all_book_reports):
    publication = all_book_reports.pubs[0]
    assert [x[2] for x in publication] == [0, 25, 0, 0, 0, 0]


def test_customer(all_book_reports):
    assert all_book_reports.customer == "University of Maximegalon"


def test_date_run(all_book_reports):
    assert all_book_reports.date_run == datetime.date(2012, 7, 9)


def test_period(all_book_reports):
    assert all_book_reports.period == (
        datetime.date(2012, 1, 1),
        datetime.date(2012, 6, 30),
    )
