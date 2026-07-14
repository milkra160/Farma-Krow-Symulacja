class Visualization:  # draws a still frame of the farm at the end of the day
    COLORS = {
        "green": "\033[92m",
        "orange": "\033[93m",
        "red": "\033[91m",
        "yellow": "\033[33m",
        "gray": "\033[90m",
        "white": "\033[37m",
        "cyan": "\033[96m",
        "reset": "\033[0m",  # turn colors off so the board is not broken on later days
    }

    def __init__(self, colors: bool = True):
        self.colors = colors  # kept so colors can be turned off

    def _colorize(self, text: str, color: str) -> str:
        if not self.colors:
            return text
        return self.COLORS[color] + text + self.COLORS["reset"]

    # look through the log for an animal standing on cell x,y and return its dict, or None
    def _animal_at(self, log: dict, x: int, y: int):
        found = None
        for animal in log["animal_states"]:
            if animal["display_pos"] == (x, y):
                # a dead animal takes priority
                if not animal["is_alive"]:
                    return animal
                if found is None:
                    found = animal
        return found

    # decide which symbol and color a cell gets
    def _cell_symbol(self, cell, log: dict) -> str:
        animal = self._animal_at(log, cell.x, cell.y)
        if animal is not None:
            letter = animal.get("symbol", "C")  # C cow, c calf, S sheep, l lamb, H hen
            if not animal["is_alive"]:
                return self._colorize(letter, "red")
            # a hen does not graze, so its color does not depend on satiety. Always yellow
            if animal.get("species") == "hen":
                return self._colorize(letter, "yellow")
            if animal["ate"]:
                return self._colorize(letter, "green")
            return self._colorize(letter, "orange")
        if cell.has_predator:
            return self._colorize("!", "red")
        if cell.has_grass:
            return self._colorize("G", "white")
        return self._colorize(".", "gray")

    # build the whole board as text (easier to test).
    # when the fence protects the farm we draw a double yellow frame instead of the plain one
    def _build_board(self, pasture, log: dict) -> str:
        width = pasture.width
        if log.get("fence_active"):
            # the top frame has gaps where a predator broke through the fence.
            # The gaps stay until the fence is gone (list of columns in the log)
            top_chars = ["═"] * width
            for column in log.get("fence_holes", []):
                if 0 <= column < width:
                    top_chars[column] = " "  # a hole in the fence
            top = self._colorize("╔" + "".join(top_chars) + "╗", "yellow")
            bottom = self._colorize("╚" + "═" * width + "╝", "yellow")
            vertical = self._colorize("║", "yellow")
        else:
            top = "+" + "-" * width + "+"
            bottom = top
            vertical = "|"

        lines = [top]
        for row in pasture.grid:
            line = vertical
            for cell in row:
                line += self._cell_symbol(cell, log)
            line += vertical
            lines.append(line)
        lines.append(bottom)

        # when Uncle the Ranger watches the pasture, we tuck his figure next to the board
        if log.get("ranger_active"):
            self._draw_ranger(lines)
        # when a cheese vat stands on the farm, we tuck its pot of cheese next to the board
        if log.get("cheese_vat", {}).get("active"):
            self._draw_cheese_vat(lines)
        # when the jamming antenna runs, we tuck its mast next to the board
        if log.get("antenna_active"):
            self._draw_antenna(lines)
        # when the coop stands (there are hens), we tuck its little house with a hen next to the board
        if log.get("coop_active"):
            self._draw_coop(lines)
        return "\n".join(lines)

    # a text tag next to the board for each active feature. We put them on separate rows
    # so several tags do not overlap when more than one feature is running.
    def _draw_ranger(self, lines: list):
        if len(lines) > 1:
            lines[1] += "   " + self._colorize("[ranger]", "green")

    def _draw_cheese_vat(self, lines: list):
        if len(lines) > 3:
            lines[3] += "   [cheese vat]"

    def _draw_antenna(self, lines: list):
        if len(lines) > 5:
            lines[5] += "   " + self._colorize("[antenna]", "gray")

    def _draw_coop(self, lines: list):
        if len(lines) > 7:
            lines[7] += "   [coop]"

    # the main method, draws the board on screen
    def draw_board(self, pasture, log: dict):
        print(self._build_board(pasture, log))
        # caption explaining the yellow frame, right under the board it belongs to
        if log.get("fence_active"):
            days = log["fence_days"]
            if days == 0:
                text = "The fence protects the farm. Last day, it falls apart tomorrow"
            else:
                word = "day" if days == 1 else "days"
                text = f"The fence protects the farm. {days} {word} left"
            print(self._colorize(text, "yellow"))
        # alert when a predator broke through the fence, explains the gap in the frame
        if log.get("predator_through_hole"):
            print(
                self._colorize(
                    "A predator slipped through a hole in the fence!", "red"
                )
            )
        # caption explaining the antenna mast next to the board
        if log.get("antenna_active"):
            days = log.get("antenna_days", 0)
            if days == 0:
                text = "The antenna jams UFOs. Last day"
            else:
                word = "day" if days == 1 else "days"
                text = f"The antenna jams UFOs. {days} {word} left"
            print(self._colorize(text, "cyan"))
        self.legend()

    # the legend
    def legend(self):
        print(
            "Legend: C=cow  c=calf  S=sheep  l=lamb  H=hen  "
            "G=grass  !=predator  .=empty"
        )
        fed = self._colorize("fed", "green")
        hungry = self._colorize("hungry", "orange")
        died = self._colorize("died", "red")
        print(f"animal colors: {fed} {hungry} {died}")
