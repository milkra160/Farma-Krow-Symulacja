from src.config import *
import random
import sys
from datetime import date
from src.pasture.pasture import Pasture
from src.weather import Weather
from src.finances import Finances
from src.events import EventManager
from src.farm import Farm
from src.animals.cow import Cow
from src.logger import Logger, green, red, yellow
from src.visualization import Visualization
from src.ranking import Ranking
from src.shop import Shop


# The Simulation class ties the farm, logger, visualization and ranking together.
# It runs the day loop and handles the player's controls.
class Simulation:
    def __init__(self):
        self.farm = None
        self.visualization = Visualization()
        self.logger = Logger()
        self.ranking = Ranking()
        self.shop = Shop()
        self.params = None
        self.max_days = MAX_DAYS
        self.auto_mode = False
        # stats collected across the whole game for the ranking
        self.max_budget = 0
        self.max_herd = 0
        self.max_herd_day = 0  # which day the herd was largest
        self.total_births = 0
        self.total_deaths = 0
        self.total_resurrections = 0
        # shop purchase counters (for the end-of-run statistics)
        self.bought = {"animal": 0, "feed": 0, "upgrade": 0}

    # build all the components and the starting herd in a private method
    def _prepare(self, params: dict):
        self.params = params
        self.max_days = params["max_days"]

        width, height = BOARD_SIZE
        pasture = Pasture(width, height)
        weather = Weather()
        finances = Finances()
        finances.budget = params["starting_budget"]
        events = EventManager(event_chance=params["event_chance"])

        # starting herd. Adult cows so they give milk from the very first day
        animals = []
        for i in range(params["starting_cows"]):
            cow = Cow(id=i + 1, position=(0, 0), name=random.choice(ANIMAL_NAMES))
            cow.is_adult = True
            cow.age = ADULT_AGE
            animals.append(cow)

        # assemble the farm and override the config defaults with the player's settings
        self.farm = Farm(
            params["farm_name"], pasture, weather, finances, events, animals
        )
        self.farm.predator_chance = params["predator_chance"]
        self.farm.max_predators = params["max_predators"]

        # starting statistics
        self.max_budget = finances.budget
        self.max_herd = self.farm.animal_count()

    def finish(self, reason: str):
        result = {
            "farm_name": self.farm.name,
            "date": date.today().isoformat(),
            "days_survived": self.farm.day,
            "max_budget": self.max_budget,
            "max_herd": self.max_herd,
            "end_reason": reason,
            "start_params": self.params,
        }
        self.logger.print_final_summary(
            self.farm.day, reason, {"budget": self.farm.finances.budget}
        )

        # stats from history plus the counters gathered during the game
        weather_history = self.farm.weather.history
        finances_history = self.farm.finances.history
        # how many cows and how many sheep are left in the herd at the end of the game
        final_cows = sum(1 for a in self.farm.animals if a.species == "cow")
        final_sheep = sum(1 for a in self.farm.animals if a.species == "sheep")
        final_hens = sum(1 for a in self.farm.animals if a.species == "hen")
        statistics = {
            "births": self.total_births,
            "resurrections": self.total_resurrections,
            "deaths": self.total_deaths,
            "max_herd": self.max_herd,
            "max_herd_day": self.max_herd_day,
            "total_cows": self.params["starting_cows"] + self.total_births,
            "events": self.farm.events.event_count,
            "sunny_days": weather_history.count("sunny"),
            "rainy_days": weather_history.count("rain"),
            "drought_days": weather_history.count("drought"),
            "total_income": sum(e["state"]["income"] for e in finances_history),
            "total_cost": sum(e["state"]["cost"] for e in finances_history),
            "final_budget": self.farm.finances.budget,
            "bought_animals": self.bought["animal"],
            "bought_feed": self.bought["feed"],
            "bought_upgrades": self.bought["upgrade"],
            "final_cows": final_cows,
            "final_sheep": final_sheep,
            "final_hens": final_hens,
        }
        self.logger.print_statistics(statistics)

        self.ranking.save_result(result)
        self.ranking.show_criteria()
        self.ranking.show_for_seed(self.params.get("seed"))
        self.ranking.show_top_10()

    # run one day, then print the log and the board. Returns False when the simulation should end
    def run_day(self) -> bool:
        log = self.farm.new_day()
        self.logger.print_log(log)
        self.visualization.draw_board(self.farm.pasture, log)
        self.total_births += len(log["births"])  # for statistics
        self.total_deaths += len(log["dead"])  # for statistics
        self.total_resurrections += len(log["resurrections"])  # for statistics

        # update the ranking records
        if self.farm.finances.budget > self.max_budget:
            self.max_budget = self.farm.finances.budget
        if self.farm.animal_count() > self.max_herd:
            self.max_herd = self.farm.animal_count()
            self.max_herd_day = self.farm.day

        # end conditions
        if self.farm.animal_count() == 0:
            self.finish("herd died out")
            return False
        if self.farm.finances.is_bankrupt():
            self.finish("bankruptcy")
            return False
        if self.farm.day >= self.max_days:
            self.finish("time is up")
            return False
        return True

    # simulate n days in a row without pausing.
    # returns False if the simulation ended along the way
    def _simulate_n_days(self, n: int) -> bool:
        for _ in range(n):
            if not self.run_day():
                return False
        return True

    # the main loop, asks the player each day or runs to the end
    def main_loop(self):
        while True:
            if self.auto_mode:
                if not self.run_day():
                    break
                continue

            # step mode, show the menu and wait for the player
            print(
                "[Enter] Next day   [s] +10 days   [a] To the end  [k] Shop  [c] Quit"
            )
            sys.stdout.flush()  # another attempt to fix the double-day bug on a single Enter
            choice = input("> ").strip().lower()

            if choice == "":
                keep_going = self.run_day()
            elif choice == "s":
                keep_going = self._simulate_n_days(10)
            elif choice == "a":
                self.auto_mode = True
                keep_going = self.run_day()
            elif choice == "k":
                self._open_shop()  # the shop does not take a day, so we return to the menu
                continue
            elif choice == "c":
                self.finish("manual quit")
                break
            else:
                print("Pick one of the options")
                continue

            if not keep_going:
                break

    # terminal driver for the shop. All the buying logic sits in the Shop class;
    # here we only show the catalog and read the choice, so a GUI can reuse the same methods
    def _open_shop(self):
        while True:
            print(yellow("=== SHOP ==="))
            print(f"Budget: {self.farm.finances.budget:.0f} zł")
            available = self.shop.available_items(self.farm)
            for i in range(len(available)):
                item = available[i]
                print(f"  [{i + 1}] {item.name} - {item.price} zł  ({item.description})")
            print("  [w] Leave the shop")

            sys.stdout.flush()
            choice = input("shop > ").strip().lower()
            if choice == "w" or choice == "":
                break

            # check whether the player gave a valid item number
            try:
                index = int(choice) - 1
            except ValueError:
                print(red("Enter an item number or [w] to leave"))
                continue
            if index < 0 or index >= len(available):
                print(red("No item with that number"))
                continue

            item = available[index]
            success, message = self.shop.buy(item, self.farm)
            if success:
                print(green(message))
                # record the purchase: a counter for statistics plus a buffer for the next day's log
                self.bought[item.category] += 1
                self.farm.purchases_today.append(message)
            else:
                print(red(message))

    def start(self, params: dict):
        self._prepare(params)
        self.main_loop()
