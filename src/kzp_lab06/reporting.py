"""Формування та збереження детермінованого текстового звіту."""

from __future__ import annotations

from pathlib import Path


def format_report(summary: dict[str, object]) -> str:
    """Перетворює словник підсумків у стабільний текстовий звіт."""
    lines = [
        "=== ЗВІТ ОБРОБКИ ДАНИХ PYTHON (Варіант 20: Тренажерний зал) ===",
        "Студент: Підлісний Микола Олександрович",
        "---------------------------------------",
    ]

    if int(summary["count"]) == 0:
        lines.append("Не знайдено жодного запису для обробки.")
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            f"1. Кількість записів (унікальних клієнтів): "
            f"{summary['count']} ({summary['unique_clients']})",
            f"2. Середня кількість відвідувань: {float(summary['average_visits']):.2f}",
            f"3. Загальний виторг: {float(summary['total_revenue']):.2f} грн",
            f"4. Найдовший абонемент: {summary['longest_subscription']}",
            f"5. Найпопулярніший абонемент: {summary['most_popular_plan']} "
            f"(куплено: {summary['most_popular_plan_count']})",
        ]
    )

    by_plan: dict[str, float] = summary["revenue_by_plan"]  # type: ignore[assignment]
    for plan, amount in sorted(by_plan.items()):
        lines.append(f"   - {plan}: {amount:.2f} грн")

    lines.append("---------------------------------------")
    return "\n".join(lines) + "\n"


def write_report(path: Path | str, text: str) -> None:
    """Записує текст звіту у файл UTF-8 із переносами рядків LF."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
