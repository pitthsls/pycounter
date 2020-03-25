"""Test COUNTER DB1 database report"""
import os

import pycounter.report


def test_pr1_reportname(pr1_report):
    assert pr1_report.report_type == "PR1"


def test_pr1_stats(pr1_report):
    publication = pr1_report.pubs[0]
    assert [x[2] for x in publication] == [91, 41, 13, 21, 44, 8, 0, 0, 36, 36, 7, 2]


def test_pr1_row_metric(pr1_report):
    # test metric of the first row
    jan_data = next(iter(pr1_report.pubs[0]))
    assert jan_data[1] == "Regular Searches"
    # test metric of the second row
    jan_data = next(iter(pr1_report.pubs[1]))
    assert jan_data[1] == "Searches-federated and automated"


def test_output(tmp_path):
    report = pycounter.report.parse(
        os.path.join(os.path.dirname(__file__), "data/PR1.tsv")
    )
    report.write_tsv(str(tmp_path / "outputfile.tsv"))
    with open(str(tmp_path / "outputfile.tsv"), "rb") as new_file:
        new_content = new_file.read()
    assert b"Searches-federated" in new_content
