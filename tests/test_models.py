"""Поведінкові тести класів, @property, @dataclass, підтипів та Protocol."""

from dataclasses import FrozenInstanceError

import pytest

from kzp_lab06.analysis import average_effective_cost
from kzp_lab06.models import (
    GymSubscription,
    GymSummary,
    PremiumSubscription,
    StandardSubscription,
    SubscriptionItem,
)


def test_property_validation_and_setter() -> None:
    sub = StandardSubscription("Марія", "Standard Gym", 3, 24, 3000.0)
    assert sub.visits == 24

    sub.visits = 0
    assert sub.visits == 0

    with pytest.raises(ValueError, match="відвідувань"):
        sub.visits = -1

    with pytest.raises(ValueError, match="Ціна"):
        sub.price = 0.0

    with pytest.raises(ValueError, match="Тривалість"):
        sub.months = 0


def test_special_methods_str_repr_eq_and_ordering() -> None:
    s1 = StandardSubscription("Олексій", "Standard", 3, 30, 3000.0)
    s2 = StandardSubscription("Олексій", "Standard", 3, 30, 3000.0)
    s3 = StandardSubscription("Богдан", "Standard", 6, 60, 5500.0)

    assert s1 == s2
    assert s1 != "не об'єкт"
    assert s1 < s3
    assert "Олексій" in str(s1)
    assert "StandardSubscription(" in repr(s1)


def test_subtypes_and_duck_typed_protocol() -> None:
    std = StandardSubscription("Марія", "Standard", 3, 30, 3000.0)
    prem = PremiumSubscription("Олексій", "Full Unlimited", 12, 100, 11000.0, spa_hours=20)

    assert isinstance(std, SubscriptionItem)
    assert isinstance(prem, SubscriptionItem)
    assert std.effective_visit_cost() == pytest.approx(100.0)
    assert prem.effective_visit_cost() == pytest.approx(100.0)

    # Перевірка качиної типізації (сторонній клас без успадкування від GymSubscription)
    class GuestPass:
        client = "Гість"
        plan = "Guest"
        months = 1
        visits = 1
        price = 200.0

        def effective_visit_cost(self) -> float:
            return 200.0

    items: list[SubscriptionItem] = [std, prem, GuestPass()]
    assert average_effective_cost(items) == pytest.approx((100.0 + 100.0 + 200.0) / 3)


def test_frozen_summary_dataclass() -> None:
    summary = GymSummary(
        count=1,
        unique_clients=1,
        average_visits=30.0,
        total_revenue=3000.0,
        average_effective_cost=100.0,
        longest_subscription="Марія (Standard, 3 міс.)",
        most_popular_plan="Standard",
        most_popular_plan_count=1,
        revenue_by_plan=(("Standard", 3000.0),),
    )

    with pytest.raises(FrozenInstanceError):
        summary.count = 5  # type: ignore[misc]


def test_base_class_effective_cost_requires_override() -> None:
    base = GymSubscription("Тест", "Base", 1, 10, 1000.0)
    with pytest.raises(NotImplementedError):
        base.effective_visit_cost()
