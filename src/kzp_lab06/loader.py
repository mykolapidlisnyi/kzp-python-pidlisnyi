"""Завантаження та перетворення CSV-записів на об'єкти GymSubscription."""

from __future__ import annotations

import csv
from pathlib import Path

from .errors import DataError
from .models import GymSubscription, PremiumSubscription, StandardSubscription

REQUIRED_COLUMNS = ("client", "plan", "months", "visits", "price")


def build_subscription(
    client: str,
    plan: str,
    months: int,
    visits: int,
    price: float,
) -> GymSubscription:
    """Фабрика вибору підтипу абонемента на основі назви тарифного плану."""
    lowered = plan.lower()
    if "premium" in lowered or "unlimited" in lowered:
        return PremiumSubscription(client, plan, months, visits, price, spa_hours=months * 2)
    return StandardSubscription(client, plan, months, visits, price)


def load_records(path: Path | str, delimiter: str = ";") -> list[GymSubscription]:
    """Зчитує CSV-файл та повертає список об'єктів GymSubscription."""
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

            records: list[GymSubscription] = []
            for line_num, row in enumerate(reader, start=2):
                if None in row and row[None]:
                    raise DataError(f"Рядок {line_num}: зайві значення поза заголовком")

                if all((val is None or val.strip() == "") for val in row.values()):
                    continue

                records.append(_parse_row(row, line_num))

            return records
    except OSError as error:
        raise DataError(f"Не вдалося прочитати файл: {csv_path}") from error


def _parse_row(row: dict[str, str | None], line_num: int) -> GymSubscription:
    client = (row.get("client") or "").strip()
    if not client:
        raise DataError(f"Рядок {line_num}, поле 'client': порожнє ім'я клієнта")

    plan = (row.get("plan") or "").strip()
    if not plan:
        raise DataError(f"Рядок {line_num}, поле 'plan': порожня назва плану")

    months = _parse_int(row.get("months"), line_num, "months")
    visits = _parse_int(row.get("visits"), line_num, "visits")
    price = _parse_float(row.get("price"), line_num, "price")

    try:
        return build_subscription(client, plan, months, visits, price)
    except ValueError as error:
        raise DataError(f"Рядок {line_num}: {error}") from error


def _parse_int(raw: str | None, line_num: int, field: str) -> int:
    text = (raw or "").strip()
    if not text:
        raise DataError(f"Рядок {line_num}, поле '{field}': відсутнє значення")
    try:
        return int(text)
    except ValueError as error:
        raise DataError(
            f"Рядок {line_num}, поле '{field}': очікувалося ціле число, отримано '{text}'"
        ) from error


def _parse_float(raw: str | None, line_num: int, field: str) -> float:
    text = (raw or "").strip()
    if not text:
        raise DataError(f"Рядок {line_num}, поле '{field}': відсутнє значення")
    try:
        return float(text)
    except ValueError as error:
        raise DataError(
            f"Рядок {line_num}, поле '{field}': очікувалося число, отримано '{text}'"
        ) from error
