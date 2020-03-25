"""Test COUNTER DB2 database report"""


def test_c4db2_reportname(c4db2):
    assert c4db2.report_type == "DB2"


def test_c4db2_stats(c4db2):
    publication = c4db2.pubs[0]
    assert [x[2] for x in publication] == [0, 5, 0, 0, 0, 0]


def test_c4db2_row_metric(c4db2):
    publication = c4db2.pubs[0]
    jan_data = next(iter(publication))
    assert (
        jan_data[1] == "Access denied: concurrent/"
        "simultaneous user license "
        "limit exceeded"
    )
