"""Base class for every animal in the simulation."""

from abc import ABC, abstractmethod


class Animal(ABC):
    """Common base for livestock and predators.

    Abstract so it cannot be instantiated on its own, and so every subclass has to
    implement move().
    """

    def __init__(self, id: int, position: tuple[int, int]):
        self.id = id
        self.position = position  # (x, y) in screen coordinates
        self.is_alive = True
        self.symbol = "?"  # base glyph; each species sets its own

    @abstractmethod
    def move(self):
        """Advance the animal's position. Each species does this differently."""
