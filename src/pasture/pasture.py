"""The pasture: a 2D grid of cells the animals graze on."""

import random
from src.pasture.cell import Cell


class Pasture:
    """A 2D board built from cells."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        # build the grid
        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x, y))
            self.grid.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        # the grid is indexed [y][x]
        return self.grid[y][x]

    def scatter_grass(self, patch_count: int) -> list:
        """Grow grass on a set of unique cells. Returns the chosen positions."""
        all_positions = []
        for y in range(self.height):
            for x in range(self.width):
                all_positions.append((x, y))

        patch_count = max(0, min(patch_count, len(all_positions)))
        # random.sample avoids repeats; random.choice could pick the same cell twice
        chosen = random.sample(all_positions, patch_count)
        for x, y in chosen:
            self.get_cell(x, y).add_grass()
        return chosen

    def grass_cells(self) -> list:
        """All cells that currently have grass."""
        result = []
        for row in self.grid:
            for cell in row:
                if cell.has_grass:
                    result.append(cell)
        return result

    def clear(self):
        # Reset every cell back to its starting state.
        for row in self.grid:
            for cell in row:
                cell.remove_grass()
                cell.occupied_by = None
                cell.has_predator = False
                cell.predator = None

    def place_predators(self, predators: list):
        cells = self.grass_cells()  # a predator only stands on grass
        # pick as many grass cells as there are predators, without repeats
        chosen = random.sample(cells, len(predators))
        for i in range(len(predators)):
            cell = chosen[i]
            cell.has_predator = True
            cell.predator = predators[i]
            predators[i].position = (cell.x, cell.y)

    # An animal that has eaten should move to a free cell next to its own (one of four).
    # The leading underscore marks this as internal; other classes should not call it.
    def _random_neighbor(self, x: int, y: int) -> tuple:
        # the four cells around this one: up, right, down, left
        neighbors = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        free = []
        for nx, ny in neighbors:
            # the neighbor must fit on the board
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.get_cell(nx, ny).is_free():
                    free.append((nx, ny))
        if len(free) > 0:
            return random.choice(free)
        # with no free neighbor the animal stays on the same cell
        return (x, y)

    def assign_grazing_cells(self, animals: list):
        """Seat living animals on free grass cells; each one eats if it gets a cell."""
        alive = []
        for animal in animals:
            if animal.is_alive:
                alive.append(animal)

        # collect free grass cells and shuffle them
        free_cells = []
        for cell in self.grass_cells():
            if cell.is_free():
                free_cells.append(cell)
        random.shuffle(free_cells)

        # hand out cells while they last; each animal gets one
        for i in range(len(alive)):
            animal = alive[i]
            if i < len(free_cells):
                cell = free_cells[i]
                cell.enter(animal)  # sets the grazing cell; the animal eats or not
                animal.display_pos = self._random_neighbor(cell.x, cell.y)
            else:
                # no free cell: the animal does not eat and stands anywhere
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                animal.display_pos = (x, y)
