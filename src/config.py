# *** Simulation-wide constants ***
BOARD_SIZE: tuple[int, int] = (20, 20)
MAX_DAYS: int = 100
EVENT_CHANCE: float = 0.10


# Animal constants
START_SATIETY: int = 100
DAILY_SATIETY_LOSS: int = 20
SATIETY_PER_MEAL: int = 30

ADULT_AGE: int = 10
PREGNANCY_CHANCE: float = 0.08
GESTATION_DAYS: int = 7

COW_MILK_INCOME: int = 20

PREDATOR_CHANCE: float = 0.15
MAX_PREDATORS: int = 2

ANIMAL_NAMES: list = [
    # male
    "Oliver",
    "George",
    "Harry",
    "Jack",
    "Charlie",
    "Thomas",
    "Henry",
    "William",
    "James",
    "Edward",
    "Arthur",
    "Alfred",
    "Walter",
    "Albert",
    "Frank",
    "Ernest",
    "Leonard",
    "Stanley",
    "Herbert",
    "Cecil",
    # female
    "Alice",
    "Emily",
    "Grace",
    "Mary",
    "Florence",
    "Edith",
    "Ada",
    "Nellie",
    "Beatrice",
    "Doris",
    "Hilda",
    "Ivy",
    "Elsie",
    "Gladys",
    "Violet",
    "Agnes",
    "Nora",
    "Ethel",
    "Maud",
    "Rose",
]


# Weather and pasture
RAIN_MULTIPLIER: float = 1.2
DROUGHT_MULTIPLIER: float = 0.8
SUN_MULTIPLIER: float = 1.0

BASE_GRASS_PATCHES: int = 12

# Finances
START_BUDGET: float = 500
DAILY_FARM_COST: int = 50

# Sheep (shop only).
# A sheep loses satiety slower than a cow, so it lives longer on the same grass.
SHEEP_DAILY_SATIETY_LOSS: int = 12
# Sheep milk sells for little on its own. It only pays off once turned into cheese.
SHEEP_MILK_INCOME: int = 5
# Cheese made from one sheep's milk. Set 10 higher than a cow (COW_MILK_INCOME = 20).
CHEESE_INCOME: int = 30
# Days the cheese vat needs to ripen sheep milk into cheese.
CHEESE_RIPEN_DAYS: int = 3

# Hens (shop only).
# A hen does not graze; the coop feeds it, and its eggs are steady income.
EGG_INCOME: int = 40
# A hen lives this many days, then dies of old age (never of hunger).
HEN_LIFESPAN: int = 7
# A hen is loud and draws predators. Owning any hen raises the predator chance by this much.
HEN_PREDATOR_CHANCE_BONUS: float = 0.10

# Shop prices
ADULT_COW_PRICE: int = 200
CALF_PRICE: int = 100
ADULT_SHEEP_PRICE: int = 120
HEN_PRICE: int = 160
CHEESE_VAT_PRICE: int = 600  # cheese vat; one per farm
FEED_PRICE: int = 40  # a feed bag tops up the whole herd's satiety
FEED_SATIETY: int = 40  # satiety one feed bag adds
FENCE_PRICE: int = 150  # a fence lowers the predator chance for a few days
FENCE_DURATION: int = 7  # days a fence stands before it breaks
FENCE_CHANCE_MULTIPLIER: float = 0.25  # a fence leaves 25% of the chance; the rest drop off
ANTENNA_PRICE: int = 180  # antenna that jams the UFO signal
ANTENNA_DURATION: int = 5  # days the antenna blocks the UFO event

# Shop: each repeat purchase of the same item costs more, to discourage spamming one item.
COW_PRICE_STEP: int = 20
CALF_PRICE_STEP: int = 10
SHEEP_PRICE_STEP: int = 15
FEED_PRICE_STEP: int = 5
FENCE_PRICE_STEP: int = 20
ANTENNA_PRICE_STEP: int = 25
HEN_PRICE_STEP: int = 20
