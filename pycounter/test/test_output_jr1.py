"""Test output of JR1 report"""

import datetime

import pycounter


def test_ordering_output():
    report = pycounter.report.CounterReport(
        report_type="JR1",
        report_version=4,
        customer="Foo",
        institutional_identifier="Bar",
        period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
    )
    report.pubs.append(
        pycounter.report.CounterJournal(
            period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
            month_data=[(datetime.date(2016, 1, 1), 260)],
            title="Fake Journal",
            publisher="No one",
            platform="Your imagination",
        )
    )
    report.pubs.append(
        pycounter.report.CounterJournal(
            period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
            month_data=[(datetime.date(2016, 1, 1), 62)],
            title="Another Fake Journal",
            publisher="No one",
            platform="Your imagination",
        )
    )
    output_content = report.as_generic()

    assert output_content[9][0] == "Another Fake Journal"
    assert output_content[10][0] == "Fake Journal"
