"""Test C5 output."""


def test_roundtrippable(all_c5_reports, tmp_path):
    """Test that all of our parsable reports can also be output."""
    all_c5_reports.write_tsv(str(tmp_path / "output.tsv"))


def test_output_sushi(sushi5_report_trj1, tmp_path):
    sushi5_report_trj1.write_tsv(str(tmp_path / "output.tsv"))
