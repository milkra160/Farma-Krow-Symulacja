"""A young sheep that grows into a Sheep."""

from src.animals.sheep import Sheep


class Lamb(Sheep):
    """A young sheep. It gives no milk until it grows up into a Sheep."""

    def __init__(self, id: int, position: tuple[int, int], name: str):
        super().__init__(id, position, name)
        self.symbol = "l"
        self.is_juvenile = True  # stays a juvenile until it grows into a Sheep

    def product_value(self):
        return 0

    def to_adult(self):
        # Grow into a full sheep, keeping the current state.
        sheep = Sheep(self.id, self.position, self.name)
        return self._copy_state_to(sheep)
