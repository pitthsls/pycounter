"""Check data in common output formats."""


def test_header_content(common_output):
    assert common_output[0][0:7] == common_output[1][0:7]


def test_table_header(common_output):
    assert common_output[0][7] == common_output[1][7]


def test_totals(common_output):
    assert common_output[0] == common_output[1]


def test_data(common_output):
    for index, line in enumerate(common_output[1][9:], 9):
        assert line == common_output[0][index]


def test_writing_file(report_file_output, tmp_path):
    report, expected_data = report_file_output

    report.write_tsv(str(tmp_path / "outputfile.tsv"))
    with open(str(tmp_path / "outputfile.tsv"), "rb") as new_file:
        new_content = new_file.read()

    assert expected_data == new_content
