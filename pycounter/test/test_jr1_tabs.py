"""Test COUNTER JR1 journal report (TSV)"""


def test_html(tsv_jr1):
    assert [pub.html_total for pub in tsv_jr1.pubs] == [0, 15, 33, 0]


def test_pdf(tsv_jr1):
    assert [pub.pdf_total for pub in tsv_jr1.pubs] == [32, 12, 855, 40]
