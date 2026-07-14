from src.finances import Finances
from src import config
from src.weather import Weather
from src.animals.cow import Cow
from src.animals.calf import Calf
from src.animals.sheep import Sheep
from src.animals.lamb import Lamb
from src.animals.hen import Hen
from src.events import (
    ValentinesDay,
    SuddenDrought,
    Epidemic,
    Veterinarian,
    MeteorStrike,
    GmoFeed,
    Easter,
    UfoInvasion,
    ForestRanger,
    RainySeason,
    JealousGoat,
    MiracleOnTheOder,
    EventManager,
    RandomEvent,
)


# ****************** Fake farm
class FakeFarm:
    def __init__(self, animals=None):
        self.animals = animals if animals is not None else []
        self.finances = Finances()
        self.weather = Weather()
        self.graveyard = []
        self.pending_heals = []
        self.births_today = []
        self.resurrections_today = []
        self.predator_chance = config.PREDATOR_CHANCE
        self.antenna_days_left = 0
        self.last_id = 0
        for a in self.animals:
            if a.id > self.last_id:
                self.last_id = a.id

    def _next_id(self):
        self.last_id += 1
        return self.last_id


# ******************** Valentine's Day
def test_valentines_day_triggers_on_day_14():
    v = ValentinesDay()
    assert v.should_trigger(14) is True
    assert v.should_trigger(13) is False


def test_valentines_raises_and_reverts_pregnancy_chance():
    ff = FakeFarm([])
    v = ValentinesDay()
    before = config.PREGNANCY_CHANCE
    v.apply(ff)
    assert config.PREGNANCY_CHANCE == before * 1.5
    v.revert(ff)
    assert config.PREGNANCY_CHANCE == before


# **************** Sudden Drought


def test_sudden_drought_halves_grass_and_forces_drought():
    ff = FakeFarm([])
    before = config.BASE_GRASS_PATCHES
    d = SuddenDrought()
    d.apply(ff)
    assert config.BASE_GRASS_PATCHES == before // 2
    assert ff.weather.forced_state == "drought"
    d.revert(ff)
    assert config.BASE_GRASS_PATCHES == before
    assert ff.weather.forced_state is None


# ************ Epidemic


def test_epidemic_takes_30_satiety_from_everyone():
    c1 = Cow(id=1, position=(0, 0), name="Bart")
    c2 = Cow(id=2, position=(0, 0), name="Bart")
    c1.satiety = 100
    c2.satiety = 50
    Epidemic().apply(FakeFarm([c1, c2]))
    assert c1.satiety == 70
    assert c2.satiety == 20


# ************** Veterinarian


def test_vet_heals_a_cow_to_full():
    c = Cow(id=1, position=(0, 0), name="Bart")
    c.satiety = 1
    ff = FakeFarm([c])
    Veterinarian().apply(ff)
    assert c.satiety == config.START_SATIETY
    assert c in ff.pending_heals


def test_vet_on_an_empty_farm():
    result = Veterinarian().apply(FakeFarm([]))
    assert isinstance(result, str)


def test_vet_skips_hens():
    hen = Hen(id=1, position=(0, 0), name="Henny")
    ff = FakeFarm([hen])
    Veterinarian().apply(ff)
    assert hen not in ff.pending_heals  # a hen does not go hungry, so the vet skips it


# ************ GMO Feed


def test_gmo_feed_raises_and_reverts_income():
    ff = FakeFarm([])
    m = GmoFeed()
    before = config.COW_MILK_INCOME
    m.apply(ff)
    assert config.COW_MILK_INCOME == before * 1.3
    m.revert(ff)
    assert config.COW_MILK_INCOME == before


# ******* Meteor Strike


def test_meteor_kills_cows_and_zeros_the_budget():
    c1 = Cow(id=1, position=(0, 0), name="Bart")
    c2 = Cow(id=2, position=(0, 0), name="Bart")
    farm = FakeFarm([c1, c2])
    farm.finances.budget = 500
    MeteorStrike().apply(farm)
    assert farm.finances.budget == 0
    assert c1.is_alive is False
    assert c2.is_alive is False


# +++++++++++ Easter


def test_easter_revives_a_dead_cow():
    c = Cow(id=1, position=(0, 0), name="Bart")
    c.is_alive = False
    c.died_today = True
    c.satiety = 5
    ff = FakeFarm([])
    ff.graveyard.append(c)
    Easter().apply(ff)
    assert c.is_alive is True
    assert c.died_today is False
    assert c.satiety == config.START_SATIETY
    assert c in ff.animals
    assert c not in ff.graveyard


def test_easter_with_no_dead_cows_changes_nothing():
    ff = FakeFarm([Cow(id=1, position=(0, 0), name="Bart")])
    result = Easter().apply(ff)
    assert isinstance(result, str)


def test_easter_revives_a_hen_with_a_fresh_life():
    h = Hen(id=1, position=(0, 0), name="Henny")
    h.age = 99  # died of old age
    h.is_alive = False
    ff = FakeFarm([])
    ff.graveyard.append(h)
    description = Easter().apply(ff)
    assert h.is_alive is True
    assert h.age == 0  # resurrection means a fresh, full life cycle
    assert "hen" in description.lower()  # the message matches the species, not "cow"


