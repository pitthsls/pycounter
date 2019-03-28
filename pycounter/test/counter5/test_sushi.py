def test_report(sushi5_report):

    assert sushi5_report.report_type == u"TR_J1"
    assert sushi5_report.report_version == 5
