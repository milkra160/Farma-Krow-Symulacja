import json
import os


# color codes for later display, kept here to make the code simpler
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


# template for showing the ranking as a tidy table
_TEMPLATE = (
    "{rank:<4}{name:<13}{seed:<8}{days:<5}"
    "{max_budget:<12}{max_herd:<11}{cows:<6}"
    "{start_budget:<11}{pred:<6}{end:<13}"
)


def _sort_key(result: dict):
    return (
        result["days_survived"],
        result["max_budget"],
        result["max_herd"],
    )


# The Ranking class saves simulation results to a json file and reads them back
class Ranking:
    def __init__(self, file: str = "ranking.json"):
        self.file = file

    def show_criteria(self):  # the ranking's sort criteria
        print()
        print(GREEN + "=== HOW WE SCORE (ranking criteria) ===" + RESET)
        print("We pick the best result in order by:")
        print("  1. Days survived  (more is better)")
        print("  2. On a tie: max budget  (more is better)")
        print("  3. On a further tie: max herd")
        print(
            "Note: comparing configs fairly only makes sense within the same seed."
        )

    def load(self) -> list:
        # safety. With no file we return an empty list
        if not os.path.exists(self.file):
            return []
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
        if not isinstance(data, list):
            return []
        # sort descending by days survived
        data.sort(key=_sort_key, reverse=True)
        return data

    def save_result(self, result: dict):
        ranking = self.load()  # what we already have is in the file
        ranking.append(result)  # add the new result
        ranking.sort(key=_sort_key, reverse=True)
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(ranking, f, ensure_ascii=False, indent=2)

    # pull the seed out of a result's start params (may be None)
    def _result_seed(self, result: dict):
        return result.get("start_params", {}).get("seed")

    # build the colored header of the ranking table
    def _table_header(self):
        text = _TEMPLATE.format(
            rank="No.",
            name="Farm",
            seed="Seed",
            days="Days",
            max_budget="Max budget",
            max_herd="Max herd",
            cows="Cows",
            start_budget="Start bud.",
            pred="Pred.",
            end="End",
        )
        line = "-" * len(text)
        return YELLOW + text + RESET + "\n" + line

    # one table row
    def _row(self, place: int, result: dict) -> str:
        p = result.get("start_params", {})
        return _TEMPLATE.format(
            rank=f"{place}.",
            name=str(result["farm_name"])[:15],
            seed=str(self._result_seed(result)),
            days=str(result["days_survived"]),
            max_budget=str(result["max_budget"]),
            max_herd=str(result["max_herd"]),
            cows=str(p.get("starting_cows")),
            start_budget=str(p.get("starting_budget")),
            pred=str(p.get("predator_chance")),
            end=str(result["end_reason"])[:19],
        )

    def show_for_seed(self, seed):
        ranking = self.load()
        only_this_seed = [r for r in ranking if self._result_seed(r) == seed]

        print()
        print(GREEN + f"=== RANKING for seed {seed} ===" + RESET)

        print()  # blank line
        if not only_this_seed:
            print("No results for this seed.")
            return
        print(self._table_header())
        place = 1
        for result in only_this_seed:
            print(self._row(place, result))
            place += 1

    def show_top_10(self):
        ranking = self.load()

        print()
        print(GREEN + "=== TOP 10 (all seeds together) ===" + RESET)
        print()

        if not ranking:
            print("No results.")
            return
        print(self._table_header())
        place = 1
        for result in ranking[:10]:
            print(self._row(place, result))
            place += 1
