"""The farm's finances: budget tracking and a per-day history."""

from src.config import *


class Finances:
    """Tracks the farm budget and records where it stood each day."""

    def __init__(self):
        self.budget = START_BUDGET
        self.history = []

    def settle_day(self, income: float, cost: float, day: int):
        """Settle one day: balance = income - cost, update the budget, log the result."""
        balance = income - cost
        self.budget += balance

        # snapshot shown in the end-of-day summary
        day_finances = {
            "budget": float(self.budget),
            "income": float(income),
            "cost": float(cost),
            "balance": float(balance),
            "bankrupt": self.is_bankrupt(),
        }

        self.history.append({"day": day, "state": day_finances})
        return day_finances

    def is_bankrupt(self) -> bool:
        # The farm goes bankrupt when the budget reaches zero or below.
        return self.budget <= 0

    def spend(self, amount: float) -> bool:
        """Spend money in the shop. Returns True on success.

        We do not let the budget drop to zero, since that would mean instant
        bankruptcy, so a purchase must leave something behind.
        """
        if amount >= self.budget:
            return False
        self.budget -= amount
        return True
