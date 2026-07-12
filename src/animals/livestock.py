"""Base class for farm animals (cow, sheep, hen)."""

import random
from src.animals.animal import Animal
from src.config import *
from src import config


class Livestock(Animal):
    """Shared behaviour for farm animals.

    Handles the daily life cycle (feeding, hunger, ageing, maturing) and
    reproduction. A new species is added as a subclass, not by changing the
    simulation.
    """

    # Species name. Used in statistics and to group animals in the log.
    species = "animal"
    # Satiety lost per day. Sheep override this with a smaller value.
    daily_satiety_loss = DAILY_SATIETY_LOSS

    def __init__(self, id: int, position: tuple[int, int], name: str):
        super().__init__(id, position)
        self.name = name
        self.age = 0
        self.satiety = START_SATIETY
        self.is_adult = False
        # True for a calf or lamb until it grows up
        self.is_juvenile = False

        # pregnancy state
        self.is_pregnant = False
        self.days_to_birth = 0

        self.ate_today = False
        self.died_today = False

        # used when placing the animal on the pasture
        self.grazing_cell = None
        self.display_pos = (0, 0)

    def age_one_day(self):
        """One day of ageing: raise age and hunger, mark adulthood, starve at zero."""
        self.age += 1
        self.satiety -= self.daily_satiety_loss
        if self.age >= ADULT_AGE:
            self.is_adult = True
        if self.satiety <= 0:
            self.is_alive = False
            self.died_today = True

    def eat(self):
        """Eat grass and raise satiety up to the maximum."""
        # min() keeps satiety from going above the cap.
        self.satiety = min(self.satiety + SATIETY_PER_MEAL, START_SATIETY)
        self.ate_today = True

    def is_hungry(self) -> bool:
        """True when satiety has dropped into the hungry range."""
        return self.satiety < 40

    def product_value(self) -> int:
        """Daily income from this animal (milk, eggs). Zero here; each species overrides it."""
        return 0

    def produces_sheep_milk(self) -> bool:
        """Whether this animal supplies the cheese vat. Only adult sheep return True."""
        return False

    def grazes(self) -> bool:
        """Whether the animal feeds on grass. Hens return False; they eat from the coop."""
        return True

    def death_is_final(self) -> bool:
        """Whether a death should stick. Hens override this so only old age kills them,
        and the farm reverts any other death."""
        return True

    def reset_for_day(self):
        """Reset the per-day flags and free the grazing cell."""
        self.ate_today = False
        self.died_today = False
        self.grazing_cell = None

    def move(self):
        # Livestock stays put. Required by the Animal base class.
        pass

    # --- reproduction (shared by every breeding species) ---

    def maybe_conceive(self):
        """A well-fed adult may become pregnant."""
        if self.is_adult and not self.is_pregnant and self.satiety > 60:
            if random.random() < config.PREGNANCY_CHANCE:
                self.is_pregnant = True
                self.days_to_birth = GESTATION_DAYS

    def advance_pregnancy(self) -> bool:
        """Count down the pregnancy. Returns True on the birth day."""
        if self.is_pregnant:
            self.days_to_birth -= 1
            if self.days_to_birth == 0:
                self.is_pregnant = False
                return True
        return False

    def create_offspring(self, id: int, position: tuple, name: str):
        """Return a newborn of the same species (cow to calf, sheep to lamb).

        Each breeding species overrides this.
        """
        raise NotImplementedError

    def to_adult(self):
        """Return the adult form. Adults return themselves; a calf or lamb overrides
        this to turn into an adult once it grows up."""
        return self

    def _copy_state_to(self, adult):
        """Copy shared state onto the adult produced when a juvenile grows up."""
        adult.age = self.age
        adult.satiety = self.satiety
        adult.is_adult = True
        adult.is_alive = self.is_alive
        adult.is_pregnant = self.is_pregnant
        adult.days_to_birth = self.days_to_birth
        adult.display_pos = self.display_pos
        adult.grazing_cell = self.grazing_cell
        adult.ate_today = self.ate_today
        adult.died_today = self.died_today
        return adult
