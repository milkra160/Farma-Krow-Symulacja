from abc import ABC, abstractmethod
import random
from src import config
from src.animals.cow import Cow
from src.animals.calf import Calf
from src.animals.sheep import Sheep
from src.animals.hen import Hen


# base class for a shop item. Each item has a name, description and price, and can "apply"
# itself to the farm. Like the random events, adding a new item is just a new subclass, with
# no changes to the Shop class (the open-closed principle).
class Item(ABC):
    def __init__(self):
        self.name = ""
        self.description = ""
        self.base_price = 0  # price of the first purchase
        self.price = 0  # current price (rises with each repeat purchase of this item)
        self.price_step = 0  # how much it goes up per purchase (0 = fixed price)
        self.times_bought = 0  # how many times this item has been bought (for price balance)
        self.category = ""  # "animal" / "feed" / "upgrade", for the end-of-run statistics

    # some items only make sense in certain conditions (e.g. a fence only once a predator threatens)
    def available(self, farm) -> bool:
        return True

    # apply the purchase effect to the farm (the shop has already taken the money). Returns a message
    @abstractmethod
    def apply(self, farm) -> str:
        pass

    # after a successful purchase the next unit of this item costs more, which curbs spamming one item
    def register_purchase(self):
        self.times_bought += 1
        self.price = self.base_price + self.price_step * self.times_bought

    def __str__(self) -> str:
        return f"{self.name} - {self.price} zł"


# --------------------------------------------------------------------


# Adult cow. Gives milk right away, but costs the most
class BuyAdultCow(Item):
    def __init__(self):
        super().__init__()
        self.name = "Adult cow"
        self.description = "An adult cow that gives milk from the next day"
        self.base_price = config.ADULT_COW_PRICE
        self.price = config.ADULT_COW_PRICE
        self.price_step = config.COW_PRICE_STEP
        self.category = "animal"

    def apply(self, farm) -> str:
        name = random.choice(config.ANIMAL_NAMES)
        cow = Cow(id=farm._next_id(), position=(0, 0), name=name)
        cow.is_adult = True
        cow.age = config.ADULT_AGE
        farm.add_animal(cow)
        return f"Bought an adult cow {name}"


# --------------------------------------------------------------------


# Calf. Cheaper, but has to grow up first before it gives milk
class BuyCalf(Item):
    def __init__(self):
        super().__init__()
        self.name = "Calf"
        self.description = "Cheaper, but only starts giving milk once it grows up"
        self.base_price = config.CALF_PRICE
        self.price = config.CALF_PRICE
        self.price_step = config.CALF_PRICE_STEP
        self.category = "animal"

    def apply(self, farm) -> str:
        name = random.choice(config.ANIMAL_NAMES)
        calf = Calf(id=farm._next_id(), position=(0, 0), name=name)
        farm.add_animal(calf)
        return f"Bought a calf {name}"


# --------------------------------------------------------------------


# Feed bag. Rescues a hungry herd regardless of the grass on the pasture
class FeedBag(Item):
    def __init__(self):
        super().__init__()
        self.name = "Feed bag"
        self.description = f"Adds {config.FEED_SATIETY} satiety to the whole herd"
        self.base_price = config.FEED_PRICE
        self.price = config.FEED_PRICE
        self.price_step = config.FEED_PRICE_STEP
        self.category = "feed"

    def apply(self, farm) -> str:
        fed = 0
        for animal in farm.animals:
            if animal.is_alive:
                animal.satiety = min(
                    animal.satiety + config.FEED_SATIETY, config.START_SATIETY
                )
                fed += 1
        return f"Fed {fed} animals with the feed bag"


# --------------------------------------------------------------------


# Fence. For a few days it strongly lowers the predator chance, then it breaks
class Fence(Item):
    def __init__(self):
        super().__init__()
        self.name = "Fence"
        self.description = (
            f"Lowers the predator chance for {config.FENCE_DURATION} days"
        )
        self.base_price = config.FENCE_PRICE
        self.price = config.FENCE_PRICE
        self.price_step = config.FENCE_PRICE_STEP
        self.category = "upgrade"

    # putting up a new fence renews the protection for the full FENCE_DURATION days
    def apply(self, farm) -> str:
        farm.fence_days_left = config.FENCE_DURATION
        farm.fence_holes = []  # a new fence has no holes
        return f"Fence up. Lower predator chance for {config.FENCE_DURATION} days"


# --------------------------------------------------------------------


