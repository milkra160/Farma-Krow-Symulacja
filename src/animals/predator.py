"""The predator. Kills grazing animals that enter its cell."""

from src.animals.animal import Animal


class Predator(Animal):
    """Kills any animal that steps onto its grass cell. Keeps the herd from growing
    without limit."""

    def __init__(self, id: int, position: tuple[int, int]):
        super().__init__(id, position)
        self.symbol = "!"

    def attack(self, animal) -> bool:
        # Kill the animal that entered this predator's cell.
        animal.is_alive = False
        animal.died_today = True
        return True

    def move(self):
        # A predator stays put. Required by the Animal base class.
        pass
