#  Cow Farm Simulation

A turn-based farm management game that runs in the terminal. You start with a
herd of dairy cows and a small budget, then decide how to spend it one day at a
time. One turn is one day. The aim is to keep the farm going for as long as you
can and finish as rich as possible.

Every run is driven by a seed, so you can replay the exact same game or try a
different strategy on equal footing.

## How the game works

Each day the farm loses money to upkeep and earns it back from what the animals
produce. Yesterday's weather sets how much grass grows today, the grass feeds
the herd, and animals that stay hungry too long eventually die. Random events
sit on top of all that and can swing a run either way.

- Weather sets how much grass grows. Rain, sun, and drought change the number of
  grass patches on a 20x20 board, and the animals graze those patches to eat.
- The herd is cows and calves, sheep and lambs, and hens. Each one has its own
  hunger, lifespan, and income, and the young have to grow up before they
  produce anything.
- Money is tight. The farm costs 50 zł a day and an adult cow brings in 20 zł of
  milk, so you need at least three cows just to break even.
- Predators show up on the pasture and pick off animals. Fences and other
  defences push the odds back down.
- The shop sells animals, feed, fences, a cheese vat, and a signal-jamming
  antenna. Buying the same item twice costs more each time, so spreading your
  money around helps.
- Random events can help or hurt: droughts, epidemics, a visiting vet, GMO feed,
  a meteor strike, a UFO abduction, and a few more.
- Finished runs get saved to a ranking, so you can compare farms across games.

### A couple of strategy notes

Sheep get hungry slower than cows, so they live longer, but their milk is nearly
worthless on its own. They only start paying off once you buy the cheese vat,
which ripens sheep milk into cheese worth 30 zł per sheep after three days.

Hens don't graze at all. The coop feeds them and their eggs are steady income,
but they're loud and pull predators toward the farm.

## Getting started

The project uses [uv](https://github.com/astral-sh/uv) for dependencies.

```bash
# install dependencies
uv sync

# run the game
uv run python -m src.main
```

When the game starts you pick a seed (or press Enter for a random one) and set a
few starting values: farm name, starting herd size, budget, predator odds, and
how long the run lasts. Values shown in `[]` are the defaults, so press Enter to
accept them.

## Running the tests

```bash
uv run pytest
```

## Project layout

```
src/
├── main.py          # entry point, sets up a run and reads player input
├── symulacja.py     # the day loop that ties everything together
├── config.py        # all the tunable constants (prices, income, odds...)
├── farma.py         # farm state: the herd, the budget, active defences
├── weather.py       # daily weather
├── finances.py      # income and upkeep
├── events.py        # the random events and the manager that rolls them
├── sklep.py         # the shop
├── ranking.py       # saved run rankings
├── logger.py        # coloured terminal output
├── wizualizacja.py  # board rendering
├── animals/         # cow, calf, sheep, lamb, hen, predator, livestock
└── pasture/         # the pasture grid and its cells
tests/               # pytest suite
```

## Authors

- **Miłosz Krawczyk** ([github.com/miloszkrawczyk](https://github.com/miloszkrawczyk))
- **Piotr Tarłowski** ([github.com/peterman1337](https://github.com/peterman1337))

Repository: [github.com/miloszkrawczyk/Cow-Farm-Simulation](https://github.com/miloszkrawczyk/Cow-Farm-Simulation)
