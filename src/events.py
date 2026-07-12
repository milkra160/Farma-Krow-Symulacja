"""Random events and the manager that rolls them each day."""

from abc import ABC, abstractmethod
import random
from src import config


class RandomEvent(ABC):
    """Base class for a random event. Each event can trigger, apply, and revert."""

    def __init__(self):
        self.name = ""
        self.description = ""
        self.duration_days = 1
        self.days_left = 0

    @abstractmethod
    def should_trigger(self, day: int) -> bool:
        pass

    @abstractmethod
    def apply(self, farm) -> str:
        pass

    @abstractmethod
    def revert(self, farm) -> None:
        pass

    def is_blocked(self, farm) -> bool:
        # Whether a farm defence blocks this event (e.g. the antenna blocks UFOs).
        # Nothing blocks by default; a specific event overrides this.
        return False

    def __str__(self) -> str:
        return f"{self.name} (days left: {self.days_left})"


# ------------------------- the events -------------------------


# Valentine's Day: raises the pregnancy chance by 50%, on day 14.
class ValentinesDay(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Valentine's Day 💘"
        self.description = "Pregnancy chance +50% for one day"
        self.duration_days = 1
        self.original_chance = config.PREGNANCY_CHANCE

    def should_trigger(self, day: int) -> bool:
        return day == 14

    def apply(self, farm) -> str:
        self.original_chance = config.PREGNANCY_CHANCE
        config.PREGNANCY_CHANCE *= 1.5
        return f"{self.name} {self.description}"

    def revert(self, farm) -> None:
        config.PREGNANCY_CHANCE = self.original_chance


# -------------------------------------------------------------


# Sudden Drought: cuts the number of grass patches in half for 3 days.
class SuddenDrought(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Sudden Drought ☀️"
        self.description = "Grass patches cut in half for 3 days"
        self.duration_days = 3
        self.original_base = config.BASE_GRASS_PATCHES

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        self.original_base = config.BASE_GRASS_PATCHES
        self.previous_forced = farm.weather.forced_state
        farm.weather.forced_state = "drought"
        config.BASE_GRASS_PATCHES = config.BASE_GRASS_PATCHES // 2
        return f"{self.name} {self.description}"

    def revert(self, farm) -> None:
        config.BASE_GRASS_PATCHES = self.original_base
        farm.weather.forced_state = self.previous_forced


# --------------------------------------------------------------------


# Epidemic: animals fall ill; the whole herd loses 30 satiety.
class Epidemic(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Epidemic"
        self.description = "The whole herd loses 30 satiety at once"
        self.duration_days = 1

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        for animal in farm.animals:
            animal.satiety -= 30
        return f"{self.name} {self.description}"

    def revert(self, farm) -> None:
        pass


# ----------------------------------------------------------------------


# Veterinarian: heals a few animals to full satiety, one-off.
class Veterinarian(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Veterinarian"
        self.description = "A few random animals recover full satiety"
        self.duration_days = 1

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        # Treat only living animals that can go hungry. The coop feeds hens, so satiety
        # does not apply to them and the vet skips them.
        treatable = []
        for animal in farm.animals:
            if animal.is_alive == True and animal.grazes():
                treatable.append(animal)

        if len(treatable) > 0:
            # the vet heals a few animals at once (2-4), but no more than there are
            count = random.randint(2, 4)
            if count > len(treatable):
                count = len(treatable)

            # shuffle the herd and take them without repeats
            random.shuffle(treatable)
            names = []
            for i in range(count):
                animal = treatable[i]
                animal.satiety = config.START_SATIETY
                farm.pending_heals.append(animal)
                names.append(animal.name)

            self.description = f"Full satiety restored for: {', '.join(names)}"
        else:
            self.description = "No animals to treat"
        return self.description

    def revert(self, farm) -> None:
        pass


# --------------------------------------------------------------------


# GMO Feed: milk income up 30% for 5 days.
class GmoFeed(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "GMO Feed"
        self.description = (
            "The farmer fed the cows modified feed and they started producing more "
            "milk: milk income up 30% for 5 days"
        )
        self.duration_days = 5
        self.original_income = config.COW_MILK_INCOME

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        self.original_income = config.COW_MILK_INCOME
        config.COW_MILK_INCOME = config.COW_MILK_INCOME * 1.3
        return f"{self.name} {self.description}"

    def revert(self, farm) -> None:
        config.COW_MILK_INCOME = self.original_income


# --------------------------------------------------------------------


# Meteor Strike: wipes out the simulation completely.
class MeteorStrike(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Meteor Strike"
        self.description = "The meteor wipes out the farm completely. End of simulation."
        self.duration_days = 1

    def should_trigger(self, day: int) -> bool:
        return random.random() < 0.009

    def apply(self, farm) -> str:
        farm.finances.budget = 0.0
        for animal in farm.animals:
            animal.is_alive = False
            animal.died_today = True
        return f"DISASTER! {self.name}: {self.description}"

    def revert(self, farm) -> None:
        pass


# -------------------------------------------------------------


# Easter: one random dead animal comes back to life.
class Easter(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Easter"
        self.description = "A MIRACLE! One random dead animal comes back to life"
        self.duration_days = 1

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        if len(farm.graveyard) > 0:
            revived = random.choice(farm.graveyard)
            farm.graveyard.remove(revived)
            revived.is_alive = True
            revived.died_today = False
            revived.ate_today = False
            revived.grazing_cell = None
            revived.satiety = config.START_SATIETY
            # Resurrection means a fresh life: reset the age, so a hen gets a full new
            # life cycle instead of dying of old age again the next day.
            revived.age = 0
            farm.animals.append(revived)
            farm.resurrections_today.append(revived.name)
            self.description = f"{revived.species} {revived.name} came back to life!"
            return f"{self.name}: {self.description} ({revived.name} rejoins the herd!)"
        else:
            self.description = "A miracle was due, but no animal has died yet"
            return f"{self.name}: {self.description}"

    def revert(self, farm) -> None:
        pass


# -----------------------------------------------------------------


class UfoInvasion(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "UFO Invasion"
        self.description = "Aliens abduct one random cow to run experiments on it"
        self.duration_days = 1

    def should_trigger(self, day: int) -> bool:
        return True

    def is_blocked(self, farm) -> bool:
        # The jamming antenna scrambles the UFO signal; while it runs, no aliens arrive.
        return farm.antenna_days_left > 0

    def apply(self, farm) -> str:
        alive = []
        for animal in farm.animals:
            if animal.is_alive == True:
                alive.append(animal)

        if len(alive) == 0:
            self.description = "The UFO drifted over an empty pasture"
            return self.description

        target = random.choice(alive)
        # A hen is a descendant of dinosaurs, so the aliens get spooked and flee empty-handed.
        if target.species == "hen":
            self.description = (
                "The UFO got spooked by a descendant of dinosaurs and fled, abducting no one"
            )
            return self.description

        target.is_alive = False
        target.died_today = True
        self.description = f"Aliens abducted {target.name}"
        return self.description

    def revert(self, farm) -> None:
        pass


# ------------------------------------------------------------------------


# Forest Ranger: no predators on the pasture for 3 days.
class ForestRanger(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Uncle the Ranger"
        self.description = "The ranger watches the pasture for the weekend. No predators for 3 days"
        self.duration_days = 3
        self.original_chance = config.PREDATOR_CHANCE

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        self.original_chance = farm.predator_chance
        farm.predator_chance = 0.0
        return f"{self.name}: {self.description}"

    def revert(self, farm) -> None:
        farm.predator_chance = self.original_chance


# -------------------------------------------------------------------------


# Rainy Season: nothing but rain for 3 days.
class RainySeason(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Rainy Season"
        self.description = "For the next 3 days the weather is nothing but rain"
        self.duration_days = 3

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        self.previous_forced = farm.weather.forced_state
        farm.weather.forced_state = "rain"
        return f"{self.name}: {self.description}"

    def revert(self, farm) -> None:
        farm.weather.forced_state = self.previous_forced


# --------------------------------------------------------------------


# Jealous Goat: no grass today.
class JealousGoat(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Jealous Goat"
        self.description = "The goat got up early and ate all the grass before the cows: no grass today"
        self.duration_days = 1
        self.original_base = config.BASE_GRASS_PATCHES

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        self.original_base = config.BASE_GRASS_PATCHES
        config.BASE_GRASS_PATCHES = 0
        return f"{self.name}: {self.description}"

    def revert(self, farm) -> None:
        config.BASE_GRASS_PATCHES = self.original_base


# --------------------------------------------------------------


# Miracle on the Oder: an adult instantly gives birth.
class MiracleOnTheOder(RandomEvent):
    def __init__(self):
        super().__init__()
        self.name = "Miracle on the Oder"
        self.description = "A random adult animal instantly gives birth"
        self.duration_days = 1

    def should_trigger(self, day: int) -> bool:
        return True

    def apply(self, farm) -> str:
        adults = []
        for animal in farm.animals:
            if animal.is_alive == True and animal.is_adult == True:
                adults.append(animal)

        if len(adults) > 0:
            mother = random.choice(adults)
            new_id = farm._next_id()
            name = random.choice(config.ANIMAL_NAMES)
            # the mother bears young of her own species (cow -> calf, sheep -> lamb)
            young = mother.create_offspring(new_id, mother.position, name)
            farm.animals.append(young)
            farm.births_today.append(f"{name} (mother: {mother.name})")
            self.description = f"A young {name} was born (mother: {mother.name})"
        else:
            self.description = "No adult animals able to give sudden birth"
        return self.description

    def revert(self, farm) -> None:
        pass


# ----------------------------------------------------------------------------
# The manager owns the pool of random events and their life cycle.
# The pool is a list of classes we pick from and instantiate.


class EventManager:
    def __init__(self, pool=None, event_chance: float = config.EVENT_CHANCE):
        self.event_count = 0
        if pool is None:
            pool = [
                SuddenDrought,
                Epidemic,
                Veterinarian,
                MeteorStrike,
                GmoFeed,
                Easter,
                UfoInvasion,
                ForestRanger,
                RainySeason,
                JealousGoat,
                MiracleOnTheOder,
            ]
        self.pool = pool
        self.active = []
        self.event_chance = event_chance

    def update(self, farm, day: int) -> list:
        # Count down active events; revert and drop the ones that have expired.
        still_active = []
        messages = []
        for event in self.active:
            event.days_left -= 1
            if event.days_left <= 0:
                event.revert(farm)
            else:
                still_active.append(event)
                messages.append(f"{event.name} (days left: {event.days_left})")
        self.active = still_active

        # is any long-running event still going
        long_event_running = False
        for event in self.active:
            if event.duration_days > 1:
                long_event_running = True

        # Valentine's Day is a calendar event: a 50% chance exactly on day 14.
        if day == 14 and random.random() < 0.5:
            valentines = ValentinesDay()
            valentines.days_left = valentines.duration_days
            valentines.apply(farm)
            self.active.append(valentines)
            messages.append(f"{valentines.name}: {valentines.description}")

        if random.random() < self.event_chance:
            new_event = random.choice(self.pool)()
            blocked = new_event.duration_days > 1 and long_event_running
            if new_event.is_blocked(farm):
                # a farm defence (the antenna) kept the event out; report it
                messages.append(
                    f"The antenna jammed the signal; {new_event.name} did not happen"
                )
            elif new_event.should_trigger(day) and not blocked:
                new_event.days_left = new_event.duration_days
                new_event.apply(farm)
                self.event_count += 1
                self.active.append(new_event)
                messages.append(f"{new_event.name}: {new_event.description}")

        return messages
