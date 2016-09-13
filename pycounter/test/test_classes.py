"""Tests regarding instantiating classes"""

from pycounter import report


def test_counter_journal():
    journal = report.CounterJournal()
    assert journal.issn == u""
