"""regression test to ensure all output is of text type"""

from __future__ import absolute_import

import os

import pytest

from pycounter import report


@pytest.mark.parametrize("attribute", ["title", "publisher", "platform"])
@pytest.mark.parametrize("filename", ["JR1.xlsx", "simpleJR1.tsv"])
def test_unicode_fields(filename, attribute):
    """All parsers should return text fields as unicode"""
    rep = report.parse(os.path.join(os.path.dirname(__file__), "data", filename))
    assert isinstance(getattr(rep.pubs[0], attribute), str)
