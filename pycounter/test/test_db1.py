"""Test COUNTER DB1 database report"""


def test_reportname(c4db1):
    assert c4db1.report_type == "DB1"


def test_stats(c4db1):
    publication = c4db1.pubs[0]
    assert [x[2] for x in publication] == [0, 20, 0, 0, 5, 0]


def test_row_metric(c4db1):
    publication = c4db1.pubs[0]
    jan_data = next(iter(publication))
    assert jan_data[1] == "Regular Searches"


def test_split_year_reportname(c4db1_sy):
    assert c4db1_sy.report_type == "DB1"
