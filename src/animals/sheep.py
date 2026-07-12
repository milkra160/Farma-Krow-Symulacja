"""The sheep. Loses satiety slowly; its milk pays off only with a cheese vat."""

from src.animals.livestock import Livestock
from src.config import *
from src import config


class Sheep(Livestock):
    """Like a cow, but loses satiety more slowly and its milk is worth little.

    It pays off only once you own a cheese vat, which turns the milk into cheese.
    Sheep are available only from the shop.
    """

    species = "sheep"
    daily_satiety_loss = SHEEP_DAILY_SATIETY_LOSS

    def __init__(self, id: int, position: tuple, name: str):
        super().__init__(id, position, name)
        self.symbol = "S"

    def product_value(self) -> int:
        # Sold directly it is worth little. A vat turns it into cheese instead.
        if self.is_adult:
            return int(config.SHEEP_MILK_INCOME)
        return 0

    def produces_sheep_milk(self) -> bool:
        # Only an adult sheep gives milk the vat can process.
        return self.is_adult

    def create_offspring(self, id: int, position: tuple, name: str):
        # A sheep's offspring is a lamb. Local import, since Lamb subclasses Sheep.
        from src.animals.lamb import Lamb

        return Lamb(id=id, position=position, name=name)
