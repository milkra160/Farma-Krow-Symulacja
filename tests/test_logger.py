from src.logger import Logger


def sample_log():
    return {
        "day": 5,
        "weather": "rain",
        "births": ["Charlie"],
        "dead": ["Mark", "Bart"],
        "death_causes": {"Mark": "hunger", "Bart": "predator"},
        "fed": ["Spotty", "Andrew"],
        "hungry": ["Spaniard"],
        "predators": [(3, 4)],
        "animal_states": [
            {
                "symbol": "C",
                "species": "cow",
                "name": "Spotty",
                "satiety": 80,
                "ate": True,
                "is_alive": True,
            },
            {
                "symbol": "C",
                "species": "cow",
                "name": "Andrew",
                "satiety": 70,
                "ate": True,
                "is_alive": True,
            },
            {
                "symbol": "C",
                "species": "cow",
                "name": "Spaniard",
                "satiety": 20,
                "ate": False,
                "is_alive": True,
            },
        ],
        "grass_patches": [(1, 1), (2, 2)],
        "finances": {
            "budget": 120,
            "income": 40,
            "cost": 50,
            "balance": -10,
            "bankrupt": False,
        },
        "events": ["Rainy Season: rain for a few days"],
    }


def test_log_contains_weather_and_header(capsys):
    Logger().print_log(sample_log())
    result = capsys.readouterr().out
    assert "DAY 5" in result
    assert "rain" in result


def test_log_shows_death_with_cause(capsys):
    Logger().print_log(sample_log())
    result = capsys.readouterr().out
    assert "Mark" in result
    assert "hunger" in result
    assert "Bart" in result
    assert "predator" in result


def test_log_prints_herd_statistics(capsys):
    Logger().print_log(sample_log())
    result = capsys.readouterr().out
    assert "LIVING COWS: 3" in result  # 3 living cows
    assert "fed: 2" in result  # 2 fed
    assert "hungry: 1" in result  # 1 hungry


def test_log_without_events_shows_none(capsys):
    log = sample_log()
    log["events"] = []
    Logger().print_log(log)
    result = capsys.readouterr().out
    assert "RANDOM EVENTS: none" in result


def test_log_prints_final_summary(capsys):
    Logger().print_final_summary(5, "bankruptcy", {"budget": 0})
    result = capsys.readouterr().out
    assert "END OF SIMULATION" in result
    assert "bankruptcy" in result
