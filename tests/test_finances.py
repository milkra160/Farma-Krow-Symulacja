from src.config import START_BUDGET
from src.finances import Finances


def test_is_bankrupt_when_budget_zero():
    f = Finances()
    f.budget = 0
    assert f.is_bankrupt()


def test_is_bankrupt_when_budget_negative():
    f = Finances()
    f.budget = -100
    assert f.is_bankrupt()


def test_not_bankrupt_when_budget_positive():
    f = Finances()
    f.budget = 100
    assert not f.is_bankrupt()


def test_bankrupt_flag_in_dict():
    f = Finances()
    f.budget = 0
    state = f.settle_day(0, 50, 1)
    assert state["bankrupt"]


def test_starting_budget():
    f = Finances()
    assert f.budget == START_BUDGET


def test_settle_day_for_profit():
    f = Finances()
    f.budget = 100
    f.settle_day(50, 20, 1)
    assert f.budget == 130


def test_settle_day_for_loss():
    f = Finances()
    f.budget = 100
    f.settle_day(10, 40, 1)
    assert f.budget == 70


def test_settle_day_returns_dict():
    f = Finances()
    f.budget = 100
    state = f.settle_day(50, 20, 1)
    assert state["income"] == 50
    assert state["cost"] == 20
    assert state["balance"] == 30
    assert state["bankrupt"] is False
    assert state["budget"] == 130


def test_settle_day_records_history():
    f = Finances()
    f.settle_day(50, 20, 1)
    f.settle_day(10, 5, 2)
    assert f.history[0]["day"] == 1
    assert f.history[1]["day"] == 2
