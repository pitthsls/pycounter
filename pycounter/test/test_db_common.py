"""Common DB report tests."""
import datetime

from pycounter.constants import METRICS


def test_version(db_report):
    assert db_report.report_version == 4


def test_publisher(db_report):
    for publication in db_report:
        assert publication.publisher == "Megadodo Publications"


def test_platform(db_report):
    for publication in db_report:
        assert publication.platform == "HHGTTG Online"


def test_customer(db_report):
    assert db_report.customer == "University of Maximegalon"


def test_date_run(db_report):
    assert db_report.date_run == datetime.date(2012, 7, 9)


def test_period(db_report):
    assert db_report.period == (datetime.date(2012, 1, 1), datetime.date(2012, 6, 30))


def test_report_metric(db_report):
    for metric in db_report.metric:
        assert metric in METRICS[db_report.report_type]
