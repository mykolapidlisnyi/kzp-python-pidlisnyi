"""Тести командного рядка CLI та запису звіту."""

from pathlib import Path

from kzp_lab06.cli import main


def test_cli_success_creates_utf8_report(tmp_path: Path) -> None:
    input_csv = tmp_path / "input.csv"
    output_txt = tmp_path / "out" / "report.txt"
    input_csv.write_text(
        "client;plan;months;visits;price\nТарас Шевченко;Premium Annual;12;100;10000.00\n",
        encoding="utf-8",
    )

    exit_code = main([str(input_csv), str(output_txt)])
    assert exit_code == 0
    assert output_txt.exists()
    content = output_txt.read_text(encoding="utf-8")
    assert "Тарас Шевченко (Premium Annual, 12 міс.)" in content


def test_cli_returns_nonzero_on_invalid_csv(tmp_path: Path, capsys) -> None:
    bad_csv = tmp_path / "bad.csv"
    output_txt = tmp_path / "report.txt"
    bad_csv.write_text(
        "client;plan;months;visits;price\nТарас;Premium;-5;100;10000\n",
        encoding="utf-8",
    )

    exit_code = main([str(bad_csv), str(output_txt)])
    assert exit_code == 2
    assert not output_txt.exists()
    captured = capsys.readouterr()
    assert "Рядок 2: Тривалість абонемента" in captured.err
