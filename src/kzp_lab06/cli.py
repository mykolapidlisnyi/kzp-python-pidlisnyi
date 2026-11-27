"""Інтерфейс командного рядка (CLI) для пакета kzp_lab06."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .analysis import make_summary
from .errors import DataError
from .loader import load_records
from .reporting import format_report, write_report


def build_parser() -> argparse.ArgumentParser:
    """Створює парсер аргументів командного рядка."""
    parser = argparse.ArgumentParser(
        prog="kzp-lab06",
        description="Обробка даних абонементів тренажерного залу (Варіант 20)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Шлях до вхідного CSV-файла",
    )
    parser.add_argument(
        "output_report",
        type=Path,
        help="Шлях до вихідного текстового звіту",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Точка входу CLI: повертає 0 при успіху або ненульовий код при помилці даних."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = build_parser().parse_args(argv)

    if args.input_csv.resolve() == args.output_report.resolve():
        print("Помилка даних: вихідний файл звіту не може збігатися з вхідним CSV", file=sys.stderr)
        return 2

    try:
        records = load_records(args.input_csv)
        summary = make_summary(records)
        report_text = format_report(summary)
        write_report(args.output_report, report_text)
    except DataError as error:
        print(f"Помилка даних: {error}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
