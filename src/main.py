from src.config import *
from src.simulation import Simulation
import os
import random
import sys
from src.logger import header

os.system("")

# colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[96m"
RESET = "\033[0m"


def green(text):
    return f"{GREEN}{text}{RESET}"


def yellow(text):
    return f"{YELLOW}{text}{RESET}"


def red(text):
    return f"{RED}{text}{RESET}"


def blue(text):
    return f"{BLUE}{text}{RESET}"


# flush the buffer before each input in main. This fixes the bug where the day showed up twice
# on a single Enter press
def read_input(prompt=""):
    sys.stdout.flush()
    return input(prompt)


# ask the player for a seed. With no input we draw a random one, so seeds can be compared later
def ask_for_seed():
    while True:
        sys.stdout.flush()
        answer = input(
            "Enter a seed (integer >= 0, Enter = random): "
        ).strip()

        # Enter = draw a new seed
        if answer == "":
            seed = random.randrange(1, 1_000_000)
            random.seed(seed)
            print(
                yellow(
                    f"Drew a new seed: {seed} (save it if you want to replay this game)"
                )
            )
            return seed

        # try to turn it into an integer
        try:
            seed = int(answer)
        except ValueError:
            print(
                red(
                    "The seed must be an integer (e.g. 1, 42, 1000). Try again."
                )
            )
            continue

        # the seed cannot be negative
        if seed < 0:
            print(
                red(
                    "The seed cannot be negative. Enter a number >= 0. Try again."
                )
            )
            continue

        random.seed(seed)
        print(yellow(f"Seed set: {seed}"))
        return seed


# ask the player for one parameter. Enter = the default value
def ask(text, default, type_, description="", minimum=None, maximum=None):
    if description:
        print(blue(description))

    # build the allowed-range text for the error message
    if minimum is not None and maximum is not None:
        allowed = f"between {minimum} and {maximum}"
    elif minimum is not None:
        allowed = f"no less than {minimum}"
    elif maximum is not None:
        allowed = f"no more than {maximum}"
    else:
        allowed = ""

    while True:
        sys.stdout.flush()
        answer = input(f"{text} [{default}]: ").strip()
        if answer == "":
            return default  # Enter = the default value

        # try to convert to the right type (int/float)
        try:
            value = type_(answer)
        except ValueError:
            print(red("That is not a valid number. Try again."))
            continue

        # range check with a readable message
        out_of_range = (minimum is not None and value < minimum) or (
            maximum is not None and value > maximum
        )
        if out_of_range:
            print(
                red(f"Value out of range, allowed {allowed}. Try again.")
            )
            continue

        return value


# greet the player and explain the values set at the start of the simulation
def main():
    print()
    print(header("COW FARM"))
    print(
        green(
            "You manage a dairy cow farm, where 1 turn = 1 day.\n"
            "An adult cow gives 20 zł of milk a day, and keeping the farm\n"
            "running costs 50 zł a day (you need at least 3 adult cows\n"
            "to break even).\n\n"
            "A calf gives no milk until it grows up.\n"
            "Yesterday's weather decides how much grass grows the next day.\n"
            "The goal is to pick starting settings so the farm survives as\n"
            "long as possible and ends up as rich as possible.\n\n"
            "SHEEP (buyable only in the shop): get hungry slower than cows,\n"
            "so they live longer, but their milk is worth little (5 zł).\n"
            "They only pay off after you buy a CHEESE VAT (one per farm):\n"
            "the vat turns sheep milk into cheese. The milk ripens in the\n"
            "vat for 3 days, then becomes cheese worth 30 zł per sheep\n"
            "(10 zł more than a cow). Sheep give milk every day, so cheese\n"
            "comes out daily, just with a 3-day delay.\n\n"
            "SHOP: every repeat purchase of the same item costs more, so it\n"
            "is worth spreading your money around.\n\n"
            "Values in '[]' are the defaults, so press ENTER to accept them."
        )
    )
    print(header("STARTING SETTINGS"))

    seed = ask_for_seed()
    print()  # blank line

    params = {
        "seed": seed,
        "farm_name": ask(
            "Farm name", "My Farm", str, "The farm name, shown in the ranking."
        ),
        "starting_cows": ask(
            "Starting cows",
            5,
            int,
            "How many adult cows to start with. Each one = +20 zł/day.",
            minimum=1,
            maximum=400,
        ),
        "starting_budget": ask(
            "Starting budget",
            START_BUDGET,
            float,
            "Money to start with. A day costs 50 zł.",
            minimum=1,
        ),
        "predator_chance": ask(
            "Predator chance (0-1)",
            PREDATOR_CHANCE,
            float,
            "0 = never, 1 = every day.",
            minimum=0,
            maximum=1,
        ),
        "max_predators": ask(
            "Max predators",
            MAX_PREDATORS,
            int,
            "How many can appear at once.",
            minimum=1,
            maximum=10,
        ),
        "max_days": ask(
            "Max days",
            MAX_DAYS,
            int,
            "After this many days the simulation ends on its own.",
            minimum=1,
        ),
        "event_chance": ask(
            "Random event chance (0-1)",
            EVENT_CHANCE,
            float,
            "How often something unexpected happens.",
            minimum=0,
            maximum=1,
        ),
    }
    simulation = Simulation()
    simulation.start(params)


if __name__ == "__main__":  # safeguard
    main()
