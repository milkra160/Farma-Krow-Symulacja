from src.farm import Farm
from src.pasture.pasture import Pasture
from src.weather import Weather
from src.finances import Finances
from src.events import EventManager
from src.animals.cow import Cow
from src.animals.sheep import Sheep
from src.animals.hen import Hen
from src.shop import (
    Shop,
    BuyAdultCow,
    BuyCalf,
    BuyAdultSheep,
    BuyHen,
    BuyCheeseVat,
    FeedBag,
    Fence,
    BuyAntenna,
)
from src.config import *


# helper: build a farm with a given budget
def make_farm(budget=1000, animals=None):
    finances = Finances()
    finances.budget = budget
    return Farm(
        name="Test name",
        pasture=Pasture(5, 5),
        weather=Weather(),
        finances=finances,
        events=EventManager(),
        animals=animals,
    )


#  Finances.spend *************************************************


def test_spend_takes_money():
    f = Finances()
    f.budget = 500
    assert f.spend(200) is True
    assert f.budget == 300


def test_spend_refuses_when_too_little():
    f = Finances()
    f.budget = 100
    assert f.spend(200) is False
    assert f.budget == 100


def test_spend_does_not_let_budget_reach_zero():
    f = Finances()
    f.budget = 200
    assert f.spend(200) is False  # leaving 0 = bankruptcy, so it is refused
    assert f.budget == 200


#  Shop *******************************************************


def test_shop_has_a_default_catalog():
    shop = Shop()
    assert len(shop.catalog) == 8


def test_buy_adult_cow_adds_a_cow_and_takes_money():
    f = make_farm(budget=1000)
    shop = Shop()
    success, _ = shop.buy(BuyAdultCow(), f)
    assert success is True
    assert f.animal_count() == 1
    assert f.animals[0].is_adult is True
    assert f.finances.budget == 1000 - ADULT_COW_PRICE


def test_buy_calf_adds_a_juvenile():
    f = make_farm(budget=1000)
    shop = Shop()
    shop.buy(BuyCalf(), f)
    assert f.animal_count() == 1
    assert f.animals[0].symbol == "c"
    assert f.animals[0].is_adult is False


def test_buy_adult_sheep_adds_a_sheep():
    f = make_farm(budget=1000)
    success, _ = Shop().buy(BuyAdultSheep(), f)
    assert success is True
    assert isinstance(f.animals[0], Sheep)
    assert f.animals[0].is_adult is True
    assert f.finances.budget == 1000 - ADULT_SHEEP_PRICE


def test_buy_hen_adds_a_hen():
    f = make_farm(budget=1000)
    success, _ = Shop().buy(BuyHen(), f)
    assert success is True
    assert isinstance(f.animals[0], Hen)
    assert f.animals[0].grazes() is False  # a hen does not graze
    assert f.finances.budget == 1000 - HEN_PRICE


def test_cheese_vat_enables_cheese_and_is_unique():
    f = make_farm(budget=1000)
    vat = BuyCheeseVat()
    assert vat.available(f) is True
    Shop().buy(vat, f)
    assert f.cheese_vat is True
    # once the vat stands, it leaves the offer (one per farm)
    assert vat.available(f) is False


def test_antenna_gives_protection_for_a_few_days():
    f = make_farm(budget=1000)
    Shop().buy(BuyAntenna(), f)
    assert f.antenna_days_left == ANTENNA_DURATION


def test_item_price_rises_after_each_purchase():
    f = make_farm(budget=100000)
    shop = Shop()
    sheep = BuyAdultSheep()
    assert sheep.price == ADULT_SHEEP_PRICE
    shop.buy(sheep, f)
    assert sheep.price == ADULT_SHEEP_PRICE + SHEEP_PRICE_STEP  # second buy is dearer
    shop.buy(sheep, f)
    assert sheep.price == ADULT_SHEEP_PRICE + 2 * SHEEP_PRICE_STEP


def test_buy_without_money_fails():
    f = make_farm(budget=50)  # too little for anything
    shop = Shop()
    success, _ = shop.buy(BuyAdultCow(), f)
    assert success is False
    assert f.animal_count() == 0
    assert f.finances.budget == 50


def test_feed_bag_tops_up_satiety():
    cow = Cow(id=1, position=(0, 0), name="Bessie")
    cow.satiety = 30
    f = make_farm(budget=1000, animals=[cow])
    Shop().buy(FeedBag(), f)
    assert cow.satiety == 30 + FEED_SATIETY


def test_feed_bag_does_not_exceed_max():
    cow = Cow(id=1, position=(0, 0), name="Bessie")
    cow.satiety = 90
    f = make_farm(budget=1000, animals=[cow])
    Shop().buy(FeedBag(), f)
    assert cow.satiety == START_SATIETY


def test_fence_gives_protection_for_a_few_days():
    f = make_farm(budget=1000)
    Shop().buy(Fence(), f)
    assert f.fence_days_left == FENCE_DURATION


def test_fence_cuts_the_chance_but_does_not_zero_it():
    f = make_farm(budget=1000)
    f.predator_chance = 0.4
    # with the fence standing the chance is multiplied; without it, the full chance
    assert f._predator_chance_today(True) == 0.4 * FENCE_CHANCE_MULTIPLIER
    assert f._predator_chance_today(False) == 0.4


def test_fence_counts_down_a_day():
    f = make_farm(budget=1000)
    f.events.event_chance = 0  # disable random events so the test is stable
    Shop().buy(Fence(), f)
    log = f.new_day()
    assert log["fence_active"] is True
    assert f.fence_days_left == FENCE_DURATION - 1  # one day gone


def test_fence_destroyed_the_day_after_it_expires():
    f = make_farm(budget=1000)
    f.events.event_chance = 0
    f.predator_chance = 0  # no predators, a clean countdown test
    Shop().buy(Fence(), f)
    # for its whole duration the fence stands and is not destroyed
    for _ in range(FENCE_DURATION):
        log = f.new_day()
        assert log["fence_active"] is True
        assert log["fence_destroyed"] is False
    # only the next day, once the fence is gone, does the destroyed message land
    log = f.new_day()
    assert log["fence_active"] is False
    assert log["fence_destroyed"] is True


def test_hole_in_the_fence_stays_until_the_fence_is_gone():
    f = make_farm(budget=1000)
    f.events.event_chance = 0
    f.predator_chance = 0  # we drive the holes ourselves, no new predators
    Shop().buy(Fence(), f)
    f.fence_holes = [3]  # pretend a predator broke through in column 3 earlier
    log = f.new_day()
    assert 3 in log["fence_holes"]  # the hole is still there
    # once the fence expires the holes go with it
    for _ in range(FENCE_DURATION):
        f.new_day()
    assert f.fence_holes == []
