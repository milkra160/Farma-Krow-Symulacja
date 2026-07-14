from src.animals.cow import Cow
from src.animals.predator import Predator
from src.animals.calf import Calf
from src.animals.sheep import Sheep
from src.animals.lamb import Lamb
from src.animals.hen import Hen
from src.config import *
from src.pasture.cell import Cell


#  Cow *********************************************************


def test_cow_starts_with_full_satiety():
    c = Cow(id=1, position=(0, 0), name="Spotty")
    assert c.satiety == START_SATIETY


def test_cow_ages():
    c = Cow(id=1, position=(0, 0), name="Hippolyte")
    c.age_one_day()
    assert c.age == 1
    assert c.satiety == START_SATIETY - DAILY_SATIETY_LOSS


def test_cow_dies_of_hunger():
    c = Cow(id=1, position=(0, 0), name="Charlie")
    c.satiety = DAILY_SATIETY_LOSS
    c.age_one_day()
    assert c.is_alive is False
    assert c.died_today is True


def test_cow_grows_up():
    c = Cow(id=1, position=(0, 0), name="Spotty")
    c.satiety = 999
    for _ in range(ADULT_AGE):
        c.age_one_day()
    assert c.is_adult is True


def test_cow_eats():
    c = Cow(id=1, position=(0, 0), name="Spotty")
    c.satiety = 50
    c.eat()
    assert c.satiety == 50 + SATIETY_PER_MEAL
    assert c.ate_today is True


def test_cow_does_not_eat_above_max():
    c = Cow(id=1, position=(0, 0), name="Stanley")
    c.satiety = 90
    c.eat()
    assert c.satiety == START_SATIETY


def test_cow_reset_for_day():
    c = Cow(id=1, position=(0, 0), name="Mark")
    c.ate_today = True
    c.died_today = True
    c.grazing_cell = Cell(x=0, y=0)
    c.reset_for_day()
    assert c.ate_today is False
    assert c.died_today is False
    assert c.grazing_cell is None


def test_cow_is_hungry():
    c = Cow(id=1, position=(0, 0), name="Beatrice")
    c.satiety = 39
    assert c.is_hungry() is True
    c.satiety = 40
    assert c.is_hungry() is False


def test_cow_milk_value():
    c = Cow(id=1, position=(0, 0), name="Mel")
    c.is_adult = False
    assert c.milk_value() == 0

    c.is_adult = True
    assert c.milk_value() == COW_MILK_INCOME


#  Calf *******************************************************


def test_calf_has_symbol_c():
    c = Calf(id=2, position=(1, 1), name="Little")
    assert c.symbol == "c"


def test_calf_produces_no_milk():
    c = Calf(id=2, position=(1, 1), name="Little")
    assert c.milk_value() == 0


def test_calf_inherits_ageing():
    c = Calf(id=2, position=(1, 1), name="Little")
    c.age_one_day()
    assert c.age == 1


#  Sheep *********************************************************


def test_sheep_has_symbol_and_species():
    s = Sheep(id=1, position=(0, 0), name="Bella")
    assert s.symbol == "S"
    assert s.species == "sheep"


def test_sheep_gets_hungry_slower_than_a_cow():
    s = Sheep(id=1, position=(0, 0), name="Bella")
    s.age_one_day()
    assert s.satiety == START_SATIETY - SHEEP_DAILY_SATIETY_LOSS
    assert SHEEP_DAILY_SATIETY_LOSS < DAILY_SATIETY_LOSS  # a sheep loses less than a cow


def test_adult_sheep_gives_little_milk():
    s = Sheep(id=1, position=(0, 0), name="Bella")
    s.is_adult = False
    assert s.product_value() == 0
    s.is_adult = True
    assert s.product_value() == SHEEP_MILK_INCOME


def test_only_an_adult_sheep_produces_sheep_milk():
    s = Sheep(id=1, position=(0, 0), name="Bella")
    assert s.produces_sheep_milk() is False  # not adult yet
    s.is_adult = True
    assert s.produces_sheep_milk() is True


def test_sheep_bears_a_lamb():
    s = Sheep(id=1, position=(0, 0), name="Bella")
    young = s.create_offspring(2, (0, 0), "Mandy")
    assert isinstance(young, Lamb)


#  Lamb *******************************************************


def test_lamb_has_symbol_and_is_juvenile():
    lamb = Lamb(id=2, position=(1, 1), name="Mandy")
    assert lamb.symbol == "l"
    assert lamb.is_juvenile is True
    assert lamb.species == "sheep"


def test_lamb_produces_no_milk():
    lamb = Lamb(id=2, position=(1, 1), name="Mandy")
    assert lamb.product_value() == 0


def test_lamb_grows_into_a_sheep_keeping_its_state():
    lamb = Lamb(id=2, position=(1, 1), name="Mandy")
    lamb.satiety = 55
    lamb.is_adult = True
    adult = lamb.to_adult()
    assert isinstance(adult, Sheep)
    assert not isinstance(adult, Lamb)
    assert adult.satiety == 55
    assert adult.name == "Mandy"


#  Hen *********************************************************


def test_hen_lays_eggs_and_does_not_graze():
    h = Hen(id=1, position=(0, 0), name="Henny")
    assert h.species == "hen"
    assert h.grazes() is False  # fed from the coop, not from grass
    assert h.product_value() == EGG_INCOME


def test_hen_dies_of_old_age_after_a_set_time():
    h = Hen(id=1, position=(0, 0), name="Henny")
    for _ in range(HEN_LIFESPAN):
        h.age_one_day()
        assert h.is_alive is True  # alive for its whole lifespan
    h.age_one_day()  # the day past the limit
    assert h.is_alive is False
    assert h.died_today is True


def test_hen_does_not_die_of_hunger():
    h = Hen(id=1, position=(0, 0), name="Henny")
    h.satiety = 0  # even with zero satiety
    h.age_one_day()
    assert h.is_alive is True  # a hen dies of old age, not hunger


def test_hen_death_is_final_only_from_old_age():
    h = Hen(id=1, position=(0, 0), name="Henny")
    h.age = 3
    assert h.death_is_final() is False  # young, an event death does not stick
    h.age = HEN_LIFESPAN + 1
    assert h.death_is_final() is True  # past its lifespan


#  Predator *******************************************************


def test_predator_has_exclamation_symbol():
    d = Predator(id=1, position=(0, 0))
    assert d.symbol == "!"


def test_predator_kills_a_cow():
    c = Cow(id=1, position=(3, 3), name="Spot")
    d = Predator(id=2, position=(3, 3))
    result = d.attack(c)
    assert result is True
    assert c.is_alive is False
    assert c.died_today is True


# make sure move() does not error (it must exist, inherited from Animal)
def test_predator_does_not_move():
    d = Predator(id=1, position=(3, 3))
    d.move()
    assert d.position == (3, 3)
