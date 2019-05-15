"""Test output of JR1 report"""

from __future__ import absolute_import

import datetime

import pycounter


def test_ordering_output():
    report = pycounter.report.CounterReport(
        report_type="JR1",
        report_version=4,
        customer=u"Foo",
        institutional_identifier=u"Bar",
        period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
    )
    report.pubs.append(
        pycounter.report.CounterJournal(
            period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
            month_data=[(datetime.date(2016, 1, 1), 260)],
            title=u"Fake Journal",
            publisher=u"No one",
            platform=u"Your imagination",
        )
    )
    report.pubs.append(
        pycounter.report.CounterJournal(
            period=(datetime.date(2016, 1, 1), datetime.date(2016, 1, 31)),
            month_data=[(datetime.date(2016, 1, 1), 62)],
            title=u"Another Fake Journal",
            publisher=u"No one",
            platform=u"Your imagination",
        )
    )
    output_content = report.as_generic()

    assert output_content[9][0] == u"Another Fake Journal"
    assert output_content[10][0] == u"Fake Journal"
