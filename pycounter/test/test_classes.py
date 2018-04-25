"""Tests regarding instantiating classes"""

import datetime

from pycounter import report


def test_counter_journal():
    journal = report.CounterJournal()
    assert journal.issn == u""


def test_report_gaps():
    journal = report.CounterJournal(
        period=(datetime.date(2018, 1, 1), datetime.date(2018, 3, 1)),
        month_data=[(datetime.date(2018, 1, 1), 50),
                    (datetime.date(2018, 3, 1), 99),
                    ]
    )

    output_data = journal.as_generic()
    assert output_data[11] == '0'
    assert output_data[12] == '99'
