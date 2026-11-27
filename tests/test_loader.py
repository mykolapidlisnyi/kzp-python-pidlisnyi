"""Тести завантаження та валідації CSV."""

from pathlib import Path

import pytest

from kzp_lab06.errors import DataError
from kzp_lab06.loader import load_records


def test_load_valid_records_and_comma_in_text(tmp_path: Path) -> None:
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(
        "client;plan;months;visits;price\n"
        '"Ковальчук, Олексій";Full Unlimited;12;120;12000.50\n'
        "Марія Бондаренко;Standard Gym;3;0;3200\n",
        encoding="utf-8",
    )

    records = load_records(csv_file)
    assert len(records) == 2
    assert records[0]["client"] == "Ковальчук, Олексій"
    assert records[0]["months"] == 12
    assert records[0]["price"] == pytest.approx(12000.50)
    assert records[1]["visits"] == 0


def test_load_empty_csv_returns_empty_list(tmp_path: Path) -> None:
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")
    assert load_records(empty_file) == []

    header_only = tmp_path / "header_only.csv"
    header_only.write_text("client;plan;months;visits;price\n", encoding="utf-8")
    assert load_records(header_only) == []


def test_load_missing_column_raises_data_error(tmp_path: Path) -> None:
    bad_header = tmp_path / "missing_col.csv"
    bad_header.write_text("client;plan;months;visits\nІван;Standard;3;20\n", encoding="utf-8")

    with pytest.raises(DataError, match="price"):
        load_records(bad_header)


def test_load_invalid_number_and_missing_value_report_line_number(tmp_path: Path) -> None:
    bad_num = tmp_path / "bad_num.csv"
    bad_num.write_text(
        "client;plan;months;visits;price\nІван;Standard;3;20;abc\n",
        encoding="utf-8",
    )
    with pytest.raises(DataError, match="Рядок 2, поле 'price'"):
        load_records(bad_num)

    missing_val = tmp_path / "missing_val.csv"
    missing_val.write_text(
        "client;plan;months;visits;price\nІван;Standard;;20;3000\n",
        encoding="utf-8",
    )
    with pytest.raises(DataError, match="Рядок 2, поле 'months'"):
        load_records(missing_val)
