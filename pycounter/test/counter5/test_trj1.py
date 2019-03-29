"""Tests of title report for journals."""
from datetime import date
import os

import pycounter.report


def test_version(trj1_report):
    assert trj1_report.report_version == 5


def test_report_type(trj1_report):
    assert trj1_report.report_type == "TR_J1"


def test_pubs_length(trj1_report):
    assert len(trj1_report.pubs) == 4


def test_customer(trj1_report):
    assert trj1_report.customer == "Sample University"


def test_period(trj1_report):
    assert trj1_report.period == (date(2017, 1, 1), date(2017, 6, 30))


def test_parse():
    report = pycounter.report.parse(
        os.path.join(os.path.dirname(__file__), "data", "tr_j1.tsv")
    )
    assert report.report_version == 5
