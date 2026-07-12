"""A single cell of the pasture grid."""

from src.animals.livestock import Livestock


class Cell:
    """One square of the pasture. A cell can hold grass and/or a predator."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.has_grass = False
        self.occupied_by = None
        self.has_predator = False
        self.predator = None  # kept so we can call its attack()

    def add_grass(self):
        self.has_grass = True

    def remove_grass(self):
        # Grass is eaten, or cleared when the pasture is reset.
        self.has_grass = False

    def is_free(self) -> bool:
        return self.occupied_by is None

    def enter(self, animal: Livestock) -> str:
        """An animal steps onto the cell. Returns what happened: it died, ate grass,
        or found no grass."""
        self.occupied_by = animal
        animal.grazing_cell = self

        if self.has_predator:
            self.predator.attack(animal)
            return "death"
        if self.has_grass:
            animal.eat()
            return "ate grass"
        return "no grass"
