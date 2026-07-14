from src.farm import Farm
from src.pasture.pasture import Pasture
from src.weather import Weather
from src.finances import Finances
from src.events import EventManager
from src.animals.cow import Cow
from src.animals.sheep import Sheep
from src.animals.hen import Hen
from src.events import ForestRanger
from src.config import (
    CHEESE_RIPEN_DAYS,
    CHEESE_INCOME,
    SHEEP_MILK_INCOME,
    EGG_INCOME,
    HEN_LIFESPAN,
    HEN_PREDATOR_CHANCE_BONUS,
)


# helper: build a farm
def make_farm(animals=None):
    return Farm(
        name="Test name",
        pasture=Pasture(5, 5),
        weather=Weather(),
        finances=Finances(),
        events=EventManager(),
        animals=animals,
    )


def test_farm_starts_empty():
    f = make_farm()
    assert f.day == 0
    assert f.name == "Test name"
    assert f.animal_count() == 0


def test_remove_dead():
    a = Cow(id=1, position=(0, 0), name="A")
    b = Cow(id=2, position=(0, 0), name="B")
    b.is_alive = False
    f = make_farm([a, b])
    dead = f.remove_dead()
    assert f.animal_count() == 1
    assert len(dead) == 1
    assert dead[0] is b


def test_next_id_is_always_new():
    f = make_farm()
    assert f._next_id() == 1
    assert f._next_id() == 2
    assert f._next_id() == 3


def test_next_id_considers_the_starting_herd():
    f = make_farm(
        [Cow(id=1, position=(0, 0), name="A"), Cow(id=5, position=(0, 0), name="B")]
    )
    assert f._next_id() == 6  # the counter starts from the highest id in the herd


def test_farm_is_active():
    f = make_farm()
    assert f.is_active() is True
    f.finances.budget = 0
    assert f.is_active() is False


# build a farm for the tests
def build_farm(cows=3):
    animals = []
    for i in range(cows):
        animals.append(Cow(id=i, position=(0, 0), name=f"C{i}"))
    return Farm(
        "Farm",
        Pasture(20, 20),
        Weather(),
        Finances(),
        EventManager(),
        animals,
    )


def test_new_day_increments_the_day():
    f = build_farm()
    log = f.new_day()
    assert f.day == 1
    assert log["day"] == 1


def test_new_day_dict_has_keys():
    f = build_farm()
    log = f.new_day()
    for key in [
        "day",
        "weather",
        "births",
        "dead",
        "death_causes",
        "fed",
        "predators",
        "animal_states",
        "hungry",
        "grass_patches",
        "finances",
        "events",
    ]:
        assert key in log


def test_new_day_weather_is_valid():
    f = build_farm()
    log = f.new_day()
    assert log["weather"] in ("sunny", "rain", "drought")


def test_new_day_settles_finances():
    f = build_farm()
    log = f.new_day()
    finances = log["finances"]
    assert finances["balance"] == finances["income"] - finances["cost"]


def test_new_day_works_for_several_days():
    f = build_farm()
    for _ in range(5):
        f.new_day()
    assert f.day == 5


def test_new_day_returns_a_valid_animal_log():
    f = build_farm(cows=1)
    animal_log = f.new_day()["animal_states"][0]
    for key in [
        "id",
        "name",
        "display_pos",
        "grazing_cell_pos",
        "satiety",
        "age",
        "is_adult",
        "is_pregnant",
        "ate",
        "is_alive",
        "died_today",
    ]:
        assert key in animal_log


def test_ranger_active_reaches_the_log():
    f = build_farm()
    f.events.event_chance = 0  # no random events, we test only the ranger
    ranger = ForestRanger()
    ranger.days_left = ranger.duration_days
    ranger.apply(f)
    f.events.active.append(ranger)
    log = f.new_day()
    assert log["ranger_active"] is True


def test_without_ranger_the_flag_is_false():
    f = build_farm()
    f.events.event_chance = 0
    log = f.new_day()
    assert log["ranger_active"] is False


def test_antenna_counts_down_and_reaches_the_log():
    f = build_farm()
    f.events.event_chance = 0
    f.antenna_days_left = 3
    log = f.new_day()
    assert log["antenna_active"] is True
    assert f.antenna_days_left == 2  # one day gone


#  Hens and the coop ***********************************************


def test_owning_hens_raises_the_predator_chance():
    # only the fact of owning hens counts; two hens raise it the same as one
    f = make_farm([Hen(1, (0, 0), "A"), Hen(2, (0, 0), "B")])
    f.predator_chance = 0.2
    assert f._predator_chance_today(False) == 0.2 + HEN_PREDATOR_CHANCE_BONUS


def test_without_hens_no_predator_bonus():
    f = make_farm([Cow(1, (0, 0), "Moo")])
    f.predator_chance = 0.2
    assert f._predator_chance_today(False) == 0.2


def test_hen_walks_the_board():
    hen = Hen(id=1, position=(0, 0), name="Henny")
    f = make_farm([hen])
    f.events.event_chance = 0
    f.predator_chance = 0
    f.new_day()
    # the hen wanders the board and gets a position within the pasture
    assert hen.display_pos is not None
    x, y = hen.display_pos
    assert 0 <= x < f.pasture.width
    assert 0 <= y < f.pasture.height


