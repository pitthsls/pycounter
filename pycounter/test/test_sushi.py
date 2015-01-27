"""Tests for pycounter.sushi"""

from __future__ import absolute_import

import unittest
import os

from pycounter import sushi

class TestHelpers(unittest.TestCase):
    def test_ns(self):
        self.assertEqual(
            sushi._ns("sushi", "name"),
            "{http://www.niso.org/schemas/sushi}name")
