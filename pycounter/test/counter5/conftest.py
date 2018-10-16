import os

import pytest

import pycounter


@pytest.fixture
def trj1_report():
    return pycounter.report.parse(
        os.path.join(os.path.dirname(__file__), "data", "tr_j1.tsv")
    )
