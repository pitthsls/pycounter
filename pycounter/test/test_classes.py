"""Tests regarding instantiating classes"""

import unittest

from pycounter import report


class TestJournalClass(unittest.TestCase):
    def test_counter_journal(self):
        journal = report.CounterJournal()
        self.assertEqual(journal.issn, "")
