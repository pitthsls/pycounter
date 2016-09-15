import os

import pytest

from pycounter import report


@pytest.fixture(params=['csvC4JR1', 'C4JR1.csv', 'simpleJR1.csv',
                        'C4JR1_bad.csv', 'C4JR1GOA.csv'])
def csv_jr1_report(request):
    return report.parse(os.path.join(os.path.dirname(__file__),
                                     'data', request.param))


@pytest.fixture(params=['csvC4JR1', 'C4JR1.csv', 'simpleJR1.csv',
                        'C4JR1_bad.csv'])
def csv_jr1_report_std(request):
    return report.parse(os.path.join(os.path.dirname(__file__),
                                     'data', request.param))


@pytest.fixture(params=['csvC4JR1', 'C4JR1.csv', 'simpleJR1.csv'])
def csv_jr1_report_common_data(request):
    return report.parse(os.path.join(os.path.dirname(__file__),
                                     'data', request.param))


@pytest.fixture(params=['csvC4JR1', 'C4JR1.csv', 'C4JR1_bad.csv'])
def csv_jr1_r4_report(request):
    return report.parse(os.path.join(os.path.dirname(__file__),
                                     'data', request.param))
