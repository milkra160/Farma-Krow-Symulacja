from src.config import *
from src.finances import Finances
from src.pasture.pasture import Pasture
from src.weather import Weather
from src.events import EventManager, ForestRanger
import random
from src.animals.predator import Predator
from src import config


# Farm is the central class of the simulation. It manages the herd, the pasture,
# the weather, the finances and the random events.
class Farm:
    def __init__(
        self,
        name: str,
        pasture: Pasture,
        weather: Weather,
        finances: Finances,
        events: EventManager,
        animals: list = None,
    ):
        self.name = name
        self.animals = animals if animals is not None else []
        self.predators = []
        self.pasture = pasture
        self.weather = weather
        self.finances = finances
        self.events = events
        self.graveyard = []  # animals that died (needed for Easter)
        self.births_today = []
        self.resurrections_today = []
        self.pending_heals = []
        # purchases made in the shop since the last day (shown in the next day's log)
        self.purchases_today = []
        # how many days the fence still stands against predators (0 = no fence)
        self.fence_days_left = 0
        # columns where a predator broke through the fence; the holes stay until the fence is gone
        self.fence_holes = []
        # whether the fence stood yesterday, so the "fence destroyed" message lands the day after it expires
        self.fence_stood_yesterday = False
        # cheese vat (bought in the shop, one per farm) turns sheep milk into cheese
        self.cheese_vat = False
        # milk batches ripening in the vat: each is [days_until_ready, cheese_value_in_zl]
        self.cheese_queue = []
        # how many days the antenna still jams the UFO signal (0 = no antenna)
        self.antenna_days_left = 0
        # the coop appears with the first hen and disappears when the last one dies. This flag
        # remembers whether there were hens yesterday, so the "coop gone" message lands on the right day
        self.had_hens_yesterday = False
        # counter for handing out UNIQUE ids; a number is never reused
        self.last_id = 0
        for animal in self.animals:
            if animal.id > self.last_id:
                self.last_id = animal.id
        self.day = 0
        self.predator_chance = PREDATOR_CHANCE
        self.max_predators = MAX_PREDATORS

    # add a new animal (cow/calf) to the herd
    def add_animal(self, animal):
        self.animals.append(animal)

    # drop dead animals from the herd and return them (so they can be logged later)
    def remove_dead(self) -> list:
        dead = []
        alive = []
        for animal in self.animals:
            if animal.is_alive:
                alive.append(animal)
            else:
                dead.append(animal)
        self.animals = alive
        self.graveyard.extend(dead)
        return dead

    def animal_count(self) -> int:
        return len(self.animals)

    # the farm runs until it goes bankrupt
    def is_active(self) -> bool:
        return not self.finances.is_bankrupt()

    # internal helper, used only inside this class. Hands out the next id, never repeated.
    def _next_id(self) -> int:
        self.last_id += 1
        return self.last_id

    # number of living hens in the herd (hens draw predators and get their own log section)
    def _hen_count(self) -> int:
        return sum(1 for a in self.animals if a.species == "hen" and a.is_alive)

    # predator chance. Owning any hen raises it (loud, draws predators) - the fact counts,
    # not the number of hens. A fence lowers the chance.
    def _predator_chance_today(self, fence_active: bool) -> float:
        chance = self.predator_chance
        if self._hen_count() > 0:
            chance += config.HEN_PREDATOR_CHANCE_BONUS
        if fence_active:
            chance *= config.FENCE_CHANCE_MULTIPLIER
        return min(chance, 1.0)

    # young that have reached adult age (calf c -> cow C, lamb J -> sheep O) become adults
    # of their species. Each juvenile knows what it grows into.
    def _grow_up_juveniles(self):
        new_herd = []
        grown_up_today = []
        for animal in self.animals:
            if animal.is_juvenile and animal.is_adult:
                adult = animal.to_adult()
                new_herd.append(adult)
                grown_up_today.append(adult.name)
            else:
                new_herd.append(animal)

        self.animals = new_herd
        return grown_up_today

    # Run the cheese vat for one day. First the batches already in the vat ripen (those whose
    # timer runs out come out as finished cheese), and today's sheep milk goes in as a new batch
    # with a CHEESE_RIPEN_DAYS counter. The pipeline is parallel: each day's milk ripens on its
    # own, so cheese comes out daily, just with a delay. Returns the state for the log.
    def _process_cheese_vat(self, sheep_milk_today: int) -> dict:
        cheese_today = 0
        if not self.cheese_vat:
            return {
                "active": False,
                "milk_today": 0,
                "cheese_today": 0,
                "cheese_tomorrow": 0,
                "batches_in_vat": 0,
            }

        # ripen the batches already in the vat - the ones with a 0 counter become finished cheese
        remaining = []
        for batch in self.cheese_queue:
            batch[0] -= 1
            if batch[0] <= 0:
                cheese_today += batch[1]
            else:
                remaining.append(batch)
        self.cheese_queue = remaining

        # today's sheep milk goes into the vat as a new batch
        if sheep_milk_today > 0:
            value = sheep_milk_today * config.CHEESE_INCOME
            self.cheese_queue.append([config.CHEESE_RIPEN_DAYS, value])

        # how much cheese ripens the next day = sum of batches with one day left.
        # This lets the player know up front how much money the vat brings tomorrow.
        cheese_tomorrow = sum(batch[1] for batch in self.cheese_queue if batch[0] == 1)

        return {
            "active": True,
            "milk_today": sheep_milk_today,
            "cheese_today": cheese_today,
            "cheese_tomorrow": cheese_tomorrow,
            "batches_in_vat": len(self.cheese_queue),
        }

    def _breed(
        self,
    ) -> list:  # internal method, returns the list of newborn calf names
        pregnancies_today = []

        # gather the mothers whose pregnancy ends today
        mothers = []
        for animal in self.animals:
            if animal.is_alive and animal.advance_pregnancy():
                mothers.append(animal)

        # roll for new pregnancies
        for animal in self.animals:
            if animal.is_alive:
                was_pregnant = animal.is_pregnant
                animal.maybe_conceive()
                if animal.is_pregnant and not was_pregnant:
                    pregnancies_today.append(
                        f"{animal.name} (in {animal.days_to_birth} days)"
                    )

        # give birth - each mother bears young of her own species (calf or lamb)
        births = []
        for mother in mothers:
            new_id = self._next_id()
            name = random.choice(ANIMAL_NAMES)
            young = mother.create_offspring(new_id, mother.position, name)
            # the young appears on a free cell next to its mother
            x, y = mother.display_pos
            young.display_pos = self.pasture._random_neighbor(x, y)
            self.add_animal(young)
            births.append(f"{young.name} (mother: {mother.name})")
        return births, pregnancies_today

    # The most important method, new_day!! One day of the simulation. Returns the day's log.
    def new_day(self) -> dict:
        # start of a new day
        self.day += 1

        # reset the animals for the new day
        for animal in self.animals:
            animal.reset_for_day()

        # clear the per-day event lists
        self.births_today = []
        self.resurrections_today = []
        self.pending_heals = []

        # random events
        event_descriptions = self.events.update(self, self.day)

        # roll a new weather state
        weather_state = self.weather.next_day()

        # clear the pasture and grow new grass
        self.pasture.clear()
        patch_count = int(config.BASE_GRASS_PATCHES * self.weather.grass_multiplier())
        self.pasture.scatter_grass(patch_count)

        # if the fence stands, it lowers the predator chance and we count down a day.
        # The "destroyed" message lands on the day the fence is already gone
        fence_active = self.fence_days_left > 0
        if fence_active:
            self.fence_days_left -= 1
        fence_destroyed = self.fence_stood_yesterday and not fence_active
        if fence_destroyed:
            self.fence_holes = []  # no fence, no holes
        self.fence_stood_yesterday = fence_active

        # if the antenna runs, it blocks today's UFO event (checked above in the events on the
        # not-yet-counted value) and we count down a day
        antenna_active = self.antenna_days_left > 0
        if antenna_active:
            self.antenna_days_left -= 1

        # predators - roll whether they show up. The fence cuts the chance but does not zero it -
        # a predator can still slip in through a hole in the fence
        self.predators = []
        predator_through_hole = False
        free_cells = self.pasture.grass_cells()
        if len(free_cells) > 0 and random.random() < self._predator_chance_today(
            fence_active
        ):
            count = random.randint(1, self.max_predators)
            count = min(count, len(free_cells))  # no more predators than cells
            for i in range(count):
                self.predators.append(Predator(id=i, position=(0, 0)))
            self.pasture.place_predators(self.predators)
            if fence_active:
                predator_through_hole = True  # broke in despite the standing fence
                # the hole it left stays in the fence until the fence is gone
                for p in self.predators:
                    column = p.position[0]
                    if column not in self.fence_holes:
                        self.fence_holes.append(column)

        # if an animal is already dead before reaching the pasture, it is e.g. an event victim
        dead_before_predators = []
        for animal in self.animals:
            if not animal.is_alive:
                dead_before_predators.append(animal.id)

        # seat only the grazing animals on the cells - hens eat from the coop,
        # so they do not take cells
        self.pasture.assign_grazing_cells([a for a in self.animals if a.grazes()])

        # hens do not graze but wander the farm - they get a random board position
        for hen in self.animals:
            if hen.is_alive and not hen.grazes():
                x = random.randint(0, self.pasture.width - 1)
                y = random.randint(0, self.pasture.height - 1)
                hen.display_pos = (x, y)

        # if an animal is now dead, it must be a predator victim
        killed_by_predator = []
        for animal in self.animals:
            if not animal.is_alive and animal.id not in dead_before_predators:
                killed_by_predator.append(animal.id)

        # natural causes
        for animal in self.animals:
            animal.age_one_day()

        # the vet tops animals up to full satiety at the end of the day (after the daily loss)
        for animal in self.pending_heals:
            if animal.is_alive:
                animal.satiety = START_SATIETY

        # hens can only die of old age - if something else (an event) "killed" them,
        # they come back to life. An event can attack them, but cannot kill them.
        for animal in self.animals:
            if not animal.is_alive and not animal.death_is_final():
                animal.is_alive = True
                animal.died_today = False

        # juveniles grow up (calves -> cows, lambs -> sheep)
        grown_up = self._grow_up_juveniles()

        # breeding
        births, pregnancies_today = self._breed()
        births.extend(self.births_today)

        # remove dead animals and return them for the log
        dead = self.remove_dead()

        # the coop exists as long as at least one hen is alive; it goes when the last one dies
        coop_active = self._hen_count() > 0
        coop_gone = self.had_hens_yesterday and not coop_active
        self.had_hens_yesterday = coop_active
        # gather every animal to build the full animal_states report
        all_animals_today = []
        for animal in self.animals:
            all_animals_today.append(animal)
        for animal in dead:
            all_animals_today.append(animal)

        animal_states = []
        for animal in all_animals_today:
            # safety. Hungry animals have grazing_cell = None
            grazing_cell_pos = None
            if animal.grazing_cell is not None:
                grazing_cell_pos = (animal.grazing_cell.x, animal.grazing_cell.y)

            animal_states.append(
                {
                    "id": animal.id,
                    "name": animal.name,
                    "symbol": animal.symbol,
                    "species": animal.species,
                    "display_pos": animal.display_pos,
                    "grazing_cell_pos": grazing_cell_pos,
                    "satiety": animal.satiety,
                    "age": animal.age,
                    "is_adult": animal.is_adult,
                    "is_pregnant": animal.is_pregnant,
                    "ate": animal.ate_today,
                    "is_alive": animal.is_alive,
                    "died_today": animal.died_today,
                }
            )

        # work out the cause of death
        death_causes = {}
        dead_animal_names = []
        for animal in dead:
            dead_animal_names.append(animal.name)
            if animal.id in killed_by_predator:
                death_causes[animal.name] = "predator"
            elif animal.id in dead_before_predators:
                death_causes[animal.name] = "random event"
            elif animal.species == "hen":
                death_causes[animal.name] = "old age"
            else:
                death_causes[animal.name] = "hunger"

        # collect grass coordinates for the visualization
        grass_positions = []
        for cell in self.pasture.grass_cells():
            grass_positions.append((cell.x, cell.y))

        # collect predator coordinates for the visualization
        predator_positions = []
        for p in self.predators:
            predator_positions.append(p.position)

        # whether Uncle the Ranger is watching the pasture. If so, we draw his figure
        ranger_active = False
        for e in self.events.active:
            if isinstance(e, ForestRanger):
                ranger_active = True

        # finances - each animal reports its own income polymorphically.
        # Exception: with the vat standing, adult sheep milk is not sold directly but goes
        # into the vat, where after a few days it ripens into more valuable cheese.
        income = 0
        sheep_milk_today = 0
        for animal in self.animals:
            if self.cheese_vat and animal.produces_sheep_milk():
                sheep_milk_today += 1
            else:
                income += animal.product_value()

        cheese_state = self._process_cheese_vat(sheep_milk_today)
        income += cheese_state["cheese_today"]

        finances_state = self.finances.settle_day(income, DAILY_FARM_COST, self.day)

        # the day's log:
        fed_animals = []
        hungry_animals = []
        for animal in self.animals:
            if animal.ate_today:
                fed_animals.append(animal.name)
            else:
                hungry_animals.append(animal.name)

        log = {
            "day": self.day,
            "weather": weather_state,
            "births": births,
            "resurrections": self.resurrections_today,
            "dead": dead_animal_names,
            "death_causes": death_causes,
            "grown_up": grown_up,
            "fed": fed_animals,
            "hungry": hungry_animals,
            "predators": predator_positions,
            "animal_states": animal_states,
            "grass_patches": grass_positions,
            "finances": finances_state,
            "cheese_vat": cheese_state,
            "events": event_descriptions,
            "pregnancies": pregnancies_today,
            "purchases": self.purchases_today,
            "fence_active": fence_active,
            "fence_days": self.fence_days_left,
            "fence_destroyed": fence_destroyed,
            "fence_holes": list(self.fence_holes),
            "predator_through_hole": predator_through_hole,
            "ranger_active": ranger_active,
            "antenna_active": antenna_active,
            "antenna_days": self.antenna_days_left,
            "coop_active": coop_active,
            "coop_gone": coop_gone,
            "hen_lifespan": config.HEN_LIFESPAN,
        }
        # the purchases are now in the log, so clear the buffer for the next day
        self.purchases_today = []
        return log