# Jamming antenna. For a few days it blocks the UFO event (aliens do not abduct cows).
# Putting up a new antenna renews the protection for the full ANTENNA_DURATION days.
class BuyAntenna(Item):
    def __init__(self):
        super().__init__()
        self.name = "Jamming antenna"
        self.description = f"Blocks UFO abductions for {config.ANTENNA_DURATION} days"
        self.base_price = config.ANTENNA_PRICE
        self.price = config.ANTENNA_PRICE
        self.price_step = config.ANTENNA_PRICE_STEP
        self.category = "upgrade"

    def apply(self, farm) -> str:
        farm.antenna_days_left = config.ANTENNA_DURATION
        return f"Antenna up. UFOs blocked for {config.ANTENNA_DURATION} days"


# --------------------------------------------------------------------


# Adult sheep. Cheaper than a cow and lives longer (gets hungry slower), but its milk is worth
# little. Only pays off with a cheese vat, which turns sheep milk into more valuable cheese.
class BuyAdultSheep(Item):
    def __init__(self):
        super().__init__()
        self.name = "Adult sheep"
        self.description = "Lives longer than a cow, but its milk is worth little. Pays off with a cheese vat"
        self.base_price = config.ADULT_SHEEP_PRICE
        self.price = config.ADULT_SHEEP_PRICE
        self.price_step = config.SHEEP_PRICE_STEP
        self.category = "animal"

    def apply(self, farm) -> str:
        name = random.choice(config.ANIMAL_NAMES)
        sheep = Sheep(id=farm._next_id(), position=(0, 0), name=name)
        sheep.is_adult = True
        sheep.age = config.ADULT_AGE
        farm.add_animal(sheep)
        return f"Bought an adult sheep {name}"


# --------------------------------------------------------------------


# Hen. Does not eat grass (the coop feeds it), lays high-value eggs, but lives only a few days,
# and as a loud, easy target it raises the predator chance for the whole herd.
class BuyHen(Item):
    def __init__(self):
        super().__init__()
        self.name = "Hen"
        self.description = (
            f"Lays eggs worth {config.EGG_INCOME} zł/day for "
            f"{config.HEN_LIFESPAN} days. Does not eat grass, but draws predators"
        )
        self.base_price = config.HEN_PRICE
        self.price = config.HEN_PRICE
        self.price_step = config.HEN_PRICE_STEP
        self.category = "animal"

    def apply(self, farm) -> str:
        name = random.choice(config.ANIMAL_NAMES)
        hen = Hen(id=farm._next_id(), position=(0, 0), name=name)
        farm.add_animal(hen)
        return f"Bought a hen {name}"


# --------------------------------------------------------------------


# Cheese vat. A machine bought once for the whole game. Turns adult sheep milk into cheese:
# the milk goes into the vat and after CHEESE_RIPEN_DAYS days comes out as cheese worth more than milk.
class BuyCheeseVat(Item):
    def __init__(self):
        super().__init__()
        self.name = "Cheese vat"
        self.description = (
            f"Turns sheep milk into cheese after {config.CHEESE_RIPEN_DAYS} days "
            f"({config.CHEESE_INCOME} zł per sheep). One per farm"
        )
        self.base_price = config.CHEESE_VAT_PRICE
        self.price = config.CHEESE_VAT_PRICE
        self.category = "upgrade"

    # there can be only one vat. Once it stands, it leaves the shop offer
    def available(self, farm) -> bool:
        return not farm.cheese_vat

    def apply(self, farm) -> str:
        farm.cheese_vat = True
        return "Bought a cheese vat. Sheep milk will now be turned into cheese"


# --------------------------------------------------------------------
# The Shop manages the item catalog and runs the transactions.
# It does not depend on the interface.


class Shop:
    def __init__(self, catalog=None):
        if catalog is None:
            catalog = [
                BuyAdultCow(),
                BuyCalf(),
                BuyAdultSheep(),
                BuyHen(),
                BuyCheeseVat(),
                FeedBag(),
                Fence(),
                BuyAntenna(),
            ]
        self.catalog = catalog

    # items currently available to buy (taking each item's conditions into account)
    def available_items(self, farm) -> list:
        available = []
        for item in self.catalog:
            if item.available(farm):
                available.append(item)
        return available

    # a purchase attempt: check the budget, take the money and apply the effect.
    def buy(self, item: Item, farm) -> tuple:
        if not item.available(farm):
            return False, "This item is not available right now"
        if not farm.finances.spend(item.price):
            return False, "Not enough money in the budget"
        message = item.apply(farm)
        item.register_purchase()  # the next unit of this item will cost more
        return True, message
