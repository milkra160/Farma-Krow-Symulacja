# The Logger class formats and prints the daily log in the terminal

WIDTH = 56
# colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
PINK = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
FADED_GREEN = "\033[2;32m"
FADED_RED = "\033[2;31m"


def faded_green(text):
    return f"{FADED_GREEN}{text}{RESET}"


def faded_red(text):
    return f"{FADED_RED}{text}{RESET}"


def red(text):
    return f"{RED}{text}{RESET}"


def green(text):
    return f"{GREEN}{text}{RESET}"


def yellow(text):
    return f"{YELLOW}{text}{RESET}"


def gray(text):
    return f"{GRAY}{text}{RESET}"


def pink(text):
    return f"{PINK}{text}{RESET}"


def cyan(text):
    return f"{CYAN}{text}{RESET}"


def header(title):
    return yellow(f" {title} ".center(WIDTH, "="))


def line():
    return gray("-" * WIDTH)


class Logger:
    WIDTH = 56  # width of the "daily log"

    def print_log(self, log: dict):
        print()

        # day header (centered, shared style)
        print(yellow(header(f"DAY {log['day']} | weather: {log['weather']}")))

        # active random events (separate section)
        if len(log["events"]) > 0:
            print(yellow("RANDOM EVENTS:"))
            for description in log["events"]:
                print(f" - {description}")
        else:
            print(gray("RANDOM EVENTS: none"))

        print(gray("-" * self.WIDTH))

        # your actions: shop purchases + fence status
        purchases = log.get("purchases", [])
        if len(purchases) > 0 or log.get("fence_destroyed"):
            print(green("YOUR ACTIONS:"))
            for purchase in purchases:
                print(f"   - {purchase}")
            if log.get("fence_destroyed"):
                print(red("   The fence broke!"))
            print(gray("-" * self.WIDTH))

        # number of grass patches
        patch_count = len(log["grass_patches"])
        print(f"GRASS PATCHES: {patch_count}")
        print(gray("-" * self.WIDTH))

        # finances (aligned in columns)
        finances = log["finances"]
        print("FINANCES:")
        print(
            f"   income: {finances['income']:>8.0f}      cost:   {finances['cost']:>8.0f}"
        )

        balance = finances["balance"]
        if balance >= 0:
            change = faded_green(f"(+{balance:.0f})")
        else:
            change = faded_red(f"({balance:.0f})")

        print(
            f"   balance:  {balance:>8.0f}      budget: {finances['budget']:>8.0f} {change}"
        )
        print(gray("-" * self.WIDTH))

        # cheese vat: how much sheep milk was added today, how much cheese was made, and how much
        # ripens the next day (milk ripens into cheese with a delay)
        cheese_vat = log.get("cheese_vat")
        if cheese_vat and cheese_vat["active"]:
            print("CHEESE VAT:")
            if cheese_vat["cheese_today"] > 0:
                print(green(f"   cheese ready today: +{cheese_vat['cheese_today']} zł"))
            if cheese_vat["milk_today"] > 0:
                print(f"   sheep milk added to the vat: {cheese_vat['milk_today']}")
            if cheese_vat["cheese_tomorrow"] > 0:
                print(f"   cheese ready tomorrow: +{cheese_vat['cheese_tomorrow']} zł")
            if cheese_vat["batches_in_vat"] == 0 and cheese_vat["cheese_today"] == 0:
                print(gray("   vat empty, waiting for sheep milk"))
            print(gray("-" * self.WIDTH))

        # HERD: births/growing up/deaths
        if len(log["births"]) > 0:
            print(green(f"   births:  {', '.join(log['births'])}"))
        if log.get("grown_up") and len(log["grown_up"]) > 0:
            print(f"   grew up today:    {', '.join(log['grown_up'])}")
        if len(log["dead"]) > 0:
            parts = []
            for name in log["dead"]:
                parts.append(f"{name} ({log['death_causes'][name]})")
            print(red(f"   deaths:      {', '.join(parts)}"))

        if log.get("resurrections") and len(log["resurrections"]) > 0:
            print(cyan(f"   resurrection: {', '.join(log['resurrections'])}"))

        # herd statistics
        if log.get("pregnancies") and len(log["pregnancies"]) > 0:
            print(pink(f"   pregnancy:      {', '.join(log['pregnancies'])}"))

        # separate tables for cows and sheep. Same form, each species counted on its own
        self._species_section(log, "cow", "LIVING COWS")
        self._species_section(log, "sheep", "LIVING SHEEP")
        if log.get("coop_gone"):
            print(gray("The coop is empty, the last hen died"))
        self._hen_section(log)
        print("=" * self.WIDTH)

    # print one species: a fed/hungry count plus a table of the living with a satiety bar.
    # Same form for cows and sheep. We split them by the "species" field of the animal states.
    def _species_section(self, log: dict, species: str, title: str):
        animals = [a for a in log["animal_states"] if a.get("species") == species]
        if len(animals) == 0:
            return
        alive = [a for a in animals if a["is_alive"]]
        fed = sum(1 for a in alive if a["ate"])
        hungry = len(alive) - fed
        print(gray("-" * self.WIDTH))
        print(f"{title}: {len(alive)} | fed: {fed} | hungry: {hungry}")
        for a in alive:
            print(
                f"   {a['symbol']} {a['name']:<12} {self._hunger_bar(a['satiety'])} {a['satiety']:>3}/100"
            )

    # a separate section for hens: they have no satiety bar (the coop feeds them), so instead of
    # satiety we show how much of their fixed lifespan has passed, which tells you which hen is about to die
    def _hen_section(self, log: dict):
        hens = [a for a in log["animal_states"] if a.get("species") == "hen"]
        if len(hens) == 0:
            return
        alive = [a for a in hens if a["is_alive"]]
        lifespan = log.get("hen_lifespan", 7)
        print(gray("-" * self.WIDTH))
        print(f"LIVING HENS: {len(alive)}  (coop active)")
        for a in alive:
            print(f"   H {a['name']:<12} age {a['age']}/{lifespan} days")

    # draws an animal's satiety bar (0-100), the color depends on the hunger level
    def _hunger_bar(self, satiety: int) -> str:
        length = 10
        filled = satiety * length // 100  # how many blocks to fill (satiety 0-100)
        if filled > length:
            filled = length
        if filled < 0:
            filled = 0
        empty = length - filled
        bar = "█" * filled + "░" * empty

        if satiety >= 60:
            return green(bar)
        elif satiety >= 30:
            return yellow(bar)
        else:
            return red(bar)

    def print_final_summary(self, days: int, reason: str, finances: dict):
        print()
        print(header("END OF SIMULATION"))
        print(f"   reason:          {reason}")
        print(f"   days survived:   {days}")
        print(f"   final budget:    {finances['budget']:.0f} zł")
        print("=" * WIDTH)

    def print_statistics(self, s: dict):
        print()  # empty line for looks
        print(red("=== FINAL STATISTICS ==="))
        print(f"Total births:   {s['births']}")
        print(f"Total resurrections: {s['resurrections']}")
        print(f"Total deaths:       {s['deaths']}")
        print(f"Total cows on the farm: {s['total_cows']}")
        print(
            f"Largest herd: {s['max_herd']} animals (day {s['max_herd_day']})"
        )
        print(
            f"Final herd: {s['final_cows']} cows | "
            f"{s['final_sheep']} sheep | {s['final_hens']} hens"
        )
        print(f"Random events:   {s['events']}")
        print(line())
        print(
            f"Weather: sun {s['sunny_days']} / rain {s['rainy_days']} / drought {s['drought_days']}"
        )
        print(
            f"Finances: income {s['total_income']:.0f} zł, "
            f"cost {s['total_cost']:.0f} zł, "
            f"final budget {s['final_budget']:.0f} zł"
        )
        print(line())
        print(
            f"Shop purchases: animals {s['bought_animals']}, "
            f"feed bags {s['bought_feed']}, "
            f"upgrades {s['bought_upgrades']}"
        )
        print("=" * WIDTH)
