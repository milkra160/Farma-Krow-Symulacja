from src.config import SATIETY_PER_MEAL
from src.pasture.cell import Cell
from src.pasture.pasture import Pasture
from src.animals.predator import Predator

from src.animals.cow import Cow


# cell ******************************


def test_cell_starts_empty():
    c = Cell(x=2, y=3)
    assert c.x == 2
    assert c.y == 3
    assert c.has_grass is False
    assert c.is_free() is True


def test_add_grass():
    c = Cell(x=2, y=3)
    c.add_grass()
    assert c.has_grass is True


def test_cell_not_free_after_entering():
    c = Cell(x=2, y=3)
    cow = Cow(id=1, position=(2, 3), name="Spotty")
    c.enter(cow)
    assert c.is_free() is False
    assert cow.grazing_cell == c


def test_cow_enters_a_cell_and_eats():
    c = Cell(x=0, y=0)
    c.add_grass()
    cow = Cow(id=1, position=(0, 0), name="Spotty")
    cow.satiety = 50
    result = c.enter(cow)

    assert result == "ate grass"
    assert cow.ate_today is True
    assert cow.satiety == 50 + SATIETY_PER_MEAL
    assert cow.is_alive is True


def test_cow_enters_without_grass():
    c = Cell(x=0, y=0)
    cow = Cow(id=1, position=(0, 0), name="Spotty")
    result = c.enter(cow)

    assert result == "no grass"
    assert cow.ate_today is False
    assert cow.is_alive is True


def test_cow_enters_with_a_predator_and_dies():
    c = Cell(x=0, y=0)
    cow = Cow(id=1, position=(0, 0), name="Spotty")
    predator = Predator(id=89, position=(0, 0))
    c.has_predator = True
    c.predator = predator
    result = c.enter(cow)

    assert result == "death"
    assert cow.is_alive is False
    assert cow.died_today is True


# Pasture *******************************************
def test_pasture_has_dimensions():
    p = Pasture(5, 3)
    assert p.height == 3
    assert p.width == 5


def test_pasture_builds_a_grid_of_cells():
    p = Pasture(5, 3)
    assert len(p.grid) == 3  # number of rows = height
    assert len(p.grid[0]) == 5  # number of columns = width
    assert isinstance(p.grid[0][0], Cell)


def test_get_cell_returns_the_right_cell():
    p = Pasture(5, 3)
    c = p.get_cell(2, 1)
    assert c.x == 2
    assert c.y == 1


def test_scatter_grass_places_the_requested_amount():
    p = Pasture(5, 5)
    positions = p.scatter_grass(7)
    assert len(positions) == 7
    assert len(p.grass_cells()) == 7


def test_scatter_grass_positions_are_unique():
    p = Pasture(5, 5)
    positions = p.scatter_grass(10)
    assert len(set(positions)) == 10


def test_grass_cells_have_grass():
    p = Pasture(4, 4)
    p.scatter_grass(3)
    cells = p.grass_cells()
    assert len(cells) == 3
    for c in cells:
        assert c.has_grass is True


def test_scatter_grass_on_the_right_cells():
    p = Pasture(4, 4)
    positions = p.scatter_grass(5)
    for x, y in positions:
        assert p.get_cell(x, y).has_grass is True


def test_remove_grass():
    c = Cell(x=0, y=0)
    c.add_grass()
    c.remove_grass()
    assert c.has_grass is False


def test_clear_removes_grass():
    p = Pasture(5, 5)
    p.scatter_grass(5)
    p.clear()
    assert len(p.grass_cells()) == 0


def test_clear_removes_grass_from_cells():
    p = Pasture(5, 5)
    c = Cow(id=1, position=(0, 0), name="Spotty")
    p.get_cell(0, 0).enter(c)
    p.clear()
    assert p.get_cell(0, 0).is_free() is True


def test_clear_removes_predators():
    p = Pasture(5, 5)
    c = p.get_cell(0, 0)
    c.has_predator = True
    c.predator = Predator(id=89, position=(0, 0))
    p.clear()
    assert p.get_cell(0, 0).has_predator is False
    assert p.get_cell(0, 0).predator is None


# helper for the tests
def count_predators(pasture):
    total = 0
    for row in pasture.grid:
        for cell in row:
            if cell.has_predator:
                total += 1
    return total


