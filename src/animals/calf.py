"""A young cow that grows into a Cow."""

from src.animals.cow import Cow


class Calf(Cow):
    """A young cow. It gives no milk until it grows up, when the farm swaps it for a Cow."""

    def __init__(self, id: int, position: tuple[int, int], name: str):
        super().__init__(id, position, name)
        self.symbol = "c"
        self.is_juvenile = True  # stays a juvenile until it grows into a Cow

    def product_value(self):
        return 0

    def to_adult(self):
        # Grow into a full cow, keeping the current state.
        cow = Cow(self.id, self.position, self.name)
        return self._copy_state_to(cow)
