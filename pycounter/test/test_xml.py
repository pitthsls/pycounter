import pycounter.report


def test_xml_parsing(xml_data):
    assert pycounter.report.CounterReport.from_xml(xml_data) is not None