def test_place_predators_puts_them_on_grass():
    p = Pasture(5, 5)
    p.scatter_grass(10)
    d1 = Predator(id=1, position=(0, 0))
    d2 = Predator(id=2, position=(0, 0))
    p.place_predators([d1, d2])

    assert count_predators(p) == 2
    for row in p.grid:
        for cell in row:
            if cell.has_predator:
                assert cell.has_grass is True
                assert cell.predator is not None


def test_place_predators_on_different_cells():
    p = Pasture(5, 5)
    p.scatter_grass(10)
    predators = [
        Predator(id=1, position=(0, 0)),
        Predator(id=2, position=(0, 0)),
        Predator(id=3, position=(0, 0)),
    ]
    p.place_predators(predators)
    assert count_predators(p) == 3


def test_place_predators_with_an_empty_list():
    p = Pasture(5, 5)
    p.scatter_grass(10)
    p.place_predators([])
    assert count_predators(p) == 0


# helper
def occupy(p, x, y):
    p.get_cell(x, y).enter(Cow(id=1, position=(0, 0), name="X"))


def test_random_neighbor_returns_a_free_neighbor():
    p = Pasture(5, 5)
    result = p._random_neighbor(2, 2)
    assert result in [(2, 1), (3, 2), (2, 3), (1, 2)]


def test_random_neighbor_skips_occupied_cells():
    p = Pasture(5, 5)
    occupy(p, 2, 1)  # up
    occupy(p, 2, 3)  # down
    occupy(p, 1, 2)  # left
    assert p._random_neighbor(2, 2) == (3, 2)  # the only free one (right)


def test_random_neighbor_with_no_free_cells_returns_the_same_cell():
    p = Pasture(5, 5)
    occupy(p, 2, 1)
    occupy(p, 2, 3)
    occupy(p, 1, 2)
    occupy(p, 3, 2)
    assert p._random_neighbor(2, 2) == (2, 2)


def test_random_neighbor_stays_on_the_board():
    p = Pasture(5, 5)
    result = p._random_neighbor(0, 0)
    assert result in [(1, 0), (0, 1)]


def test_assign_grazing_cells_feeds_living_cows():
    p = Pasture(5, 5)
    p.scatter_grass(10)
    c1 = Cow(id=1, position=(0, 0), name="X")
    c2 = Cow(id=2, position=(0, 0), name="Y")
    p.assign_grazing_cells([c1, c2])
    assert c1.grazing_cell is not None
    assert c2.grazing_cell is not None
    assert c1.ate_today is True
    assert c2.ate_today is True


def test_assign_grazing_cells_with_few_cells():
    p = Pasture(5, 5)
    p.scatter_grass(1)
    c1 = Cow(id=1, position=(0, 0), name="X")
    c2 = Cow(id=2, position=(0, 0), name="Y")
    p.assign_grazing_cells([c1, c2])
    fed = 0
    if c1.ate_today:
        fed += 1
    if c2.ate_today:
        fed += 1
    assert fed == 1


def test_assign_grazing_cells_gives_a_display_pos_on_the_board():
    p = Pasture(5, 5)
    p.scatter_grass(5)
    cows = []
    for i in range(8):  # more cows than cells
        cows.append(Cow(id=i, position=(0, 0), name="X"))
    p.assign_grazing_cells(cows)
    for c in cows:  # every cow must have a spot on the board
        x, y = c.display_pos
        assert 0 <= x < 5  # board range
        assert 0 <= y < 5


def test_assign_grazing_cells_skips_dead_cows():
    p = Pasture(5, 5)
    p.scatter_grass(5)
    dead = Cow(id=1, position=(0, 0), name="X")
    dead.is_alive = False
    p.assign_grazing_cells([dead])
    assert dead.grazing_cell is None
    assert dead.ate_today is False


def test_assign_grazing_cells_when_a_cow_dies_to_a_predator():
    p = Pasture(5, 5)
    p.scatter_grass(1)
    cell = p.grass_cells()[0]
    cell.has_predator = True
    cell.predator = Predator(id=6, position=(cell.x, cell.y))
    cow = Cow(id=1, position=(0, 0), name="X")
    p.assign_grazing_cells([cow])
    assert cow.is_alive is False
    assert cow.died_today is True
