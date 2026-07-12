"""The cow. Produces milk once adult."""

from src.animals.livestock import Livestock
from src import config


class Cow(Livestock):
    """A dairy cow. Only adults produce milk."""

    species = "cow"

    def __init__(self, id: int, position: tuple, name: str):
        super().__init__(id, position, name)
        self.symbol = "C"

    def product_value(self) -> int:
        # Only an adult cow produces milk.
        if self.is_adult:
            return int(config.COW_MILK_INCOME)
        return 0

    def milk_value(self) -> int:
        # Alias kept for older code and tests.
        return self.product_value()

    def create_offspring(self, id: int, position: tuple, name: str):
        # A cow's offspring is a calf. Local import, since Calf subclasses Cow.
        from src.animals.calf import Calf

        return Calf(id=id, position=position, name=name)
