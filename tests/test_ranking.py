import os
from src.ranking import Ranking


def result(name, days):
    return {
        "farm_name": name,
        "date": "2026-06-08",
        "days_survived": days,
        "max_budget": 100,
        "max_herd": 5,
        "end_reason": "bankruptcy",
        "start_params": {},
    }


def make_ranking():
    file = "/tmp/ranking_test.json"
    if os.path.exists(file):
        os.remove(file)
    return Ranking(file=file)


def test_empty_ranking_when_no_file():
    r = make_ranking()
    assert r.load() == []


def test_save_and_sort_descending():
    r = make_ranking()
    r.save_result(result("first", 12))
    r.save_result(result("second", 46))
    r.save_result(result("third", 58))
    ranking = r.load()
    assert [w["days_survived"] for w in ranking] == [58, 46, 12]
