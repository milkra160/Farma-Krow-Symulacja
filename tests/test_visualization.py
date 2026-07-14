from src.visualization import Visualization
from src.pasture.pasture import Pasture


def make_board_and_log():
    p = Pasture(5, 5)
    p.get_cell(1, 1).add_grass()
    p.get_cell(3, 2).has_predator = True
    log = {
        "animal_states": [
            {"display_pos": (0, 0), "is_alive": True, "ate": True, "symbol": "C"},
            {"display_pos": (2, 4), "is_alive": True, "ate": False, "symbol": "C"},
            {"display_pos": (4, 4), "is_alive": False, "ate": False, "symbol": "C"},
        ],
    }
    return p, log


def test_board_has_frame_and_dimensions():
    p, log = make_board_and_log()
    lines = Visualization(colors=False)._build_board(p, log).split("\n")
    assert len(lines) == 7  # 5 rows and 2 frame lines
    assert lines[0] == "+-----+"
    assert lines[-1] == "+-----+"


def test_board_symbols_are_correct():
    p, log = make_board_and_log()
    lines = Visualization(colors=False)._build_board(p, log).split("\n")
    assert lines[1][1] == "C"
    assert lines[2][2] == "G"
    assert lines[3][4] == "!"
    assert lines[5][5] == "C"
