import io
import os
from contextlib import redirect_stdout
from src.simulation import Simulation
from src.ranking import Ranking
from src.visualization import Visualization


def params(max_days=5, cows=4, budget=1000.0):
    return {
        "farm_name": "Test",
        "starting_cows": cows,
        "starting_budget": budget,
        "predator_chance": 0.0,  # turn off randomness for the test
        "max_predators": 1,
        "max_days": max_days,
        "event_chance": 0.0,
    }


def make_simulation():
    s = Simulation()
    s.visualization = Visualization(colors=False)
    file = "/tmp/ranking_simulation_test.json"
    if os.path.exists(file):
        os.remove(file)
    s.ranking = Ranking(file=file)
    return s


def run_simulation(s):  # run through the whole simulation without cluttering the screen
    s.auto_mode = True
    output = io.StringIO()
    with redirect_stdout(output):
        s.main_loop()


def test_simulation_ends_when_time_runs_out():
    s = make_simulation()
    s._prepare(params(max_days=5))
    run_simulation(s)
    assert s.farm.day == 5
    results = s.ranking.load()
    assert len(results) == 1
    assert results[0]["end_reason"] == "time is up"


def test_bankruptcy_ends_the_simulation():
    s = make_simulation()
    s._prepare(params(max_days=100, cows=1, budget=60.0))
    run_simulation(s)
    assert s.farm.finances.is_bankrupt()
    assert s.ranking.load()[0]["end_reason"] == "bankruptcy"


def test_run_day_increments_the_day():
    s = make_simulation()
    s._prepare(params(max_days=100))
    output = io.StringIO()
    with redirect_stdout(output):
        keep_going = s.run_day()
    assert s.farm.day == 1
    assert keep_going is True
