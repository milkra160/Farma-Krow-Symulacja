"""A coop-fed hen. Lays eggs and dies only of old age."""

from src.animals.livestock import Livestock
from src.config import *
from src import config


class Hen(Livestock):
    """A hen does not graze; the coop feeds it. It still roams the board, lays
    high-value eggs, and lives a fixed number of days, then dies of old age.

    Events can attack a hen but cannot kill it. Hens come from the shop and do not
    breed, so is_adult stays False.
    """

    species = "hen"

    def __init__(self, id: int, position: tuple, name: str):
        super().__init__(id, position, name)
        self.symbol = "H"  # board glyph for a hen

    def grazes(self) -> bool:
        # Fed from the coop, so it never takes a grass cell. It still roams the board.
        return False

    def product_value(self) -> int:
        # Eggs are steady income, independent of grass, for as long as the hen lives.
        return int(config.EGG_INCOME)

    def death_is_final(self) -> bool:
        # A hen dies only of old age, once past its lifespan. The farm reverts any other death.
        return self.age > config.HEN_LIFESPAN

    def age_one_day(self):
        # A hen does not starve; the coop feeds it. It lives a set number of days,
        # then dies of old age.
        self.age += 1
        if self.age > config.HEN_LIFESPAN:
            self.is_alive = False
            self.died_today = True
