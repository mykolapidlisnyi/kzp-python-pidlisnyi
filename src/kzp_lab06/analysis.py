"""Аналітичні функції обробки абонементів тренажерного залу."""

from __future__ import annotations

from collections.abc import Iterable


def filter_active_subscriptions(
    records: Iterable[dict[str, object]],
    min_visits: int = 30,
) -> list[dict[str, object]]:
    """Відбирає абонементи з кількістю відвідувань не менше min_visits (list comprehension)."""
    return [rec for rec in records if int(rec["visits"]) >= min_visits]


def unique_clients(records: Iterable[dict[str, object]]) -> set[str]:
    """Повертає множину унікальних клієнтів (set comprehension)."""
    return {str(rec["client"]) for rec in records}


def revenue_by_plan(records: Iterable[dict[str, object]]) -> dict[str, float]:
    """Обчислює загальний виторг у розрізі кожного тарифного плану."""
    totals: dict[str, float] = {}
    for rec in records:
        plan = str(rec["plan"])
        totals[plan] = totals.get(plan, 0.0) + float(rec["price"])
    return totals


def count_by_plan(records: Iterable[dict[str, object]]) -> dict[str, int]:
    """Підраховує кількість куплених абонементів для кожного тарифного плану."""
    counts: dict[str, int] = {}
    for rec in records:
        plan = str(rec["plan"])
        counts[plan] = counts.get(plan, 0) + 1
    return counts


def summarize(
    records: Iterable[dict[str, object]],
    *metrics: str,
    min_visits: int = 0,
    **labels: str,
) -> dict[str, object]:
    """Обчислює суми вибраних числових метрик після відбору за min_visits (*args, **kwargs)."""
    selected = [rec for rec in records if int(rec["visits"]) >= min_visits]
    result: dict[str, object] = {"count": len(selected)}

    allowed_metrics = {"months", "visits", "price"}
    for metric in metrics:
        if metric not in allowed_metrics:
            raise ValueError(f"Невідома метрика: {metric}")
        label = labels.get(metric, metric)
        result[label] = sum(float(rec[metric]) for rec in selected)

    return result


def make_summary(records: list[dict[str, object]]) -> dict[str, object]:
    """Формує повний словник підсумкових показників для звіту."""
    if not records:
        return {
            "count": 0,
            "unique_clients": 0,
            "average_visits": 0.0,
            "total_revenue": 0.0,
            "longest_subscription": "немає",
            "most_popular_plan": "немає",
            "most_popular_plan_count": 0,
            "revenue_by_plan": {},
        }

    total_visits = sum(int(r["visits"]) for r in records)
    total_revenue = sum(float(r["price"]) for r in records)

    longest = max(
        records,
        key=lambda r: (int(r["months"]), float(r["price"]), str(r["client"])),
    )
    longest_info = f"{longest['client']} ({longest['plan']}, {longest['months']} міс.)"

    plan_counts = count_by_plan(records)
    popular_plan, popular_count = max(
        plan_counts.items(),
        key=lambda item: (item[1], item[0]),
    )

    return {
        "count": len(records),
        "unique_clients": len(unique_clients(records)),
        "average_visits": total_visits / len(records),
        "total_revenue": total_revenue,
        "longest_subscription": longest_info,
        "most_popular_plan": popular_plan,
        "most_popular_plan_count": popular_count,
        "revenue_by_plan": revenue_by_plan(records),
    }
