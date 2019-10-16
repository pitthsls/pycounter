"""Test COUNTER JR1 journal report (TSV)"""
import datetime


def test_html(tsv_jr1):
    assert [pub.html_total for pub in tsv_jr1.pubs] == [0, 15, 33, 0]


def test_pdf(tsv_jr1):
    assert [pub.pdf_total for pub in tsv_jr1.pubs] == [32, 12, 855, 40]


def test_months(tsv_jr1):
    for pub in tsv_jr1.pubs:
        month = next(iter(pub))[0]
        assert month == datetime.date(2013, 1, 1)