def test_ufo_flees_from_a_hen():
    # the UFO hits the hen (the only animal) and flees from a descendant of dinosaurs, abducting no one
    from src.events import EventManager, UfoInvasion

    hen = Hen(id=1, position=(0, 0), name="Henny")
    f = make_farm([hen])
    f.predator_chance = 0
    f.events = EventManager(pool=[UfoInvasion], event_chance=1.0)
    log = f.new_day()
    assert hen.is_alive is True
    assert any("dinosaur" in o.lower() for o in log["events"])


def test_hen_survives_a_lethal_event():
    # a lethal event kills the whole herd, but the Farm reverts the hen's death (it dies only of old age)
    from src.events import RandomEvent, EventManager

    class KillerEvent(RandomEvent):
        def __init__(self):
            super().__init__()
            self.name = "Cataclysm"
            self.description = "kills everyone"
            self.duration_days = 1

        def should_trigger(self, day):
            return True

        def apply(self, farm):
            for a in farm.animals:
                a.is_alive = False
                a.died_today = True
            return self.description

        def revert(self, farm):
            pass

    hen = Hen(id=1, position=(0, 0), name="Henny")
    f = make_farm([hen])
    f.predator_chance = 0
    f.events = EventManager(pool=[KillerEvent], event_chance=1.0)
    f.new_day()
    assert hen.is_alive is True  # the event killed it, but the Farm reverted the death


def test_hen_gives_egg_income():
    hen = Hen(id=1, position=(0, 0), name="Henny")
    f = make_farm([hen])
    f.events.event_chance = 0
    f.predator_chance = 0
    log = f.new_day()
    assert log["finances"]["income"] == EGG_INCOME


def test_coop_disappears_when_the_last_hen_dies():
    hen = Hen(id=1, position=(0, 0), name="Henny")
    f = make_farm([hen])
    f.events.event_chance = 0
    f.predator_chance = 0
    log = f.new_day()  # day 1: the hen is alive, the coop is active
    assert log["coop_active"] is True
    hen.age = HEN_LIFESPAN  # the next day finishes it off with old age
    log = f.new_day()
    assert log["coop_active"] is False
    assert log["coop_gone"] is True
    assert log["death_causes"]["Henny"] == "old age"


#  Cheese vat *******************************************


# helper: a farm with one adult sheep and the vat on, no randomness
def farm_with_sheep_and_vat():
    sheep = Sheep(id=1, position=(0, 0), name="Bella")
    sheep.is_adult = True
    f = make_farm([sheep])
    f.events.event_chance = 0
    f.predator_chance = 0
    f.cheese_vat = True
    return f


def test_cheese_comes_only_after_ripening_in_the_vat():
    f = farm_with_sheep_and_vat()
    # for the first CHEESE_RIPEN_DAYS days the milk ripens, no cheese yet
    for _ in range(CHEESE_RIPEN_DAYS):
        log = f.new_day()
        assert log["cheese_vat"]["cheese_today"] == 0
        assert log["finances"]["income"] == 0
    # the next day the first batch is ready and cheese worth more than milk comes out
    log = f.new_day()
    assert log["cheese_vat"]["cheese_today"] == CHEESE_INCOME
    assert log["finances"]["income"] == CHEESE_INCOME
    assert CHEESE_INCOME > SHEEP_MILK_INCOME  # cheese pays off better than milk alone


def test_vat_announces_how_much_cheese_ripens_tomorrow():
    f = farm_with_sheep_and_vat()
    for _ in range(CHEESE_RIPEN_DAYS - 1):
        log = f.new_day()
        assert log["cheese_vat"]["cheese_today"] == 0  # no cheese out yet
    log = f.new_day()  # the last ripening day of the first batch
    assert log["cheese_vat"]["cheese_today"] == 0
    assert log["cheese_vat"]["cheese_tomorrow"] == CHEESE_INCOME  # cheese comes tomorrow
    log = f.new_day()
    assert log["cheese_vat"]["cheese_today"] == CHEESE_INCOME  # and it really does


def test_cheese_still_comes_after_the_sheep_dies():
    # milk put in the vat ripens independently of the sheep, so cheese comes even after it dies
    f = farm_with_sheep_and_vat()
    sheep = f.animals[0]
    for _ in range(CHEESE_RIPEN_DAYS):  # 3 days of milk = 3 batches waiting in the vat
        f.new_day()
    sheep.is_alive = False  # the sheep dies before any batch ripened
    log = f.new_day()
    assert sum(1 for a in f.animals if a.species == "sheep") == 0  # no sheep in the herd
    assert log["cheese_vat"]["cheese_today"] == CHEESE_INCOME  # and cheese comes anyway
    assert log["finances"]["income"] == CHEESE_INCOME


def test_without_the_vat_a_sheep_gives_only_milk():
    sheep = Sheep(id=1, position=(0, 0), name="Bella")
    sheep.is_adult = True
    f = make_farm([sheep])
    f.events.event_chance = 0
    f.predator_chance = 0
    log = f.new_day()
    assert log["cheese_vat"]["active"] is False
    assert log["finances"]["income"] == SHEEP_MILK_INCOME
