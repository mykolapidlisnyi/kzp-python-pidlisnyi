"""Об'єктно-орієнтований аналіз абонементів через спільний протокол."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from .models import GymSummary, SubscriptionItem


def filter_active_subscriptions(
    records: Iterable[SubscriptionItem],
    min_visits: int = 30,
) -> list[SubscriptionItem]:
    """Відбирає абонементи з кількістю відвідувань не менше min_visits."""
    return [sub for sub in records if sub.visits >= min_visits]


def unique_clients(records: Iterable[SubscriptionItem]) -> set[str]:
    """Повертає множину унікальних клієнтів."""
    return {sub.client for sub in records}


def revenue_by_plan(records: Iterable[SubscriptionItem]) -> dict[str, float]:
    """Обчислює загальний виторг за кожним тарифним планом."""
    totals: dict[str, float] = {}
    for sub in records:
        totals[sub.plan] = totals.get(sub.plan, 0.0) + sub.price
    return totals


def count_by_plan(records: Iterable[SubscriptionItem]) -> dict[str, int]:
    """Підраховує кількість абонементів за кожним тарифним планом."""
    counts: dict[str, int] = {}
    for sub in records:
        counts[sub.plan] = counts.get(sub.plan, 0) + 1
    return counts


def average_effective_cost(records: Sequence[SubscriptionItem]) -> float:
    """Поліморфно обчислює середню ефективну вартість заняття без перевірки підтипу."""
    if not records:
        return 0.0
    total_cost = sum(sub.effective_visit_cost() for sub in records)
    return total_cost / len(records)


def summarize(
    records: Iterable[SubscriptionItem],
    *metrics: str,
    min_visits: int = 0,
    **labels: str,
) -> dict[str, object]:
    """Обчислює суми вибраних числових властивостей (*args, **kwargs)."""
    selected = [sub for sub in records if sub.visits >= min_visits]
    result: dict[str, object] = {"count": len(selected)}

    allowed_metrics = {"months", "visits", "price"}
    for metric in metrics:
        if metric not in allowed_metrics:
            raise ValueError(f"Невідома метрика: {metric}")
        label = labels.get(metric, metric)
        result[label] = sum(float(getattr(sub, metric)) for sub in selected)

    return result


def make_summary(records: Sequence[SubscriptionItem]) -> GymSummary:
    """Формує незмінний GymSummary для переданої колекції абонементів."""
    if not records:
        return GymSummary(
            count=0,
            unique_clients=0,
            average_visits=0.0,
            total_revenue=0.0,
            average_effective_cost=0.0,
            longest_subscription="немає",
            most_popular_plan="немає",
            most_popular_plan_count=0,
            revenue_by_plan=(),
        )

    total_visits = sum(sub.visits for sub in records)
    total_revenue = sum(sub.price for sub in records)

    longest = max(
        records,
        key=lambda sub: (sub.months, sub.price, sub.client),
    )
    longest_info = f"{longest.client} ({longest.plan}, {longest.months} міс.)"

    plan_counts = count_by_plan(records)
    popular_plan, popular_count = max(
        plan_counts.items(),
        key=lambda item: (item[1], item[0]),
    )

    sorted_revenue = tuple(sorted(revenue_by_plan(records).items()))

    return GymSummary(
        count=len(records),
        unique_clients=len(unique_clients(records)),
        average_visits=total_visits / len(records),
        total_revenue=total_revenue,
        average_effective_cost=average_effective_cost(records),
        longest_subscription=longest_info,
        most_popular_plan=popular_plan,
        most_popular_plan_count=popular_count,
        revenue_by_plan=sorted_revenue,
    )
