"""Тести аналітичних функцій та форматування звіту."""

import pytest

from kzp_lab06.analysis import (
    filter_active_subscriptions,
    make_summary,
    summarize,
    unique_clients,
)
from kzp_lab06.models import GymSubscription, PremiumSubscription, StandardSubscription
from kzp_lab06.reporting import format_report


@pytest.fixture
def sample_records() -> list[GymSubscription]:
    return [
        PremiumSubscription("Олексій", "Full Unlimited", 12, 120, 12000.0, spa_hours=24),
        StandardSubscription("Марія", "Standard Gym", 3, 24, 3200.0),
        StandardSubscription("Олексій", "Standard Gym", 6, 50, 5800.0),
    ]


def test_filtering_and_duplicates(sample_records: list[GymSubscription]) -> None:
    active = filter_active_subscriptions(sample_records, min_visits=50)
    assert len(active) == 2
    assert unique_clients(sample_records) == {"Олексій", "Марія"}


def test_summarize_with_args_kwargs_and_default(sample_records: list[GymSubscription]) -> None:
    res = summarize(
        sample_records,
        "price",
        "visits",
        min_visits=50,
        price="Виторг",
        visits="Відвідування",
    )
    assert res == {
        "count": 2,
        "Виторг": pytest.approx(17800.0),
        "Відвідування": pytest.approx(170.0),
    }

    with pytest.raises(ValueError, match="Невідома метрика"):
        summarize(sample_records, "unknown_field")


def test_deterministic_report_order(sample_records: list[GymSubscription]) -> None:
    summary = make_summary(sample_records)
    report = format_report(summary)
    assert "Full Unlimited: 12000.00 грн" in report
    assert "Standard Gym: 9000.00 грн" in report
    assert report.index("Full Unlimited") < report.index("Standard Gym")
