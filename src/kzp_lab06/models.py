"""Об'єктна модель абонементів тренажерного залу (Варіант 20)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class SubscriptionItem(Protocol):
    """Протокол абонемента з можливістю розрахунку ефективної вартості заняття."""

    @property
    def client(self) -> str:
        """Ім'я клієнта."""
        ...

    @property
    def plan(self) -> str:
        """Назва тарифного плану."""
        ...

    @property
    def months(self) -> int:
        """Тривалість абонемента в місяцях."""
        ...

    @property
    def visits(self) -> int:
        """Кількість відвідувань."""
        ...

    @property
    def price(self) -> float:
        """Вартість абонемента."""
        ...

    def effective_visit_cost(self) -> float:
        """Повертає ефективну вартість одного відвідування."""
        ...


class GymSubscription:
    """Базовий клас абонемента тренажерного залу з контрольованими властивостями."""

    def __init__(
        self,
        client: str,
        plan: str,
        months: int,
        visits: int,
        price: float,
    ) -> None:
        self.client = client
        self.plan = plan
        self.months = months
        self.visits = visits
        self.price = price

    @property
    def client(self) -> str:
        return self._client

    @client.setter
    def client(self, value: str) -> None:
        cleaned = value.strip() if isinstance(value, str) else ""
        if not cleaned:
            raise ValueError("Ім'я клієнта не може бути порожнім")
        self._client = cleaned

    @property
    def plan(self) -> str:
        return self._plan

    @plan.setter
    def plan(self, value: str) -> None:
        cleaned = value.strip() if isinstance(value, str) else ""
        if not cleaned:
            raise ValueError("Назва тарифного плану не може бути порожньою")
        self._plan = cleaned

    @property
    def months(self) -> int:
        return self._months

    @months.setter
    def months(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError("Тривалість абонемента має бути цілим числом >= 1")
        self._months = value

    @property
    def visits(self) -> int:
        return self._visits

    @visits.setter
    def visits(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Кількість відвідувань не може бути від'ємною")
        self._visits = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Ціна має бути числом")
        numeric = float(value)
        if not math.isfinite(numeric) or numeric <= 0.0:
            raise ValueError("Ціна має бути скінченним додатним числом")
        self._price = numeric

    def effective_visit_cost(self) -> float:
        """Базовий розрахунок ефективної вартості відвідування."""
        raise NotImplementedError("Підтипи мають реалізувати effective_visit_cost()")

    def __str__(self) -> str:
        return (
            f"{self.client} — {self.plan} "
            f"({self.months} міс., {self.visits} відв., {self.price:.2f} грн)"
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(client={self.client!r}, plan={self.plan!r}, "
            f"months={self.months!r}, visits={self.visits!r}, price={self.price!r})"
        )

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        assert isinstance(other, GymSubscription)
        return (
            self.client == other.client
            and self.plan == other.plan
            and self.months == other.months
            and self.visits == other.visits
            and math.isclose(self.price, other.price, rel_tol=1e-9)
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, GymSubscription):
            return NotImplemented
        return (self.months, self.price, self.client) < (
            other.months,
            other.price,
            other.client,
        )


class StandardSubscription(GymSubscription):
    """Стандартний абонемент без додаткових SPA-годин."""

    def effective_visit_cost(self) -> float:
        return self.price if self.visits == 0 else self.price / self.visits


class PremiumSubscription(GymSubscription):
    """Преміум-абонемент із включеними SPA-годинами."""

    def __init__(
        self,
        client: str,
        plan: str,
        months: int,
        visits: int,
        price: float,
        spa_hours: int = 12,
    ) -> None:
        super().__init__(client, plan, months, visits, price)
        self.spa_hours = spa_hours

    @property
    def spa_hours(self) -> int:
        return self._spa_hours

    @spa_hours.setter
    def spa_hours(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Кількість SPA-годин не може бути від'ємною")
        self._spa_hours = value

    def effective_visit_cost(self) -> float:
        effective_sessions = self.visits + (self.spa_hours * 0.5)
        return self.price if effective_sessions == 0 else self.price / effective_sessions

    def __repr__(self) -> str:
        return (
            f"PremiumSubscription(client={self.client!r}, plan={self.plan!r}, "
            f"months={self.months!r}, visits={self.visits!r}, "
            f"price={self.price!r}, spa_hours={self.spa_hours!r})"
        )

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        assert isinstance(other, PremiumSubscription)
        return super().__eq__(other) and self.spa_hours == other.spa_hours


@dataclass(frozen=True)
class GymSummary:
    """Незмінний підсумок аналізу абонементів для звіту."""

    count: int
    unique_clients: int
    average_visits: float
    total_revenue: float
    average_effective_cost: float
    longest_subscription: str
    most_popular_plan: str
    most_popular_plan_count: int
    revenue_by_plan: tuple[tuple[str, float], ...]
