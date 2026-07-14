from src.weather import Weather
from src.config import RAIN_MULTIPLIER, DROUGHT_MULTIPLIER, SUN_MULTIPLIER


def test_weather_starts_sunny():
    w = Weather()
    assert w.current == "sunny"


def test_next_day_returns_one_of_three_states():
    w = Weather()
    state = w.next_day()
    assert state in ("sunny", "rain", "drought")


def test_rain_multiplier():
    w = Weather()
    w.previous = "rain"
    assert w.grass_multiplier() == RAIN_MULTIPLIER


def test_drought_multiplier():
    w = Weather()
    w.previous = "drought"
    assert w.grass_multiplier() == DROUGHT_MULTIPLIER


def test_sun_multiplier():
    w = Weather()
    w.previous = "sunny"
    assert w.grass_multiplier() == SUN_MULTIPLIER
