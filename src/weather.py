"""The weather: rolls each day's conditions and drives how much grass grows."""

import random
from src.config import *


class Weather:
    # Possible weather states; one tuple shared by every instance.
    WEATHER_STATES = ("sunny", "rain", "drought")

    def __init__(self):
        # starting state
        self.current = "sunny"
        self.previous = "sunny"
        self.forced_state = None
        self.history = []

    def next_day(self):
        """Roll today's weather (unless an event forces it) and record yesterday's."""
        self.previous = self.current
        self.history.append(self.previous)
        if self.forced_state is not None:
            self.current = self.forced_state
        else:
            self.current = random.choice(self.WEATHER_STATES)
        return self.current

    def grass_multiplier(self):
        # Grass grows based on yesterday's weather, so there is a one-day delay.
        if self.previous == "rain":
            return RAIN_MULTIPLIER
        if self.previous == "drought":
            return DROUGHT_MULTIPLIER
        return SUN_MULTIPLIER

    def __str__(self):
        return f"Weather: {self.current}"
