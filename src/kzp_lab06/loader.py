"""Завантаження та валідація записів абонементів із CSV."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from .errors import DataError

REQUIRED_COLUMNS = ("client", "plan", "months", "visits", "price")


def load_records(path: Path | str, delimiter: str = ";") -> list[dict[str, object]]:
    """Зчитує CSV-файл та повертає список типізованих словників записів."""
    csv_path = Path(path)
    try:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            if reader.fieldnames is None:
                return []

            normalized_headers = [h.strip() for h in reader.fieldnames if h is not None]
            missing = [col for col in REQUIRED_COLUMNS if col not in normalized_headers]
            if missing:
                raise DataError(f"Відсутні обов'язкові стовпці: {', '.join(missing)}")

            records: list[dict[str, object]] = []
            for line_num, row in enumerate(reader, start=2):
                if None in row and row[None]:
                    raise DataError(f"Рядок {line_num}: зайві значення поза заголовком")

                if all((val is None or val.strip() == "") for val in row.values()):
                    continue

                records.append(_parse_row(row, line_num))

            return records
    except OSError as error:
        raise DataError(f"Не вдалося прочитати файл: {csv_path}") from error


def _parse_row(row: dict[str, str | None], line_num: int) -> dict[str, object]:
    client = (row.get("client") or "").strip()
    if not client:
        raise DataError(f"Рядок {line_num}, поле 'client': порожнє ім'я клієнта")

    plan = (row.get("plan") or "").strip()
    if not plan:
        raise DataError(f"Рядок {line_num}, поле 'plan': порожня назва плану")

    months = _parse_int(row.get("months"), line_num, "months", min_value=1)
    visits = _parse_int(row.get("visits"), line_num, "visits", min_value=0)
    price = _parse_float(row.get("price"), line_num, "price", min_exclusive=0.0)

    return {
        "client": client,
        "plan": plan,
        "months": months,
        "visits": visits,
        "price": price,
    }


def _parse_int(raw: str | None, line_num: int, field: str, min_value: int) -> int:
    text = (raw or "").strip()
    if not text:
        raise DataError(f"Рядок {line_num}, поле '{field}': відсутнє значення")
    try:
        value = int(text)
    except ValueError as error:
        raise DataError(
            f"Рядок {line_num}, поле '{field}': очікувалося ціле число, отримано '{text}'"
        ) from error
    if value < min_value:
        raise DataError(
            f"Рядок {line_num}, поле '{field}': значення {value} менше допустимого ({min_value})"
        )
    return value


def _parse_float(raw: str | None, line_num: int, field: str, min_exclusive: float) -> float:
    text = (raw or "").strip()
    if not text:
        raise DataError(f"Рядок {line_num}, поле '{field}': відсутнє значення")
    try:
        value = float(text)
    except ValueError as error:
        raise DataError(
            f"Рядок {line_num}, поле '{field}': очікувалося число, отримано '{text}'"
        ) from error
    if not math.isfinite(value) or value <= min_exclusive:
        raise DataError(
            f"Рядок {line_num}, поле '{field}': ціна має бути додатною, отримано '{text}'"
        )
    return value