# ************** UFO


def test_ufo_abducts_a_living_cow():
    c = Cow(id=1, position=(0, 0), name="Bart")
    UfoInvasion().apply(FakeFarm([c]))
    assert c.died_today is True
    assert c.is_alive is False


def test_no_error_when_ufo_hits_an_empty_farm():
    result = UfoInvasion().apply(FakeFarm([]))
    assert isinstance(result, str)


def test_ufo_flees_when_it_hits_a_hen():
    h = Hen(id=1, position=(0, 0), name="Henny")
    description = UfoInvasion().apply(FakeFarm([h]))
    assert h.is_alive is True  # the hen is not abducted
    assert "dinosaur" in description.lower()


def test_ufo_blocked_while_the_antenna_runs():
    ff = FakeFarm([])
    assert UfoInvasion().is_blocked(ff) is False  # no antenna, the UFO can happen
    ff.antenna_days_left = 3
    assert UfoInvasion().is_blocked(ff) is True  # the antenna runs, the UFO is blocked


def test_manager_blocks_ufo_with_the_antenna():
    # with the antenna running, the UFO abducts no cow, and the messages mention the jammed signal
    c = Cow(id=1, position=(0, 0), name="Bart")
    ff = FakeFarm([c])
    ff.antenna_days_left = 5
    m = EventManager(pool=[UfoInvasion], event_chance=1.0)
    messages = m.update(ff, 1)
    assert c.is_alive is True  # the cow is not abducted
    assert len(m.active) == 0  # the UFO did not become an active event
    assert any("antenna" in o.lower() for o in messages)


# ************ Forest Ranger


def test_ranger_zeros_and_reverts_the_predator_chance():
    ff = FakeFarm([])
    ff.predator_chance = 0.15
    r = ForestRanger()
    r.apply(ff)
    assert ff.predator_chance == 0.0
    r.revert(ff)
    assert ff.predator_chance == 0.15


# ************* Rainy Season


def test_rainy_season_sets_and_reverts_rain():
    ff = FakeFarm([])
    p = RainySeason()
    p.apply(ff)
    assert ff.weather.forced_state == "rain"
    p.revert(ff)
    assert ff.weather.forced_state is None


# ****************** Jealous Goat


def test_jealous_goat_zeros_and_reverts_grass():
    ff = FakeFarm([])
    g = JealousGoat()
    before = config.BASE_GRASS_PATCHES
    g.apply(ff)
    assert config.BASE_GRASS_PATCHES == 0
    g.revert(ff)
    assert config.BASE_GRASS_PATCHES == before


# **************** Miracle on the Oder


def test_miracle_births_a_calf():
    mother = Cow(id=1, position=(0, 0), name="Mother")
    mother.is_adult = True
    ff = FakeFarm([mother])
    MiracleOnTheOder().apply(ff)
    assert len(ff.animals) == 2
    assert isinstance(ff.animals[1], Calf)


def test_miracle_a_sheep_births_a_lamb():
    mother = Sheep(id=1, position=(0, 0), name="Bella")
    mother.is_adult = True
    ff = FakeFarm([mother])
    MiracleOnTheOder().apply(ff)
    assert len(ff.animals) == 2
    assert isinstance(ff.animals[1], Lamb)  # a sheep bears a lamb, not a calf


def test_miracle_with_no_adult_cows_adds_nothing():
    young = Calf(id=1, position=(0, 0), name="Young")
    ff = FakeFarm([young])
    result = MiracleOnTheOder().apply(ff)
    assert len(ff.animals) == 1
    assert isinstance(result, str)

    # **********************************


class FakeEvent(RandomEvent):
    triggered = True

    def __init__(self):
        super().__init__()
        self.name = "fake"
        self.description = "Fake"
        self.duration_days = 2
        self.applied = False
        self.reverted = False

    def should_trigger(self, day: int):
        return FakeEvent.triggered

    def apply(self, farm):
        self.applied = True
        return self.description

    def revert(self, farm):
        self.reverted = True


def test_manager_activates_an_event():
    FakeEvent.triggered = True
    m = EventManager(pool=[FakeEvent], event_chance=1.0)
    messages = m.update(None, 1)
    assert len(m.active) == 1
    assert m.active[0].applied is True
    assert any("Fake" in o for o in messages)


def test_manager_does_nothing_when_nothing_triggers():
    FakeEvent.triggered = False
    m = EventManager(pool=[FakeEvent], event_chance=1.0)
    messages = m.update(None, 1)
    assert len(m.active) == 0
    assert messages == []


def test_manager_expires_and_reverts():
    FakeEvent.triggered = True
    m = EventManager(pool=[FakeEvent], event_chance=1.0)
    m.update(None, 1)  # activates, days_left = 2
    e = m.active[0]
    FakeEvent.triggered = False  # so no new ones activate
    m.update(None, 2)  # down to 1, still active
    assert len(m.active) == 1
    m.update(None, 3)  # 1 to 0, revert and drop
    assert len(m.active) == 0
    assert e.reverted is True
