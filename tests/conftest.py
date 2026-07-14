import pytest
from src import config


# Random events mutate constants in the global config module (e.g. GmoFeed changes
# COW_MILK_INCOME, SuddenDrought BASE_GRASS_PATCHES, ValentinesDay PREGNANCY_CHANCE) and only
# revert them once the event expires. A test that ends with an active event leaves a mutated
# constant behind and breaks the next test. This fixture snapshots the simple config constants
# before each test and restores them afterwards, so tests stay independent of the run order.
@pytest.fixture(autouse=True)
def restore_config_constants():
    snapshot = {
        name: value
        for name, value in vars(config).items()
        if name.isupper() and isinstance(value, (int, float))
    }
    yield
    for name, value in snapshot.items():
        setattr(config, name, value)
